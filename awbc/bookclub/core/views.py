from django.shortcuts import render
from .models import Poll

# Create your views here.
def home(request):
    poll = Poll.objects.filter(is_closed=False).order_by('-created_at').first()

    return render(request, "core/home.html", {
        "poll": poll,
    }
    )
