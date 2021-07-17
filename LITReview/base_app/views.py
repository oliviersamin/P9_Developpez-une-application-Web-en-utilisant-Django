from django.shortcuts import render
# from django.http import HttpResponse
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

def index(request):
    """ display the stream which is on the first page after success login of the user """
    # template = loader.get_template('base_app/index.html')
    reviews = mod.Review.objects.filter().order_by('-time_created')
    tickets = mod.Ticket.objects.filter().order_by('-time_created')
    # reviews = get_users_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    # tickets = get_users_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {'posts': posts}

    return render(request, 'base_app/flux.html', context=context)

def home(request):
    context = {}
    return render(request, 'base_app/home.html', context=context)