from django.shortcuts import redirect, render
from student.models import Student
from faculty.models import Employee
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/index.html')


def login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if role == 'student':
                try:
                    student = Student.objects.get(user=user)
                    request.session['role'] = 'student'
                    request.session['name'] = student.name
                    
                    auth_login(request, user)
                    return redirect('student:Sindex')
                except Student.DoesNotExist:
                    error = 'Invalid Role for the provided credentials'
            elif role == 'faculty':
                try:
                    faculty = Employee.objects.get(user=user)
                    request.session['role'] = 'faculty'
                    request.session['type'] = faculty.role.name
                    request.session['name'] = faculty.name
                    auth_login(request, user)
                    return redirect('faculty:Findex')
                except Employee.DoesNotExist:
                    error = 'Invalid Role for the provided credentials'
            else:
                error = 'Invalid role selected'
        else:
            error = 'Invalid email or password'
    
    return render(request, 'main/login.html', {'error': error})


def logout(request):
    auth_logout(request)
    return redirect('main:index')

@login_required
def changePass(request):
    user  = request.user 
    print(user.username)
    error = None
    if request.method == "POST":
        password = request.POST.get('password')
        npassword = request.POST.get('npassword')
        if not user.check_password(password):
            error = 'Invalid Password'
        if password == npassword:
            error = 'New Password is as old password'
        if error is None:
            user.set_password(npassword)
            if user.is_authenticated:
                auth_logout(request)
            return redirect('main:login')
    return render(request, 'main/updatePass.html', {
        'user': user,
        'error':error
        
        })