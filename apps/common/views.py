from django.http import HttpResponse
def common(request):
    return HttpResponse("hey this is the common section")