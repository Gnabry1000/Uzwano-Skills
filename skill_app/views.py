from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, SkillAd
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password, check_password

def home(request):
    return render(request, 'skill_app/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'skill_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('login')

        if check_password(password, user.password):
            request.session['user_email'] = user.email
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('dashboard')  # ✅ Go to the personalized page
        else:
            messages.error(request, "Invalid password.")
            return redirect('login')  # ✅ Stay on login page for retry

    return render(request, 'skill_app/login.html')

def dashboard(request):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, "Please log in first.")
        return redirect('login')

    user = User.objects.get(email=user_email)

    # Handle new skill post
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        rate = float(request.POST.get('rate'))
        available_days = request.POST.get('available_days')

        if rate < 10 or rate > 100:
            messages.error(request, "Rate must be between R10 and R100.")
        else:
            SkillAd.objects.create(
                user=user,
                title=title,
                description=description,
                rate=rate,
                available_days=available_days,
            )
            messages.success(request, f"Skill '{title}' added successfully!")

    # Ads by other users
    other_ads = SkillAd.objects.exclude(user=user)
    # Ads by current user
    my_ads = SkillAd.objects.filter(user=user)

    return render(request, 'skill_app/dashboard.html', {
        'user': user,
        'other_ads': other_ads,
        'my_ads': my_ads
    })

def logout_view(request):
    request.session.flush()
    messages.info(request, "You’ve been logged out.")
    return redirect('login')
