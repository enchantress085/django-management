from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(requests, *args, **kwargs):
        if requests.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(requests, *args, **kwargs)

    return wrapper_func 


def allowed_user(allowed_roles):
    def decorator(view_func):
        def wrapper_func(requests, *args, **kwargs):
            group = None
            if requests.user.groups.exists():
                group = requests.user.groups.all()[0].name 

            if group in allowed_roles:
                return view_func(requests, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to this view')
        return wrapper_func
    return decorator


def admin_only(view_func):
	def wrapper_function(requests, *args, **kwargs):
		group = None
		if requests.user.groups.exists():
			group = requests.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')

		if group == 'admin':
			return view_func(requests, *args, **kwargs)

	return wrapper_function
