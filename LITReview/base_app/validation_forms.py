import os
from .forms import CreateTicket, CreateReview


def method_post_ticket_form(request):
    form_ticket = CreateTicket(request.POST, request.FILES)
    if form_ticket.is_valid():
        ticket = form_ticket.save(commit=False)
        ticket.user = request.user
        ticket.save()
        os.system('python base_app/resize_images.py -i {} -max_w 200'.format(ticket.image))
        return True
    return False


def method_post_review_form(request, ticket):
    form_review = CreateReview(request.POST)
    if form_review.is_valid():
        review = form_review.save(commit=False)
        review.ticket = ticket
        review.user = request.user
        review.save()
        return True
    return False


def method_post_review_without_ticket_froms(request):
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
        return True
    return False


def method_post_modify_review_form(request, old_review):
    form_review = CreateReview(request.POST)
    if form_review.is_valid():
        review = form_review.save(commit=False)
        review.ticket = old_review.ticket
        review.user = request.user
        review.save()
        old_review.delete()
        return True
    return False


def method_post_modify_ticket_form(request, old_ticket):
    form_ticket = CreateTicket(request.POST, request.FILES)
    if form_ticket.is_valid():
        ticket = form_ticket.save(commit=False)
        ticket.user = request.user
        try:
            print(ticket.image.path)
            ticket.save()
            os.system('python base_app/resize_images.py -i {} -max_w 200'.format(ticket.image))
        except ValueError:
            ticket.image = old_ticket.image
            ticket.save()
        old_ticket.delete()
        return True
    return False
