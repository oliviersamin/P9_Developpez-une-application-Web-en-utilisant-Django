from django.shortcuts import render
from . import filter_viewable_posts as filter
from . import models as mod
from django.template import loader
from django.db.models import CharField, Value
from itertools import chain
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

def feed(request):
    """ display the stream which is on the first page after success login of the user """
    reviews = mod.Review.objects.filter().order_by('-time_created')
    # tickets = mod.Ticket.objects.filter(user=request.user).order_by('-time_created')
    tickets = mod.Ticket.objects.filter().order_by('-time_created')
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {'posts': posts}

    return render(request, 'base_app/feed.html', context=context)

def home(request):
    context = {}
    return render(request, 'base_app/home.html', context=context)