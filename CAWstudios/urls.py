"""CAWstudios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from bookmyticket  import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('bookmyticket.urls')),
    path('api/v1/genToken', views.MyObtainTokenPairView.as_view(), name="generate_token"),
    path('api/v1/refreshToken', jwt_views.TokenRefreshView.as_view(), name="refresh_token"),
    path('api/v1/verifyToken', jwt_views.TokenVerifyView.as_view(), name="verify_token"),
]
