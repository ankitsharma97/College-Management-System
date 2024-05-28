from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Book, Fine
from student.models import Student
from faculty.models import Department, Employee, Notice, Role, Semester, Subject
from faculty.decorators import librarian_required
# Create your views here.
@librarian_required
def Lindex(request):
    total_books = Book.objects.count()
    issued_books = Book.objects.filter(isseued_date__isnull=False).count()
    overdue_books = 0
    total_fines =  0

    context = {
        'total_books': total_books,
        'issued_books': issued_books,
        'overdue_books': overdue_books,
        'total_fines': total_fines,
    }
    return render(request, 'library/index.html', context)

@librarian_required
def addBook(request, bookId):
    book = get_object_or_404(Book, bookId=bookId) if bookId != 0 else None
    semesters = Semester.objects.all()
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    
    
    
    if request.method == 'POST':
        book_id = int(request.POST.get('book_id'))
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        semester_id = request.POST.get('semester')
        department_id = request.POST.get('department')
        subject_id = request.POST.get('subject')
        quantity = request.POST.get('quantity')
        semester = get_object_or_404(Semester, id=semester_id)
        department = get_object_or_404(Department, id=department_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        if bookId == 0:
            for i in range(int(quantity)):
                Book.objects.create(
                    bookId=book_id,
                    title=title,
                    author=author,
                    publisher=publisher,
                    semester=semester,
                    department=department,
                    subject=subject,
                )
                book_id += 1
        else:
            book.book_id = book_id
            book.title = title
            book.author = author
            book.publisher = publisher
            book.semester = semester
            book.department = department
            book.subject = subject
            book.save()
        
        return redirect('library:viewBook')  # Adjust to your actual viewBook URL name
    
    return render(request, 'library/addBook.html', {
        'book': book,
        'semesters': semesters,
        'departments': departments,
        'subjects': subjects
    })

@librarian_required
def search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(bookId__icontains=query)
    return render(request, 'library/search.html', {'books': books, 'query': query})

@librarian_required
def viewBook(request):
    user = request.user
    faculty = Employee.objects.get(user=user)
    Role = faculty.role.name
    books = Book.objects.all()
    semesters = Semester.objects.all()
    departments = Department.objects.all()

    if 'semester' in request.GET:
        if request.GET['semester'] == '0':
            books = books
        else:
            books = books.filter(semester=request.GET['semester'])
    if 'department' in request.GET:
        if request.GET['department'] == '0':
            books = books
        else:
            books = books.filter(department=request.GET['department'])

    context = {
        'books': books,
        'semesters': semesters,
        'departments': departments,
        'Role': Role
    }
    return render(request, 'library/viewBook.html', context)

@librarian_required
def profile(request):
    User = request.user
    faculty = Employee.objects.get(user=User)
    subjects = None
    return render(request, 'library/profile.html', {
        'faculty': faculty,
        'subjects': subjects
        })
  
@librarian_required  
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

    return render(request, 'library/editProfile.html', {
        'messages': messages,
        'faculty': faculty
    })

@librarian_required
def viewFine(request):
    fines = Fine.objects.all()
    return render(request, 'library/calFine.html', {'fines': fines})

@librarian_required
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
        return redirect('library:viewNotice')


    return render(request, 'library/Addnotice.html', {
        'roles': roles,
        'faculties': faculties,
        'branches': branches
    })

@librarian_required
def deleteBook(request, bookId):
    book = Book.objects.get(bookId=bookId)
    book.delete()
    return redirect('library:viewBook')

@librarian_required
def addFine(request):
    books = Book.objects.all()
    if request.method == 'POST':
        book_id = request.POST.get('book')
        amount = request.POST.get('amount')
        fine_date = request.POST.get('fine_date')
        book = Book.objects.get(bookId=book_id)
        Fine.objects.create(
            book=book,
            amount=amount,
            fine_date=fine_date
        )
        
    return render(request, 'library/addCalFine.html', {'books': books})

@librarian_required
def issueBook(request):
    books = Book.objects.filter(isseued_date__isnull=True)
    students = Student.objects.all()
    if request.method == 'POST':
        book_id = request.POST.get('book')
        student_roll_no = request.POST.get('student')
        book = Book.objects.get(bookId=book_id)
        student = Student.objects.get(roll_no=student_roll_no)
        book.user = student
        book.isseued_date = request.POST.get('issued_date')
        book.save()
        
        return redirect('library:viewBook')
    
    return render(request, 'library/issueBook.html', {'books': books, 'students': students})

@librarian_required
def submitBook(request):
    books = Book.objects.filter(isseued_date__isnull=False)
    if request.method == 'POST':
        book_id = request.POST.get('book')
        book = Book.objects.get(bookId=book_id)
        book.user = None
        book.submit_date = request.POST.get('submit_date')
        book.save()
        
        return redirect('library:viewBook')
    
    return render(request, 'library/submitbook.html', {'books': books})

def viewNotice(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'library/ViewNotice.html', {'notices': notices})