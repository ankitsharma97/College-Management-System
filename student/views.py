from enum import auto
from .forms import StudentProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Student, Attendance
from django.contrib.auth.models import User
from django.http import HttpResponse
from faculty.models import Schedule, Department, Semester, Subject,  classTime,  Notice,SessionalMarks
from feeMan.models import Fee
from library.models import Book
from django.contrib import auth
# Create your views here.
@login_required
def Sindex(request):
    user = request.user
    student = Student.objects.get(user=user)
    return render(request, 'student/home.html', {'student': student})

@login_required
def timeTable(request):
    user = request.user
    student = Student.objects.get(user=user)
    sem = student.semester
    branch = student.branch
    schedule = Schedule.objects.filter(semester=sem, department=branch)
    schedule_dict = {}

    for s in schedule:
        if s.day in schedule_dict:
            schedule_dict[s.day].append(s)
        else:
            schedule_dict[s.day] = [s]




    subjects = Subject.objects.filter(semester=sem)
    return render(request, 'student/timeTable.html', {'schedule_dict': schedule_dict, 'subjects': subjects, 'student': student})

@login_required
def attendance(request):
    user = request.user
    student = Student.objects.get(user=user)
    attendances = Attendance.objects.filter(student=student)
    class_times = classTime.objects.all()

    
    attendance_data = {}

    for attendance in attendances:
        date_str = attendance.date.strftime("%d-%m-%Y (%A)")
        if date_str not in attendance_data:
            attendance_data[date_str] = [(2, "")] * len(class_times)  # 2 represents 'N/A', "" for subject code

        for idx, class_time in enumerate(class_times):
            if class_time == attendance.classTime:
                status = 1 if attendance.status else 0
                subject_code = attendance.subject.code
                attendance_data[date_str][idx] = (status, subject_code)
                
    daily_summary = []
    for date, day_data in attendance_data.items():
        total_present = sum(1 for status, _ in day_data if status == 1)
        total_classes = sum(1 for status, _ in day_data if status in [0, 1])
        percentage = (total_present / total_classes * 100) if total_classes > 0 else 0
        daily_summary.append((date, day_data, total_present, total_classes, percentage))

    context = {
        'student': student,
        'daily_summary': sorted(daily_summary),
        'class_times': class_times,
    }
    return render(request, 'student/attendance.html', context)

@login_required
def marks(request):
    user = request.user
    student = Student.objects.get(user=user)
    marks = SessionalMarks.objects.filter(student=student)

    return render(request, 'student/sessional.html', {
        'marks': marks,
        'student': student
        })

@login_required
def notice(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'student/notice.html', {'notices': notices})

@login_required
def profile(request):
    User = request.user
    student = Student.objects.get(user=User)
    return render(request, 'student/profile.html', {'student': student})

@login_required
def message(request):
    return render(request, 'student/message.html')

def signUp(request):
    semesters = Semester.objects.all()
    branches = Department.objects.all()
    error = None

    if request.method == 'POST':
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        branch_id = request.POST.get('branch')
        semester_id = request.POST.get('semester')
        mobile_no = request.POST.get('mobile_no')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('confirm_password')

        if Student.objects.filter(email=email).exists():
            error = 'Email already exists'
        elif Student.objects.filter(roll_no=roll_no).exists():
            error = 'Student already exists'
        elif password != password_confirm:
            error = 'Passwords do not match'

        if error is None:

            branch = Department.objects.get(id=branch_id)
            semester = Semester.objects.get(id=semester_id)

            user = User.objects.create_user(username=email, email=email, password=password)

            Student.objects.create(
                name=name,
                roll_no=roll_no,
                branch=branch,
                semester=semester,
                mobile_no=mobile_no,
                email=email,
                user=user  # Link the student with the user
            )
            auth.login(request, user)
            return redirect('student:Sindex')  # Replace with the actual URL name for success redirection

    return render(request, 'student/signup.html', {
        'semesters': semesters,
        'branches': branches,
        'error': error,
    })
 
@login_required
def editProfile(request):
    student = Student.objects.get(user=request.user)
    form = StudentProfileForm(instance=student)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student:profile')
    return render(request, 'student/editProfile.html', {'form': form})
 
