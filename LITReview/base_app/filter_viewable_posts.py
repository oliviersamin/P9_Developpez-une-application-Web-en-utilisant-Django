from . import models as mod
from django.db.models import Q

def get_user_viewable_tickets(request):
    """ return tickets from user, or from anyone following user or anyone that user follows """
    # filter = [mod.UserFollows.user, mod.UserFollows.followed_user, mod.Ticket.user]

    tickets = mod.Ticket.objects.filter(Q(user=request.user) | Q()).order_by('-time_created')

    return tickets