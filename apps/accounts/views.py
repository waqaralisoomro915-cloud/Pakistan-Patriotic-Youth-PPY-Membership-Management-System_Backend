from django.http import HttpResponse

def accounts(request):
    return HttpResponse("Hey this is the accounts section ")