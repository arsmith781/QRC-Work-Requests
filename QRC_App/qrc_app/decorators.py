from django.http import HttpResponse
from django.shortcuts import redirect


# decorator for views function requiring a login
def allowed_users(allowed_roles=[]):
    # pass in the function we're wrapping
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # debug statement
            print('Role(s)', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You can't view this page")
        return wrapper_func
    return decorator

