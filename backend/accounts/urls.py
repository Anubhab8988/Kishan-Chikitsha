from django.contrib import admin
from django.urls import path
from Authentication import views  # <--- CRITICAL: Import views from your app folder

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Homepage (http://127.0.0.1:8000/)
    path('', views.index_view, name='index'),

    # Sign Up (http://127.0.0.1:8000/signup/)
    path('signup/', views.signup_view, name='signup'),

    # Sign In (http://127.0.0.1:8000/signin/)
    path('signin/', views.signin_view, name='signin'),
]