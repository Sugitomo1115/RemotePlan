from django.shortcuts import render

# Create your views here.
def top(request):
    """トップ画面"""
    return render(request, "remote_eventplan/top.html")