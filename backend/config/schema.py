import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from emergencies.models import Emergency
from providers.models import Provider

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
        interfaces = (graphene.relay.Node,)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class EmergencyType(DjangoObjectType):
    class Meta:
        model = Emergency
        fields = "__all__"


class ProviderType(DjangoObjectType):
    class Meta:
        model = Provider
        fields = "__all__"


class Query(graphene.ObjectType):
    emergencies = graphene.List(EmergencyType)
    providers = graphene.List(ProviderType)

    def resolve_emergencies(self, info):
        return Emergency.objects.all()

    def resolve_providers(self, info):
        return Provider.objects.all()


class CreateEmergency(graphene.Mutation):
    class Arguments:
        emergency_type = graphene.String(required=True)
        user_id = graphene.UUID(required=True)  # Add this
        latitude = graphene.Float(required=True)
        longitude = graphene.Float(required=True)
        description = graphene.String()

    emergency = graphene.Field(EmergencyType)

    def mutate(
        self, info, emergency_type, latitude, longitude, user_id, description=None
    ):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            # Add context but preserve original exception type
            e.message = f"User with ID {user_id} does not exist"
            raise

        emergency = Emergency.objects.create(
            user=user,
            emergency_type=emergency_type,
            latitude=latitude,
            longitude=longitude,
            description=description or "",
        )
        return CreateEmergency(emergency=emergency)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    def mutate(self, info, username, password, email, first_name="", last_name=""):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_emergency = CreateEmergency.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
