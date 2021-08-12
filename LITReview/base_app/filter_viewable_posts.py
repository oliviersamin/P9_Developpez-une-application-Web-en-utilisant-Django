from . import models as mod
from django.db.models import CharField, Value


def get_viewable_posts(request):
    """ return tickets from user, or from anyone following user or anyone that user follows """
    users = [request.user]
    user_is_following = mod.UserFollows.objects.filter(user=request.user)
    user_is_followed_by = mod.UserFollows.objects.filter(followed_user=request.user)
    for user in user_is_following:
        users.append(user.followed_user)
    for user in user_is_followed_by:
        users.append(user.user)
    users = list(set(users))
    reviews = mod.Review.objects.none()
    tickets = mod.Ticket.objects.none()

    for user in users:
        review = mod.Review.objects.filter(user=user)
        ticket = mod.Ticket.objects.filter(user=user)
        review = review.annotate(content_type=Value('REVIEW', CharField()))
        ticket = ticket.annotate(content_type=Value('TICKET', CharField()))
        reviews = reviews.union(review)
        tickets = tickets.union(ticket)
    return reviews, tickets
