from django.http import Http404

def check_user_able_to_see_page(function):
    def wrapper(request,*args, **kwargs):
        if request.user.groups.filter(name='Boss').exists():
            return function(request, *args, **kwargs)
        raise Http404
    return wrapper