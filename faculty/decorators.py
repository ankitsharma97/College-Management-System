from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from main.views import logout

def faculty_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') == 'faculty':
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            return redirect('main:login')  # Use the correct URL name for your login view
    return _wrapped_view

def librarian_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') == 'librarian':
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            return redirect('main:login')  # Use the correct URL name for your login view
    return _wrapped_view


def account_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') == 'account':
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            return redirect('main:login')  # Use the correct URL name for your login view
    return _wrapped_view

