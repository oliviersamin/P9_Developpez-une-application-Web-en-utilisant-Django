"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'base_app'

urlpatterns = [
    url('creation_ticket', views.creation_ticket, name='creation_ticket'),
    url('creation_critic', views.creation_critic, name='creation_critic'),
    url('feed', views.feed, name="feed"),
    url('/', views.feed, name="index"),

]
