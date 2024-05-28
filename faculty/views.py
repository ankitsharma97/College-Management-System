from datetime import date
from pyexpat.errors import messages
import pandas as pd
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseBadRequest
from student.models import Student, Attendance
from .decorators import faculty_required
from django.contrib.auth.models import User
from faculty.models import Semester, Department, Subject, Schedule, Employee, Role, classTime, workingDays,Notice,sessional,SessionalMarks
# Create your views here.
@faculty_required
def index(request):
    today_date = date.today()
    user = request.user
    faculty = get_object_or_404(Employee, user=user)
    today_day_name = today_date.strftime('%A')

    if today_day_name == 'Sunday':
        today_class = None  # Or handle accordingly, e.g., show a message that there are no classes
    else:
        try:
            today_day = workingDays.objects.get(day=today_day_name)
            today_class = Schedule.objects.filter(day=today_day, employee_name=faculty)
        except workingDays.DoesNotExist:
            today_class = None  # Handle case where the day is not found in workingDays

    return render(request, 'faculty/home.html', {
        'today_date': today_date,
        'today_class': today_class
    })

@faculty_required
def EditAttendance(request):
    user = request.user
    faculty = Employee.objects.get(user=user)
    semesters = Semester.objects.all()
    branches = Department.objects.all()
    subjects = Subject.objects.filter(employee_name=faculty)
    class_times = classTime.objects.all()
    students = []
    attendance_list = []
    selected_subject_id = None
    selected_class_times_id = None
    message = None
    error = None

    if request.method == 'POST':
        action = request.POST.get('action')
        selected_subject_id = request.POST.get('subject')
        selected_class_times_id = request.POST.get('class_times')

        if  selected_subject_id:
            subject = Subject.objects.get(id=selected_subject_id)
            sem = subject.semester
            branch = faculty.department
            time = classTime.objects.get(id=selected_class_times_id)
            students = Student.objects.filter(semester=sem, branch=branch)
            if request.POST.get('h') == 'Filter':
                
                subject = get_object_or_404(Subject, id=selected_subject_id)
                sem = subject.semester
                branch = faculty.department
                time = get_object_or_404(classTime, id=selected_class_times_id)
                students = Student.objects.filter(semester=sem, branch=branch)

                attendance_records_by_time = Attendance.objects.filter(
                    classTime=time,
                    date=date.today()
                )

                if not attendance_records_by_time.exists():
                    attendance_records = Attendance.objects.filter(
                        subject=subject,
                        date=date.today()
                    )

                    if not attendance_records.exists():
                        for student in students:
                            attendance = Attendance.objects.create(
                                student=student, 
                                subject=subject, 
                                Semester=sem,
                                classTime=time,
                                deparment=branch,
                                date=date.today()
                            )
                            attendance_list.append(attendance)
                    else:
                        message = "Attendance already taken for this subject."
                        attendance_list = attendance_records
                else:
                    message = "Attendance already taken for this time."
                    attendance_list = attendance_records_by_time
                        
                    
            else:    
                
                for student in students:
                    attendance = Attendance.objects.filter(student=student, subject=subject, date=date.today()).first()
                    if attendance is not None:
                        atten = request.POST.get(f"attendance_{ attendance.student.id }") 
                        if atten == 'present':
                            status = True
                        else:
                            status = False

                        if attendance is not None:
                            
                            attendance.status = status
                            attendance.save()
                        
                        attendance_list.append(attendance)  
                    else:
                        error = "first take attendance"
        else:     
            error = "Please select a subject."   


    return render(request, 'faculty/attendance.html', {
        'class_times': class_times,
        'students': students,
        'semesters': semesters,
        'branches': branches,
        'subjects': subjects,
        'selected_subject_id': selected_subject_id,
        'selected_class_times_id': selected_class_times_id,
        'attendance_list': attendance_list,
        'message': message,
        'error': error
    })

@faculty_required
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
        return redirect('faculty:viewNotice')


    return render(request, 'faculty/Addnotice.html', {
        'roles': roles,
        'faculties': faculties,
        'branches': branches
    })

