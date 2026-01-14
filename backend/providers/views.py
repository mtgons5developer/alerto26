# Either remove or use the import
from django.http import HttpResponse


def test_debug(request):
    return HttpResponse("Debug works!")
