"""
create a function with boolean result to know if the ticket has a review or not
create a function with boolean result to know if the user is legitimate or not
"""
from ..models import Review
from django import template


register = template.Library()

# @register.simple_tag
def has_review(ticket_id):
    reviews = Review.objects.all()
    for review in reviews:
        if ticket_id == review.ticket.pk:
            return True
    return False


register.filter('has_review', has_review)
