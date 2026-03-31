from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, PollOption, Vote, MemberProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import MemberProfileForm

# Create your views here.
def home(request):
    poll = None
    user_vote = None
    option_stats = {}

    # Only load poll data if the user is logged in
    if request.user.is_authenticated:
        poll = Poll.objects.filter(is_closed=False).order_by('-created_at').first()

        if poll:
            # Precompute stats for each option
            for option in poll.options.all():
                count = poll.votes.filter(option=option).count()
                total = poll.votes.count()
                percentage = round((count / total) * 100) if total > 0 else 0

                option_stats[option.id] = {
                    "count": count,
                    "percentage": percentage,
                }

            # Get user's vote
            user_vote = poll.votes.filter(user=request.user).first()

    return render(request, "core/home.html", {
        "poll": poll,
        "user_vote": user_vote,
        "option_stats": option_stats,
    })


def vote(request, poll_id, option_id):
    poll = get_object_or_404(Poll, id=poll_id)
    option = get_object_or_404(PollOption, id=option_id, poll=poll)

    if not request.user.is_authenticated:
        return redirect("/accounts/login/")

    Vote.objects.update_or_create(
        poll=poll,
        user=request.user,
        defaults={"option": option}
    )

    return redirect("home")

# Signup View
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("edit_profile")
    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})

# Profile Page
@login_required
def my_profile(request):
    profile = request.user.memberprofile
    return render(request, "core/my_profile.html", {"profile": profile})


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("my_profile")  # ← NEW
    else:
        form = CustomUserCreationForm()

    return render(request, "core/signup.html", {"form": form})

@login_required
def edit_profile(request):
    profile, created = MemberProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MemberProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("my_profile")
    else:
        form = MemberProfileForm(instance=profile)

    return render(request, "core/edit_profile.html", {"form": form})