@faculty_required
def sessionalMarks(request):
    user = request.user
    fac_name = Employee.objects.get(user=user)
    subjects = Subject.objects.filter(employee_name=fac_name)
    sessionlist = sessional.objects.all()  
    sessionalno = None
    students = []
    sessional_list = []
    error = None



    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        sessional_id = request.POST.get('sessional')
        marks = request.POST.get('marks')
        
        if  subject_id and sessional_id:
            subject = Subject.objects.get(id=subject_id)
            sessionalno = sessional.objects.get(id=sessional_id)
            sem = subject.semester
            dept = fac_name.department
            students = Student.objects.filter(semester=sem, branch=dept)

            if request.POST.get('h') == 'Filter':
                a = SessionalMarks.objects.filter(subject=subject, sessionalno=sessionalno)
                if not a.exists():
                    for student in students:
                        sessional_marks = SessionalMarks.objects.create(
                            sem=sem,
                            dept=dept,
                            student=student,
                            subject=subject,
                            faculty=fac_name,
                            sessionalno=sessionalno
                        )
                        sessional_list.append(sessional_marks)
                        
                else:
                    sessional_list = a  
                    
            else:
                for student in students:
                    marks = request.POST.get(f"{student.id}_marks")
                    sessional_marks = SessionalMarks.objects.filter(student=student, subject=subject, sessionalno=sessionalno).first()
                    if marks is not None:
                        sessional_marks.marks = marks
                        sessional_marks.save()
                        sessional_list.append(sessional_marks)
        else:
            error = "Please select a subject and sessional."
            
    return render(request, 'faculty/Addmarks.html', {
        'subjects': subjects,
        'sessionals': sessionlist,
        'students': students,
        'sessional_list': sessional_list,
        'sessionalno': sessionalno,
        'error': error,
        
    })


@faculty_required
def updateSchedule(request):
    user = request.user 
    faculty = Employee.objects.get(user=user)   
    semesters = Semester.objects.all()
    branche = faculty.department
    subjects = []
    faculties = []
    class_times = classTime.objects.all()
    working_days = workingDays.objects.all()
    schedules = Schedule.objects.all()
    selected_sem_id = None
    selected_branch_id = None
    schedule_list = []
    error = None

    if request.method == 'POST':
        action = request.POST.get('action')
        selected_sem_id = request.POST.get('semester')
        selected_branch_id = request.POST.get('branch')
        subjects = Subject.objects.filter(semester=selected_sem_id)
        faculties = Employee.objects.filter(department=faculty.department)

        if selected_sem_id and selected_branch_id:
            sem = Semester.objects.get(id=selected_sem_id)
            branch = Department.objects.get(id=selected_branch_id)
            if request.POST.get('h') == 'Filter':
                schedules = Schedule.objects.filter(semester=sem, department=branch)
                if not schedules.exists():
                    for i in range(1, 7):
                        for j in range(1, 8):
                            day = workingDays.objects.get(id=i)
                            time = classTime.objects.get(id=j)
                            schedule = Schedule.objects.create(
                                semester=sem,
                                department=branch,
                                day=day,
                                time=time
                            )
                            schedule_list.append(schedule)
                else:
                    schedule_list = list(schedules)
            else:
                for i in range(1, 7):
                    for j in range(1, 8):
                        key = f"{i}_{j}"
                        sub_code = request.POST.get(key)
                        day = workingDays.objects.get(id=i)
                        time = classTime.objects.get(id=j)
                        if sub_code is not None and sub_code != '':
                            subject = Subject.objects.get(id=sub_code)
                            schedules = Schedule.objects.filter(semester=sem, department=branch, day=day, time=time)
                            if schedules is not None:
                                for schedule in schedules:
                                    schedule.subject = subject
                                    schedule.employee_name = subject.employee_name
                                    schedule.save()
                                    schedule_list.append(schedule)
                            else:
                                schedule = Schedule.objects.create(
                                    semester=sem,
                                    department=branch,
                                    day=day,
                                    time=time,
                                    subject=subject,
                                    employee_name=subject.employee_name
                                )
                                schedule_list.append(schedule)
                        else:
                            schedules = Schedule.objects.filter(semester=sem, department=branch, day=day, time=time)
                            for schedule in schedules:
                                schedule.subject = None
                                schedule.employee_name = None
                                schedule.save()
                                schedule_list.append(schedule)
        else:
            error = "Please select a semester and branch."

    return render(request, 'faculty/updateschedule.html', {
        'semesters': semesters,
        'branch': branche,
        'subjects': subjects,
        'faculties': faculties,
        'class_times': class_times,
        'working_days': working_days,
        'selected_sem_id': selected_sem_id,
        'selected_branch_id': selected_branch_id,
        'schedule_list': schedule_list,
        'error': error
    })
 
