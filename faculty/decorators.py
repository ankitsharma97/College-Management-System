from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def faculty_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('role') == 'faculty':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('main:login')  # Use the correct URL name for your login view
    return _wrapped_view

