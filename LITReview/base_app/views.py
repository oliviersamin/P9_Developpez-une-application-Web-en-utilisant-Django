from django.shortcuts import render, redirect
from . import models as mod
from django.db.models import CharField, Value
from itertools import chain
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import CreateTicket, CreateReview, SearchForm
from .filter_viewable_posts import get_viewable_posts
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class CreationTicketForm(View):
    """ create a new ticket from the feed or my_posts pages """
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


class SearchFollowerForm(View):
    """ class used to add if possible a new user to follow using the search form """
    form = SearchForm
    template_name = 'base_app/add_follower.html'

    def get(self, request):
        """ 3 cases are possibles when the form is sent:
          1 - the user entered does not exist and cannot be followed
          2 - the user exists but is already followed by the user
          3 - the user exists and is not yet followed by the user"""

        user_to_follow = ''
        form_follower = SearchForm(request.GET)
        if form_follower.is_valid():
            try:
                user_to_follow = User.objects.filter(username=request.GET.get('username'))[0]
            except:
                message = "L'utilisateur " + request.GET.get('username') + " n'existe pas"
                context = {'message': message}
                return render(request, self.template_name, context=context)
            user_is_following = mod.UserFollows.objects.filter(user=request.user)
            for user in user_is_following:
                if user.followed_user == user_to_follow:
                    message = 'Vous suivez déjà ' + user.followed_user.username
                    context = {'message': message}
                    return render(request, self.template_name, context=context)
            follower = mod.UserFollows()
            follower.user = self.request.user
            follower.followed_user = user_to_follow
            follower.save()
            message = 'Vous suivez maintenant ' + request.GET.get('username')
            context = {'message': message}
            return render(request, self.template_name, context=context)


class CreationCriticForm(View):
    """ class used to create a new critic from the feed or my_posts pages  """
    form = CreateTicket
    template_name = 'base_app/creation_critic.html'

    def get(self, request):
        form_ticket = CreateTicket()
        form_review = CreateReview()
        context = {'form_ticket': form_ticket, 'form_review': form_review}
        return render(request, self.template_name, context=context)

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
    """ class used to find and display the users followed by the user connected
     and to find and display the users that are following the user connected"""

    model = mod.UserFollows
    context_object_name = 'users'
    template_name = 'base_app/followers.html'

    def get_queryset(self):
        following = []
        followed_by = []
        user_is_following = mod.UserFollows.objects.filter(user=self.request.user)
        user_is_followed_by = mod.UserFollows.objects.filter(followed_user=self.request.user)
        for user in user_is_following:
            following.append(user)
        for user in user_is_followed_by:
            followed_by.append(user)
        return {'I_follow': following, 'that_follow_me': followed_by, 'buttons': False}


def home(request):
    """ display the home page with the signup and login buttons """
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
    """ display the tickets and reviews of the connected user only """
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
    """ use an existing ticket to create a new review of it """
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
    """ use the existing ticket to display and modify it """
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
    """ use an existing review to display and modify it if the user asking for the modification is
     the user that created the review"""
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


def ask_delete_review(request, review_id):
    """ ask for a confirmation before deleting the review """
    context = {'review_id': review_id}
    return render(request, 'base_app/ask_delete_review.html', context=context)


def delete_review(request, review_id):
    """ if the user asking for the deletion is the user that created the review then it is deleted """
    review = mod.Review.objects.get(pk=review_id)
    if review.user == request.user:
        review.delete()
        message = "Votre critique a été supprimée"
    else:
        message = "Vous n'êtes pas autorisé à supprimer cette critique"
    context = {'review_id': review_id, 'message': message}
    return render(request, 'base_app/delete_review.html', context=context)


def ask_delete_ticket(request, ticket_id):
    """ ask for a confirmation before deleting the ticket """
    context = {'ticket_id': ticket_id}
    return render(request, 'base_app/ask_delete_ticket.html', context=context)


def delete_ticket(request, ticket_id):
    """ if the user asking for the deletion is the user that created the review then it is deleted """
    ticket = mod.Ticket.objects.get(pk=ticket_id)
    if ticket.user == request.user:
        ticket.delete()
        message = "Votre ticket a été supprimé"
    else:
        message = "Vous n'êtes pas autorisé à supprimer ce ticket"
    context = {'ticket_id': ticket_id, 'message': message}
    return render(request, 'base_app/delete_ticket.html', context=context)


def delete_follower(request, follower_id):
    """ if the user asking for deletion is the user in the follower instance
    then the user followed is deleted """
    follower = mod.UserFollows.objects.get(pk=follower_id)
    if follower.user == request.user:
        follower.delete()
        message = "Vous avez supprimé {} de vos abonnements".format(follower.followed_user)
        context = {'message': message}
    else:
        message = "Vous n'êtes pas autorisé à supprimer cet abonnement"
        context = {'message': message}
    return render(request, 'base_app/delete_follower.html', context=context)
