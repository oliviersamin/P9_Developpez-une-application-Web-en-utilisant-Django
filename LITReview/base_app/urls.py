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
    url('creation_ticket', views.CreationTicketForm.as_view(), name='creation_ticket'),
    url('creation_critic', views.CreationCriticForm.as_view(), name='creation_critic'),
    url(r'^modify_ticket_(?P<ticket_id>[0-9]+)$', views.modify_ticket, name='modify_ticket'),
    url('delete_ticket', views.delete_ticket, name='delete_ticket'),
    url(r'^modify_review_(?P<review_id>[0-9]+)$', views.modify_review, name='modify_review'),
    url('delete_review', views.delete_review, name='delete_review'),
    url('followers', views.ListFollowers.as_view(), name='followers'),
    # url('followers', views.followers, name='followers'),
    url('feed', views.feed, name="feed"),
    url('/', views.feed, name="index"),
    url('my_posts', views.my_posts, name='my_posts'),
    url(r'^review_from_ticket_(?P<ticket_id>[0-9]+)$', views.create_review_from_ticket,
        name='create_review_from_ticket'),

]