@faculty_required
def addSubject(request, subId):
    user = request.user
    currFaculty = Employee.objects.get(user=user)
    subject = Subject.objects.filter(id=subId).first() if subId != 0 else None
    employees = Employee.objects.filter(department=currFaculty.department)
    semesters = Semester.objects.all()
    error = None

    if request.method == 'POST':
        selected_sem_id = request.POST.get('semester')
        code = request.POST.get('code')
        name = request.POST.get('name')
        selected_Fac_id = request.POST.get('employee_name')
        updatedFaculty = Employee.objects.get(id=selected_Fac_id)
        sub_type = request.POST.get('subject_Type')

        if selected_sem_id:
            semester = Semester.objects.get(id=selected_sem_id)
            if subId == 0:
                Subject.objects.create(
                    code=code,
                    name=name,
                    employee_name=updatedFaculty,
                    semester=semester,
                    subject_Type=sub_type,
                )
            else:
                subject.code = code
                subject.name = name
                subject.employee_name = updatedFaculty
                subject.semester = semester
                subject.subject_Type = sub_type
                subject.save()
            return redirect('faculty:editSubject')
        
        else:
            error = "Please select a semester."
    return render(request, 'faculty/addSubject.html', {
        'semesters': semesters,
        'currFaculty': currFaculty,
        'subject': subject,
        'employees': employees,
        'error': error
    })

