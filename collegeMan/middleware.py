class SwitchAppMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get('is_student'):
            request.urlconf = 'student.urls'
        elif request.session.get('is_faculty'):
            request.urlconf = 'faculty.urls'
        else:
            request.urlconf = 'main.urls'
        response = self.get_response(request)
        return response
