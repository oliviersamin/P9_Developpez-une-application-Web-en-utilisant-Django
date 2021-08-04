from django.shortcuts import render, redirect
from . import models as mod
from django.db.models import CharField, Value
from itertools import chain
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreateTicket, CreateReview
# from . import filter_viewable_posts as fv
from . import validation_forms as vf
# import os


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


def home(request):
    context = {}
    return render(request, 'base_app/home.html', context=context)


def creation_ticket(request):
    if (request.method == "POST"):
        form = CreateTicket(request.POST, request.FILES)
        if vf.method_post_ticket_form(request):
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
        if vf.method_post_review_without_ticket_froms(request):
            return redirect('feed/')
        else:
            print('at least one of the two forms is not valid!!!!')
            form_ticket = CreateTicket()
            form_review = CreateReview()
            context = {'form_ticket': form_ticket, 'form_review': form_review}
            return render(request, 'base_app/creation_critic.html', context=context)
    else:
        print('dans else VIEWS')
        form_ticket = CreateTicket()
        print('FORM TICKET:\n', form_ticket)
        form_review = CreateReview()
        print('FORM REVIEW:\n', form_review)
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


def my_posts(request):
    reviews = mod.Review.objects.filter(user=request.user).order_by('-time_created')
    tickets = mod.Ticket.objects.filter(user=request.user).order_by('-time_created')
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {'posts': posts}
    # return render(request, 'base_app/test.html', context=context)
    return render(request, 'base_app/my_posts.html', context=context)


def create_review_from_ticket(request, ticket_id):
    ticket = mod.Ticket.objects.filter(pk=ticket_id)[0]
    if (request.method == "POST"):
        if vf.method_post_review_form(request, ticket):
            return redirect('feed/')
    else:
        form_review = CreateReview()
        context = {'ticket': ticket, 'form_review': form_review}
        return render(request, 'base_app/create_review_from_ticket.html', context=context)


def modify_ticket(request, ticket_id):
    ticket = mod.Ticket.objects.filter(pk=ticket_id)[0]
    if (request.method == "POST"):
        if vf.method_post_modify_ticket_form(request, ticket):
            return redirect('feed/')
    else:
        initial = {'title': ticket.title, 'image': ticket.image, 'description': ticket.description}
        form = CreateTicket(initial=initial)
        context = {'form': form, 'current_image_name': ticket.image_path}
        return render(request, 'base_app/modify_post.html', context=context)


def modify_review(request, review_id):
    review = mod.Review.objects.filter(pk=review_id)[0]
    if (request.method == "POST"):
        if vf.method_post_modify_review_form(request, review):
            return redirect('feed/')
    else:
        initial = {'headline': review.headline, 'rating': review.rating, 'body': review.body}
        form_review = CreateReview(initial=initial)
        # context = {'ticket': ticket, 'form_review': form_review}
        context = {'review': review, 'form_review': form_review}
    return render(request, 'base_app/modify_review.html', context=context)


def delete_review(request):
    context = {}
    return render(request, 'base_app/delete_review.html', context=context)


def delete_ticket(request):
    context = {}
    return render(request, 'base_app/delete_ticket.html', context=context)


def followers(request):
    context = {}
    return render(request, 'base_app/followers.html', context=context)