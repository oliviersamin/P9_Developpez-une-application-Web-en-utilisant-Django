"""
create a function with boolean result to know if the ticket has a review or not
create a function with boolean result to know if the user is legitimate or not
"""

def _has_review(ticket_id, reviews):
    for review in reviews:
        if ticket_id == review.ticket.pk:
            return True
    return False
