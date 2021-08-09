from django.shortcuts import render, redirect
from . import models as mod
from django.db.models import CharField, Value
from itertools import chain
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import CreateTicket, CreateReview
from .filter_viewable_posts import get_viewable_posts
# import os


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class CreationTicketForm(View):
    form = CreateTicket
    template_name = 'base_app/creation_ticket.html'

    def get(self, request):
        form = self.form()
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form_ticket = CreateTicket(request.POST, request.FILES)
        if form_ticket.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed/')


class CreationCriticForm(View):
    form = CreateTicket
    template_name = 'base_app/creation_critic.html'

    def get(self, request):
        form_ticket = CreateTicket()
        form_review = CreateReview()
        context = {'form_ticket': form_ticket, 'form_review': form_review}
        return render(request, 'base_app/creation_critic.html', context=context)

    def post(self, request):
        # form = self.form(request.POST, request.FILES)
        form_ticket = CreateTicket(request.POST, request.FILES)
        form_review = CreateReview(request.POST)
        if form_ticket.is_valid() and form_review.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed/')


class ListFollowers(generic.ListView):
    model = mod.UserFollows
    context_object_name = 'users'
    template_name = 'base_app/followers.html'

    def get_queryset(self):
        following = []
        followed_by = []
        user_is_following = mod.UserFollows.objects.filter(user=self.request.user)
        user_is_followed_by = mod.UserFollows.objects.filter(followed_user=self.request.user)
        for user in user_is_following:
            following.append(user.followed_user)
        for user in user_is_followed_by:
            followed_by.append(user.user)
        return {'I_follow': following, 'that_follow_me': followed_by, 'buttons': False}


def home(request):
    context = {}
    return render(request, 'base_app/home.html', context=context)


def feed(request):
    """ display the stream which is on the first page after success login of the user """
    reviews, tickets = get_viewable_posts(request)
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {'posts': posts, 'buttons': True}
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
    context = {'posts': posts, 'buttons': True}
    # return render(request, 'base_app/test.html', context=context)
    return render(request, 'base_app/my_posts.html', context=context)


def create_review_from_ticket(request, ticket_id):
    ticket = mod.Ticket.objects.get(pk=ticket_id)
    if (request.method == "POST"):
        form_review = CreateReview(request.POST)
        if form_review.is_valid():
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed/')
    else:
        form_review = CreateReview(instance=ticket)
        context = {'ticket': ticket, 'form_review': form_review}
        return render(request, 'base_app/create_review_from_ticket.html', context=context)


def modify_ticket(request, ticket_id):
    ticket = mod.Ticket.objects.get(pk=ticket_id)
    if (request.method == "POST") and (request.user == ticket.user):
        form = CreateTicket(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('feed/')
    else:
        form = CreateTicket(instance=ticket)
        context = {'form': form, 'current_image_name': ticket.image_path}
        return render(request, 'base_app/modify_post.html', context=context)


def modify_review(request, review_id):
    review = mod.Review.objects.get(pk=review_id)
    if (request.method == "POST") and (request.user == review.user):
        form_review = CreateReview(request.POST, instance=review)
        if form_review.is_valid():
            form_review.save()
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
    context = {'buttons': False}
    return render(request, 'base_app/followers.html', context=context)