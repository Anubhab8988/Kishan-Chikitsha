# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# import json

# class SignUpView(View):
#     @csrf_exempt
#     def post(self, request):
#         data = json.loads(request.body)
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')

#         if User.objects.filter(username=username).exists():
#             return JsonResponse({'error': 'Username already exists'}, status=400)

#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()
#         return JsonResponse({'message': 'User created successfully'}, status=201)

# class SignInView(View):
#     @csrf_exempt
#     def post(self, request):
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'message': 'Login successful'}, status=200)
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=401)

# class SignOutView(View):
#     def post(self, request):
#         logout(request)
#         return JsonResponse({'message': 'Logout successful'}, status=200)
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages   # ✅ import messages
from .models import Profile

def index_view(request):
    return render(request, 'index.html')
def signup_view(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # check passwords match
        if password != confirm_password:
            return render(request, 'signup.html', {"error": "Passwords do not match"})

        if full_name and email and password:
            # ✅ create user (Django hashes automatically)
            user = User.objects.create_user(username=email, email=email, password=password)

            # ✅ save full_name in Profile
            Profile.objects.create(user=user, full_name=full_name)

            print("User created:", user.username)

            # ✅ show success message
            messages.success(request, "Successfully registered! Please sign in.")

            # ✅ redirect to signin
            return redirect("/signin/")

    return render(request, 'signup.html')


def signin_view(request):
    print("Signin view called")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ✅ authenticate using email (username=email since we set it like that above)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'signin.html', {"message": f"Welcome, {user.profile.full_name}!"})
        else:
            return render(request, 'signin.html', {"error": "Invalid credentials"})

    return render(request, 'signin.html')
