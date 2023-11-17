from django.http import HttpResponse

def index(request):
    return HttpResponse("Some beautiful html here")