@login_required
def fee(request):
    user = request.user
    student = Student.objects.get(user=user)
    fees = Fee.objects.filter(student=student)
    return render(request, 'student/fee.html', {'fees': fees})  

@login_required
def yourBooks(request):
    user = request.user
    student = Student.objects.get(user=user)
    books = Book.objects.filter(user=student)
    return render(request, 'student/yourBooks.html', {'books': books})

@login_required
def yourSemesterBooks(request):
    user = request.user
    student = Student.objects.get(user=user)
    all_books = Book.objects.filter(semester=student.semester, department=student.branch)
    
    seen_titles = set()
    unique_books = []
    
    for book in all_books:
        if book.title not in seen_titles:
            seen_titles.add(book.title)
            unique_books.append(book)
    
    return render(request, 'student/yourSemesterBooks.html', {'books': unique_books})

@login_required
def searchBook(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'student/searchBook.html', {'books': books, 'query': query})
    
 
 
def createStudent(request):
    # names = [
    #     "Aakash Kumar", "Abhay Singh", "Abhay Yadav", "Abhishek Mishra", "Adarsh Kashyap", "Adarsh Shukla",
    #     "Aditya Kumar BRANCH-IT", "Aditya Singh", "Akash Kumar", "Aman kushwaha", "Aman Singh Yadav",
    #     "Amit Kumar Chaudahri", "Ankit Sharma", "Anurag Yadav", "Arpit Patel", "Arun", "Ashish Kumar",
    #     "Ashok kumar", "Astha Chakravarti", "Baishnvi goswami", "Baliram Singh", "Chetan Gautam",
    #     "Deepak Kumar", "Divyansh vishwakarma", "Diya Sharma", "Gourav kumar", "Hari Om Srivastav",
    #     "JITENDRA KUMAR", "Kajal Saini", "Kisan sonkar", "Kritika Pandey", "KUMAR GAURAV", "Lavkesh Kumar",
    #     "Manish Kumar", "Mohammed Aqib", "Mohit Verma", "Naveen Kumar", "Navneet pratap", "Nitin Mishra",
    #     "Piyush Rathour", "Pooja Kumari", "Pratikanshamishra", "Priyanshu Rai", "Priyanshu Tripathi",
    #     "Rajat Shaily", "Rajeev Rajesh", "Rajshree Gautam", "Ranjeet kumar", "Rishabh singh", "Rohit kumar",
    #     "Sachin Gond", "SACHIN MAURYA", "SANDEEP YADAV", "Saumya Singh", "Shashank Singh", "Shivani Chauhan",
    #     "Shivanshu Singh", "Shubham Kumar", "Sumit Giri", "Suraj kumar", "Susheel Kumar", "UTKARSH KUMAR",
    #     "Vaishnavi mishra", "Vishal Kumar", "Vishnu modanval", "Anurag Chaudhary", "Sant Kumar", "Vikas Pratap",
    #     "Rishabh bharti", "Praveen Sharma", "Mahima Sahu", "Raju Prasad"
    # ]

    # registration_numbers = [
    #     "2207360130001", "2207360130002", "2207360130003", "2207360130004", "2207360130005", "2207360130006",
    #     "2207360130007", "2207360130008", "2207360130009", "2207360130010", "2207360130011", "2207360130012",
    #     "2207360130013", "2207360130014", "2207360130015", "2207360130016", "2207360130017", "2207360130018",
    #     "2207360130019", "2207360130020", "2207360130021", "2207360130022", "2207360130023", "2207360130024",
    #     "2207360130025", "2207360130026", "2207360130027", "2207360130028", "2207360130029", "2207360130030",
    #     "2207360130031", "2207360130032", "2207360130033", "2207360130034", "2207360130035", "2207360130036",
    #     "2207360130037", "2207360130038", "2207360130039", "2207360130040", "2207360130041", "2207360130042",
    #     "2207360130043", "2207360130044", "2207360130045", "2207360130046", "2207360130047", "2207360130048",
    #     "2207360130049", "2207360130050", "2207360130051", "2207360130052", "2207360130053", "2207360130054",
    #     "2207360130055", "2207360130056", "2207360130057", "2207360130058", "2207360130060", "2207360130061",
    #     "2207360130062", "2207360130063", "2207360130064", "2207360130065", "2207360130066", "Y2113036",
    #     "Y2313901", "Y2313902", "Y2313903", "Y2313904", "Y2313905", "Y2313906"
    # ]

    # abc_ids = [
    #     "252710580852", "287-174-600-308", "368-382-011-317", "347-034-033-791", "946976618873", "767664736421",
    #     "336714316445", "999698615740", "896-159-661-061", "925864188012", "956-183-042-276", "201337457931",
    #     "484750498698", "841158153084", "974885769185", "183-660-432-136", "706843262561", "957-509-798-527",
    #     "978452121193", "655-627-545-913", "457-028-587-448", "866-138-528-329", "120-787-508-531", "179-132-480-479",
    #     "358685998632", "970-755-359-050", "750-489-485-521", "467355870064", "142924830301", "121227154170",
    #     "322403753179", "166555722859", "489-784-114-696", "911-809-878-457", "188-877-604-123", "243153227504",
    #     "423-345-155-322", "718287075302", "544303623867", "349856533912", "417705549963", "918530779050",
    #     "718154247369", "943-451-027-192", "374-419-558-102", "565952758773", "537614281394", "871-013-011-712",
    #     "149006720460", "259590023361", "285-243-694-736", "117424499268", "705057384313", "286-118-733-130",
    #     "746086270931", "188236668895", "475377293385", "273081016011", "268169479726", "829-077-554-802",
    #     "740834628198", "619-671-477-644", "403060291476", "267-198-330-642", "795-631-065-947", "889071681258",
    #     "969411857392", "458082298427", "527-069-824-624", "179488076632", "681803584111", "716268257054"
    # ]
    
    # email_password_list = [
    #     {"email": "aakash.reca@gmail.com", "password": "Aakash0130"},
    #     {"email": "abhay.reca@gmail.com", "password": "Abhay0003"},
    #     {"email": "abhay1.reca@gmail.com", "password": "Abhay0004"},
    #     {"email": "abhishek.reca@gmail.com", "password": "Abhishek0005"},
    #     {"email": "adarsh.reca@gmail.com", "password": "Adarsh0006"},
    #     {"email": "adarsh1.reca@gmail.com", "password": "Adarsh0007"},
    #     {"email": "aditya.reca@gmail.com", "password": "Aditya0008"},
    #     {"email": "aditya1.reca@gmail.com", "password": "Aditya0009"},
    #     {"email": "akash.reca@gmail.com", "password": "Akash0010"},
    #     {"email": "aman.reca@gmail.com", "password": "Aman0011"},
    #     {"email": "aman1.reca@gmail.com", "password": "Aman0012"},
    #     {"email": "amit.reca@gmail.com", "password": "Amit0013"},
    #     {"email": "ankit.reca@gmail.com", "password": "Ankit0014"},
    #     {"email": "anurag.reca@gmail.com", "password": "Anurag0015"},
    #     {"email": "arpit.reca@gmail.com", "password": "Arpit0016"},
    #     {"email": "arun.reca@gmail.com", "password": "Arun0017"},
    #     {"email": "ashish.reca@gmail.com", "password": "Ashish0018"},
    #     {"email": "ashok.reca@gmail.com", "password": "Ashok0019"},
    #     {"email": "astha.reca@gmail.com", "password": "Astha0020"},
    #     {"email": "baishnvi.reca@gmail.com", "password": "Baishnvi0021"},
    #     {"email": "baliram.reca@gmail.com", "password": "Baliram0022"},
    #     {"email": "chetan.reca@gmail.com", "password": "Chetan0023"},
    #     {"email": "deepak.reca@gmail.com", "password": "Deepak0024"},
    #     {"email": "divyansh.reca@gmail.com", "password": "Divyansh0025"},
    #     {"email": "diya.reca@gmail.com", "password": "Diya0026"},
    #     {"email": "gourav.reca@gmail.com", "password": "Gourav0027"},
    #     {"email": "hari.reca@gmail.com", "password": "Hari0028"},
    #     {"email": "jitendra.reca@gmail.com", "password": "Jitendra0029"},
    #     {"email": "kajal.reca@gmail.com", "password": "Kajal0030"},
    #     {"email": "kisan.reca@gmail.com", "password": "Kisan0031"},
    #     {"email": "kritika.reca@gmail.com", "password": "Kritika0032"},
    #     {"email": "kumar.reca@gmail.com", "password": "Kumar0033"},
    #     {"email": "lavkesh.reca@gmail.com", "password": "Lavkesh0034"},
    #     {"email": "manish.reca@gmail.com", "password": "Manish0035"},
    #     {"email": "mohammed.reca@gmail.com", "password": "Mohammed0036"},
    #     {"email": "mohit.reca@gmail.com", "password": "Mohit0037"},
    #     {"email": "naveen.reca@gmail.com", "password": "Naveen0038"},
    #     {"email": "navneet.reca@gmail.com", "password": "Navneet0039"},
    #     {"email": "nitin.reca@gmail.com", "password": "Nitin0040"},
    #     {"email": "piyush.reca@gmail.com", "password": "Piyush0041"},
    #     {"email": "pooja.reca@gmail.com", "password": "Pooja0042"},
    #     {"email": "pratikanshamishra.reca@gmail.com", "password": "Pratikanshamishra0043"},
    #     {"email": "priyanshu.reca@gmail.com", "password": "Priyanshu0044"},
    #     {"email": "priyanshu1.reca@gmail.com", "password": "Priyanshu0045"},
    #     {"email": "rajat.reca@gmail.com", "password": "Rajat0046"},
    #     {"email": "rajeev.reca@gmail.com", "password": "Rajeev0047"},
    #     {"email": "rajshree.reca@gmail.com", "password": "Rajshree0048"},
    #     {"email": "ranjeet.reca@gmail.com", "password": "Ranjeet0049"},
    #     {"email": "rishabh.reca@gmail.com", "password": "Rishabh0050"},
    #     {"email": "rohit.reca@gmail.com", "password": "Rohit0051"},
    #     {"email": "sachin.reca@gmail.com", "password": "Sachin0052"},
    #     {"email": "sachin1.reca@gmail.com", "password": "Sachin0053"},
    #     {"email": "sandeep.reca@gmail.com", "password": "Sandeep0054"},
    #     {"email": "saumya.reca@gmail.com", "password": "Saumya0055"},
    #     {"email": "shashank.reca@gmail.com", "password": "Shashank0056"},
    #     {"email": "shivani.reca@gmail.com", "password": "Shivani0057"},
    #     {"email": "shivanshu.reca@gmail.com", "password": "Shivanshu0058"},
    #     {"email": "shubham.reca@gmail.com", "password": "Shubham0060"},
    #     {"email": "sumit.reca@gmail.com", "password": "Sumit0061"},
    #     {"email": "suraj.reca@gmail.com", "password": "Suraj0062"},
    #     {"email": "susheel.reca@gmail.com", "password": "Susheel0063"},
    #     {"email": "utkarsh.reca@gmail.com", "password": "Utkarsh0064"},
    #     {"email": "vaishnavi.reca@gmail.com", "password": "Vaishnavi0065"},
    #     {"email": "vishal.reca@gmail.com", "password": "Vishal0066"},
    #     {"email": "vishnu.reca@gmail.com", "password": "Vishnu3901"},
    #     {"email": "anurag1.reca@gmail.com", "password": "Anurag3902"},
    #     {"email": "sant.reca@gmail.com", "password": "Sant3903"},
    #     {"email": "vikas.reca@gmail.com", "password": "Vikas3904"},
    #     {"email": "rishabh1.reca@gmail.com", "password": "Rishabh3905"},
    #     {"email": "praveen.reca@gmail.com", "password": "Praveen3906"},
    #     {"email": "mahima.reca@gmail.com", "password": "Mahima3907"},
    #     {"email": "raju.reca@gmail.com", "password": "Raju3908"}
    # ]
    # i = 0
    # for user_data in email_password_list:
    #     email = user_data["email"]
    #     password = user_data["password"]
    #     user = User.objects.create_user(
    #         username=email,
    #         email=email,
    #         password=password
    #         )
    #     Student.objects.create(
    #         user=user, 
    #         roll_no=registration_numbers[i],
    #         abc_id = abc_ids[i],
    #         name=names[i]
    #         )
    #     i+=1
        
    return HttpResponse("Students created successfully")


        
        