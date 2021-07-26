from . import models as mod

def get_viewable_tickets(request):
    """ return tickets from user, or from anyone following user or anyone that user follows """
    # filter = [mod.UserFollows.user, mod.UserFollows.followed_user, mod.Ticket.user]
    # followed_by_user = mod.UserFollows.objects.filter(user=request.user)
    # print(followed_by_user)
    # filter_following = []
    # for item in followed_by_user:
    #     filter_following.append(item.user)
    print('dans get_viewable_posts: ', request)
    # filter = mod.Ticket.objects.filter(user=request.user)
    # return filter