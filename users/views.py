from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# ----------------------------------------
# Register
# ----------------------------------------


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")

# ----------------------------------------
# Login
# ----------------------------------------

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# ----------------------------------------
# Logout
# ----------------------------------------

def logout_view(request):

    logout(request)
    messages.success(request, "Logged out successfully.")

    return redirect("landing")