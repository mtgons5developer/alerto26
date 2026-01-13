# Either remove or use the import
from django.shortcuts import render
from django.http import HttpResponse


def test_debug(request):
    x = 5
    return HttpResponse("Debug works!")
