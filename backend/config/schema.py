# backend/config/schema.py
import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from emergencies.models import Emergency
from providers.models import Provider

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password',)

class EmergencyType(DjangoObjectType):
    # Define location as a custom scalar or exclude it
    location_lat = graphene.Float()
    location_lng = graphene.Float()
    
    class Meta:
        model = Emergency
        fields = ("id", "code", "emergencyType", "priority", "status", "createdAt")
        # Or exclude location: exclude = ("location",)
    
    def resolve_location_lat(self, info):
        if self.location:
            return self.location.y  # latitude
        return None
    
    def resolve_location_lng(self, info):
        if self.location:
            return self.location.x  # longitude
        return None

class ProviderType(DjangoObjectType):
    class Meta:
        model = Provider
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    # User queries
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID())
    
    # Emergency queries
    emergencies = graphene.List(EmergencyType)
    emergency = graphene.Field(EmergencyType, id=graphene.ID())
    active_emergencies = graphene.List(EmergencyType)
    
    # Provider queries
    providers = graphene.List(ProviderType)
    provider = graphene.Field(ProviderType, id=graphene.ID())
    nearby_providers = graphene.List(
        ProviderType,
        lat=graphene.Float(required=True),
        lng=graphene.Float(required=True),
        radius=graphene.Int(default_value=5000),
        service_type=graphene.String()
    )
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication required')
        return user
    
    def resolve_nearby_providers(self, info, lat, lng, radius, service_type=None):
        from django.contrib.gis.geos import Point
        from django.contrib.gis.db.models.functions import Distance
        
        point = Point(lng, lat, srid=4326)
        queryset = Provider.objects.filter(
            is_active=True,
            status='AVAILABLE'
        ).annotate(
            distance=Distance('current_location', point)
        ).filter(
            distance__lte=radius
        ).order_by('distance')
        
        if service_type:
            queryset = queryset.filter(service_types__contains=[service_type])
        
        return queryset

class CreateEmergency(graphene.Mutation):
    class Arguments:
        emergency_type = graphene.String(required=True)
        lat = graphene.Float(required=True)
        lng = graphene.Float(required=True)
        description = graphene.String()
        symptoms = graphene.List(graphene.String)
    
    emergency = graphene.Field(EmergencyType)
    
    def mutate(self, info, emergency_type, lat, lng, description="", symptoms=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication required')
        
        from django.contrib.gis.geos import Point
        from emergencies.models import Emergency
        
        location = Point(lng, lat, srid=4326)
        
        emergency = Emergency.objects.create(
            user=user,
            emergency_type=emergency_type,
            location=location,
            description=description,
            symptoms=symptoms or []
        )
        
        return CreateEmergency(emergency=emergency)

class Mutation(graphene.ObjectType):
    create_emergency = CreateEmergency.Field()
    
    # Authentication
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)