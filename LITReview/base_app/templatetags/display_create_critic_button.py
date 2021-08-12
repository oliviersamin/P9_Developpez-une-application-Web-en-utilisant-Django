"""
create a function with boolean result to know if the ticket has a review or not
create a function with boolean result to know if the user is legitimate or not
"""
from ..models import Review
from django import template


register = template.Library()


def has_review(ticket_id):
    """ filter that return if the Ticket instance has a review already existing
     It is used to display a button to create a critic in the ticket.html file"""
    reviews = Review.objects.all()
    for review in reviews:
        if ticket_id == review.ticket.pk:
            return True
    return False


register.filter('has_review', has_review)
