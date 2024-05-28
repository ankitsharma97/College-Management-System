from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from faculty.models import Department, Employee, Notice, Role, Semester
from feeMan.models import Fee, FeeType, feeStructure
from student.models import Student
from faculty.decorators import account_required
# Create your views here.

@account_required
def Aindex(request):
    return render(request, 'feeMan/index.html')

@account_required
def profile(request):
    User = request.user
    faculty = Employee.objects.get(user=User)
    subjects = None
    return render(request, 'feeMan/profile.html', {
        'faculty': faculty,
        'subjects': subjects
        })

@account_required
def editProfile(request):
    messages = []
    user = request.user
    faculty = Employee.objects.get(user=user)

    if request.method == 'POST':
        faculty.department = Department.objects.get(name=request.POST.get('department', faculty.department.id))
        faculty.email = request.POST.get('email', faculty.email)
        faculty.mobile_no = request.POST.get('mobile_no', faculty.mobile_no)
        faculty.father_name = request.POST.get('father_name', faculty.father_name)
        faculty.mother_name = request.POST.get('mother_name', faculty.mother_name)
        faculty.dob = request.POST.get('dob', faculty.dob)
        faculty.joining_date = request.POST.get('joining_date', faculty.joining_date)

        faculty.save()
        messages = ['Profile updated successfully!']

    return render(request, 'feeMan/editProfile.html', {
        'messages': messages,
        'faculty': faculty
    })
    
@account_required 
def addFee(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id) if fee_id != 0 else Fee()
    error = None

    if request.method == 'POST':
        student_roll_no = request.POST.get('student')
        student = Student.objects.filter(roll_no=student_roll_no).first()

        if student:
            fee.student = student
            fee.transaction_id = request.POST.get('transaction_id')
            fee.payable = FeeType.objects.get(id=request.POST.get('payable'))
            fee.req_amount = feeStructure.objects.get(
                semester=student.semester,
                department=student.branch,
                fee_type=fee.payable
            )
            fee.amount = float(request.POST.get('amount'))
            fee.dues = fee.req_amount.amount - fee.amount
            fee.status = fee.dues <= 0
            fee.date = request.POST.get('date')
            fee.save()
            return redirect(reverse('feeMan:viewFee'))
        else:
            error = 'Student does not exist'

    fee_types = FeeType.objects.all()
    fee_structures = feeStructure.objects.all()

    return render(request, 'feeMan/addFee.html', {
        'fee': fee,
        'fee_types': fee_types,
        'fee_structures': fee_structures,
        'error': error,
    })
    
@account_required
def viewFee(request):
    semesters = Semester.objects.all()
    departments = Department.objects.all()
    fees = Fee.objects.all()
    if 'semester' in request.GET:
        if request.GET['semester'] == '0':
            fees = fees
        else:
            fees = fees.filter(student__semester=request.GET['semester'])
    if 'department' in request.GET:
        if request.GET['department'] == '0':
            fees = fees
        else:
            fees = fees.filter(student__branch=request.GET['department'])
        
        
    context = {
        'fees': fees,
        'semesters': semesters,
        'departments': departments,
    }
        
    return render(request, 'feeMan/viewFee.html', context)
    
@account_required
def searchFee(request):
    query = request.GET.get('q', '')
    fees = Fee.objects.filter(student__roll_no__icontains=query)
    return render(request, 'feeMan/search.html', {'fees': fees, 'query': query})

@account_required
def notice(request):
    roles = Role.objects.all()
    faculties = Employee.objects.all()
    branches = Department.objects.all()
    user = request.user
    faculty = Employee.objects.get(user=user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        role_id = faculty.role.id
        branch_id = faculty.department.id
        faculty_id = request.POST.get('faculty')

        role = Role.objects.get(id=role_id)
        branch = Department.objects.get(id=branch_id)

        notice = Notice.objects.create(
            Title=title,
            Description=description,
            who=role,
            category=branch,
            by=faculty
        )
        return redirect(reverse('feeMan:viewNotice'))


    return render(request, 'feeMan/Addnotice.html', {
        'roles': roles,
        'faculties': faculties,
        'branches': branches
    })
    
def viewNotice(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'feeMan/ViewNotice.html', {'notices': notices})