@faculty_required
def addStudent(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    semesters = Semester.objects.all()
    branch = employee.department
    selected_sem_id = None
    message = "Excel sheet should contain columns: email, name, roll_no, registration_day."
    error = None
    if request.method == 'POST':
        selected_sem_id = request.POST.get('semester')
        if selected_sem_id:
            semester = Semester.objects.get(id=selected_sem_id)
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            
            for index, row in df.iterrows():
                email = row['email']
                name = row['name']
                roll_no = row['roll_no']
                registration_day = row['registration_day']
                if not User.objects.filter(username=email).exists():
                    user = User.objects.create_user(username=email, email=email, password=roll_no)
                    student = Student.objects.create(user=user, email=email, name=name, roll_no=roll_no, registration_day=registration_day, semester=semester, branch=branch)   
                    student.save()
                    redirect('faculty:addStudent')
                else:
                    message = name + " already exists."
                    
            return HttpResponse("Students added successfully.")
        else:
            error = "Please select a semester."
            
      
    return render(request, 'faculty/addStudent.html', {
        'semesters': semesters,
        'branch': branch,
        'message': message
    })
 
@faculty_required   
def profile(request):
    User = request.user
    faculty = Employee.objects.get(user=User)
    subjects = Subject.objects.filter(employee_name=faculty)
    return render(request, 'faculty/profile.html', {
        'faculty': faculty,
        'subjects': subjects
        })

@faculty_required   
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

    return render(request, 'faculty/editProfile.html', {
        'messages': messages,
        'faculty': faculty
    })

@faculty_required   
def editSubject(request):
    user = request.user
    faculty = Employee.objects.get(user=user)
    subjects = Subject.objects.filter(employee_name=faculty)
    Role = faculty.role
    if faculty.role.name == 'HOD':
        subjects = Subject.objects.filter(branch=faculty.department)

    return render(request, 'faculty/editSubject.html', {
        'subjects': subjects,
        'Role': Role
    })
  
@faculty_required     
def deleteSubject(request, subId):
    subject = Subject.objects.get(id=subId)
    subject.delete()
    return redirect('faculty:editSubject')

@faculty_required   
def addFaculty(request, facId):
    user = request.user
    currfaculty = Employee.objects.get(user=user)
    faculty = get_object_or_404(Employee, id=facId) if facId != 0 else None
    Roles = Role.objects.all()
    roles = []
    for role in Roles:
        if role.name != 'Director' and role.name != 'HOD':
            roles.append(role)
            
    if currfaculty.role.name == 'Director':
        roles = Roles
    
    if request.method == 'POST':
        name = request.POST.get('name')
        department = currfaculty.department  # Assuming department comes from the current faculty
        email = request.POST.get('email')
        password = request.POST.get('password')
        role_id = request.POST.get('role')
        role = get_object_or_404(Role, id=role_id)
        
        if facId == 0:
            user = User.objects.create_user(username=email, email=email, password=password)
            Employee.objects.create(
                user=user,
                name=name,
                email=email,
                department=department,
                role=role
            )
        else:
            faculty.name = name
            faculty.email = email
            faculty.department = department
            faculty.role = role
            if password:
                faculty.user.set_password(password)
            faculty.save()
        
        return redirect('faculty:editFaculty')  # Assuming you have a URL named 'faculty_list'
    
    return render(request, 'faculty/addFaculty.html', {
        'roles': roles,
        'faculty': faculty,
        'department': currfaculty.department
    })
 
@faculty_required      
def editFaculty(request):
    user = request.user
    faculty = Employee.objects.get(user=user)
    Department = faculty.department
    faculties = Employee.objects.filter(department=faculty.department)
    Role = faculty.role
    return render(request, 'faculty/editFaculty.html', {
        'faculties': faculties,
        'Role': Role,
        'Department': Department
    })

@faculty_required   
def deleteFaculty(request, facId):
    faculty = Employee.objects.get(id=facId)
    faculty.delete()
    return redirect('faculty:editFaculty')

@faculty_required   
def attendanceBySubject(request, subId):
    subject = get_object_or_404(Subject, id=subId)
    attendance_records = Attendance.objects.filter(subject=subject).select_related('student').order_by('date')

    unique_dates = sorted(set(record.date for record in attendance_records))
    students = sorted(set(record.student for record in attendance_records), key=lambda s: s.name)

    attendance_data = {student: {date: 'N/A' for date in unique_dates} for student in students}

    for record in attendance_records:
        attendance_data[record.student][record.date] = 'Present' if record.status else 'Absent'
        
    for student in students:
        total_classes = len(unique_dates)
        total_attended = sum(1 for date in unique_dates if attendance_data[student][date] == 'Present')
        attendance_data[student]['total_classes'] = total_classes
        attendance_data[student]['total_attended'] = total_attended
        attendance_data[student]['attendance_percentage'] = (total_attended / total_classes) * 100

    return render(request, 'faculty/attendance_by_subject.html', {
        'subject': subject,
        'unique_dates': unique_dates,
        'attendance_data': attendance_data,
    })

def viewNotice(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'faculty/ViewNotice.html', {'notices': notices})

def createEmployee(request):
    # teacher_emails = [
    #     "pramod.srivastava@recazamgarh.ac.in",
    #     "mahesh.vishwakarma@recazamgarh.ac.in",
    #     "tauseef.ahmad@recazamgarh.ac.in",
    #     "ashok.yadav@recazamgarh.ac.in",
    #     "manjeet.jaiswar@recazamgarh.ac.in",
    #     "sanjay.kumar@recazamgarh.ac.in",
    #     "ahmad.hasan@recazamgarh.ac.in"
    # ]
    

    # passwords = [
    #     "Pramod@BCS403",
    #     "Mahesh@BVE401",
    #     "Tauseef@BCS453",
    #     "Ashok@BCS402",
    #     "Manjeet@BCS451",
    #     "Sanjay@BCC402",
    #     "Ahmad@BAS403"
    # ]
    # teacher = [
    #     "Dr. Pramod Kumar Srivastava", 
    #     "Mr. Mahesh Kumar Vishwakarma",
    #     "Dr. Tauseef Ahmad", 
    #     "Dr. Ashok Kumar Yadav", 
    #     "Mr. Manjeet Kumar Jaiswar", 
    #     "Mr. Sanjay Kumar", 
    #     "Mr. Ahmad Hasan"
    # ]
    # for i in range(7):
    #     user = User.objects.create_user(username=teacher_emails[i], email=teacher_emails[i], password=passwords[i])
        # Employee.objects.create(
        #     user=user,
        #     name=teacher[i],
        #     email=teacher_emails[i],
        #     department=Department.objects.get(id=1),
        #     role=Role.objects.get(id=3)
        # )
    return HttpResponse("Done")

def createSubject(request):
    # aligned_data = [
    # {"subject_code": "BVE401", "subject_name": "Ethics", "teacher": "Dr. Pramod Kumar Srivastava"},
    # {"subject_code": "BCS401", "subject_name": "Operating System", "teacher": "Mr. Mahesh Kumar Vishwakarma"},
    # {"subject_code": "BCS402", "subject_name": "Theory of Automata and Formal Languages", "teacher": "Dr. Tauseef Ahmad"},
    # {"subject_code": "BCS403", "subject_name": "Object Oriented Programming with Java", "teacher": "Dr. Ashok Kumar Yadav"},
    # {"subject_code": "BCC402", "subject_name": "Python Programming", "teacher": "Mr. Manjeet Kumar Jaiswar"},
    # {"subject_code": "BCS451", "subject_name": "Operating Systems Lab", "teacher": "Mr. Sanjay Kumar"},
    # {"subject_code": "BCS452", "subject_name": "Object Oriented Programming with Java Lab", "teacher": "Mr. Ahmad Hasan"},
    # {"subject_code": "BCS453", "subject_name": "Cyber Security Workshop", "teacher": "Mr. Ahmad Hasan"},
    # {"subject_code": "BVE451", "subject_name": "Sports and Yoga-II", "teacher": "Dr. Pramod Kumar Srivastava"}  # Assuming "Dr. Pramod Kumar Srivastava" teaches this
    # ]
    
    # for data in aligned_data:
    #     subject = Subject.objects.create(
    #         code=data['subject_code'],
    #         name=data['subject_name'],
    #         employee_name=Employee.objects.get(name=data['teacher']),
    #         semester=Semester.objects.get(id=4) 
            
    #     )
    return HttpResponse("Done")
    