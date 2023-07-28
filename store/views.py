from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def our_story(request):
    return render(request, 'our-story.html')


def your_services(request):
    return render(request, 'your-services.html')
