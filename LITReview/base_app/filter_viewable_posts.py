from . import models as mod

def get_viewable_tickets(user_test):
    """ return tickets from user, or from anyone following user or anyone that user follows """
    # filter = [mod.UserFollows.user, mod.UserFollows.followed_user, mod.Ticket.user]
    # followed_by_user = mod.UserFollows.objects.filter(user=request.user)
    # print(followed_by_user)
    # filter_following = []
    # for item in followed_by_user:
    #     filter_following.append(item.user)
    # print('dans get_viewable_posts: ', request)
    results = mod.Ticket.objects.filter()
    return results