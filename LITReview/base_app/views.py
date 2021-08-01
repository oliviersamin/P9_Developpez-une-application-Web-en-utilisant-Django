from django.shortcuts import render, redirect
from . import models as mod
from django.db.models import CharField, Value
from itertools import chain
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreateTicket, CreateReview
from . import filter_viewable_posts as fv
# from . import resize_images as ri
import os


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


def home(request):
    context = {}
    return render(request, 'base_app/home.html', context=context)

def creation_ticket(request):
    if (request.method == "POST"):
        form = CreateTicket(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            # print(type(ticket.image), ticket.image.path)
            ticket.save()
            os.system('python base_app/resize_images.py -i {} -max_w 200'.format(ticket.image))
            return redirect('feed/')
        else:
            print('form no valid!!!!')
            return render(request, 'base_app/creation_ticket.html', context=context)
    else:
        form = CreateTicket()
        context = {'form': form}
        return render(request, 'base_app/creation_ticket.html', context=context)

def creation_critic(request):
    if (request.method == "POST"):
        form_ticket = CreateTicket(request.POST, request.FILES)
        form_review = CreateReview(request.POST)
        if form_ticket.is_valid() and form_review.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            os.system('python base_app/resize_images.py -i {} -max_w 200'.format(ticket.image))
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            # ticket.delete()
            return redirect('feed/')
        else:
            print('at least one of the two forms is not valid!!!!')
            form_ticket = CreateTicket()
            form_review = CreateReview()
            context = {'form_ticket': form_ticket, 'form_review': form_review}
            return render(request, 'base_app/creation_critic.html', context=context)
    else:
        form_ticket = CreateTicket()
        form_review = CreateReview()
        context = {'form_ticket': form_ticket, 'form_review': form_review}
        # return render(request, 'base_app/creation_ticket.html', context=context)
        return render(request, 'base_app/creation_critic.html', context=context)

def feed(request):
    """ display the stream which is on the first page after success login of the user """
    reviews = mod.Review.objects.filter().order_by('-time_created')
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
