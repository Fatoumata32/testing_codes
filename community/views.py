from django.shortcuts import render

def community_view(request):
    return render(request, 'farmconnect_app/community.html')