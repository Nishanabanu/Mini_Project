from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

def logout(request):
    request.session.flush()
    return redirect('kmct_home')

def kmct_home(request):
    wardens = Warden.objects.all()

    context = {
        'wardens': wardens,
    }
    
    return render(request, 'kmct/kmct_home_page.html', context)
    
def kmct_login_page(request):
    return render(request, 'kmct/kmct_login_page.html')

def kmct_about_page(request):
    return render(request, 'kmct/kmct_about_page.html')

def kmct_gallery_page(request):
    return render(request, 'kmct/kmct_gallery_page.html')

def admin_home(request):
    return render(request, 'admin/admin_home.html')

def student_home(request):
    return HttpResponse("The page is not created, As per the scrum the page will be create")

def warden_home(request):
    return render(request, 'warden/warden_home.html')

def tutor_home(request):
    return HttpResponse("The page is not created, As per the scrum the page will be create")

def parent_home(request):
    return HttpResponse("The page is not created, As per the scrum the page will be create")


def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        
        login_fetch = LoginTable.objects.filter(user_name=user_name, password=password)
        if login_fetch.exists():
            login_objects = LoginTable.objects.get(user_name=user_name, password=password)
            request.session['lid'] = login_objects.id
            
            user_role = login_objects.role
            
            # Get the user's full name based on their role
            if user_role == 'student':
                student = Student.objects.get(LOGIN_id=request.session['lid'])
                request.session['student_name'] = student.name
            elif user_role == 'warden':
                warden = Warden.objects.get(LOGIN_id=request.session['lid'])
                request.session['warden_name'] = warden.name
            elif user_role == 'tutor':
                tutor = Tutor.objects.get(LOGIN_id=request.session['lid'])
                request.session['tutor_name'] = tutor.name
            elif user_role == 'parent':
                parent = Parent.objects.get(LOGIN_id=request.session['lid'])
                request.session['parent_name'] = parent.name

            if user_role == 'admin':
                return HttpResponse('''<script> window.location = "/admin_home";</script>''')
            elif user_role == 'warden':
                return HttpResponse('''<script> window.location = "/warden_home";</script>''')
            elif user_role == 'tutor':
                return HttpResponse('''<script> window.location = "/tutor_home";</script>''')
            elif user_role == 'parent':
                return HttpResponse('''<script> window.location = "/parent_home";</script>''')
            elif user_role == 'student':
                return HttpResponse('''<script> window.location = "/student_home";</script>''')
            elif user_role == 'pending':
                return HttpResponse('''<script>alert("Your Account is not active, Contact Warden"); window.location = "/";</script>''')
            elif user_role == 'blocked':
                return HttpResponse('''<script>alert("Your Account is Blocked, Contact Warden"); window.location = "/";</script>''')
            else:
                return HttpResponse('''<script>alert("Invalid"); window.location = "/";</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid"); window.location = "/";</script>''')
    else:
        return render(request, 'kmct/kmct_login_page.html')      

   
#---------------------------------------------------------------------------------------------------------------------------------   
# @login_required(login_url='/')    
def admin_view_hostel(request):
    assigned_hostels = Warden.objects.all()  # Hostels with assigned wardens
    # unassigned_hostels = Hostel.objects.filter(warden__isnull=True)  # Hostels without assigned wardens
    return render(request, 'admin/admin_view_hostel.html', {
        'assigned_hostels': assigned_hostels,
        # 'unassigned_hostels': unassigned_hostels
    })

# @login_required(login_url='/')    
def admin_add_hostel(request):
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        details = request.POST['address']
        status = request.POST['status']
        image = request.FILES['image']
        
        hostel = Hostel.objects.create(name=name, number=number, details=details, status=status, image=image)
        
        # Get selected courses as a list of IDs
        selected_courses = request.POST.getlist('courses')
        
        # Set the many-to-many relationship
        hostel.COURSE.set(selected_courses)
        hostel.save()

        return render(request, 'admin/admin_add_hostel.html', {'success': True})
    
    courses = Course.objects.all()
    return render(request, 'admin/admin_add_hostel.html', {'courses': courses})


# def admin_delete_hostel(request,id):
#     hostel = Hostel.objects.get(id=id)
#     hostel.delete()
#     return HttpResponse('''<script>alert("Deleted successfully");window.location="/admin_view_hostel"</script>''')

# @login_required(login_url='/')
def admin_edit_hostel(request, id):
    hostel = get_object_or_404(Hostel, id=id)

    if request.method == 'POST':
        hostel.name = request.POST.get('name')
        hostel.number = request.POST.get('number')
        hostel.details = request.POST.get('address')
        hostel.status = request.POST.get('status')

        if 'image' in request.FILES:
            hostel.image = request.FILES['image']
        
        # Update the courses accepted by this hostel
        selected_courses = request.POST.getlist('courses')
        hostel.COURSE.set(selected_courses)
        
        hostel.save()
        return render(request, 'admin/admin_edit_hostel.html', {'hostel': hostel, 'success': True, 'courses': Course.objects.all()})

    courses = Course.objects.all()
    return render(request, 'admin/admin_edit_hostel.html', {'hostel': hostel, 'courses': courses})

#--------------------------------------------------------------------------------------------------------------------------------- 
# @login_required(login_url='/')   
def admin_view_wardens(request):
    warden_details = Warden.objects.all()
    return render(request, 'admin/admin_view_wardens.html',{'warden_details':warden_details})

# @login_required(login_url='/')
def admin_add_warden(request):
    # Fetch hostels that are not assigned to any warden
    available_hostels = Hostel.objects.filter(warden__isnull=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        image = request.FILES.get('image')
        hostel_id = request.POST.get('hostel')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        # Save warden login details in the LoginTable
        warden_login_details = LoginTable.objects.create(
            user_name=user_name,
            password=password,
            role='warden'
        )
        warden_login_details.save()

        # Fetch the selected hostel object
        hostel = Hostel.objects.get(id=hostel_id)

        # Save warden profile details in the Warden model
        warden_profile_details = Warden.objects.create(
            LOGIN=warden_login_details,
            name=name,
            phone=phone,
            address=address,
            image=image,
            HOSTEL=hostel
        )
        warden_profile_details.save()

        return render(request, 'admin/admin_add_warden.html', {'success': True, 'hostels': available_hostels})
    return render(request, 'admin/admin_add_warden.html', {'hostels': available_hostels})

# @login_required(login_url='/')
def admin_edit_warden(request, id):
    warden = Warden.objects.get(id=id)
    login = warden.LOGIN
    if request.method == 'POST':
        warden.name = request.POST.get('name')
        warden.phone = request.POST.get('phone')
        warden.address = request.POST.get('address')
        login.user_name = request.POST.get('user_name')
        login.password = request.POST.get('password')
        
        if 'image' in request.FILES:
            warden.image = request.FILES['image']
        warden.save()
        login.save()
        return render(request, 'admin/admin_edit_warden.html', {'warden': warden, 'success': True})
    return render(request, 'admin/admin_edit_warden.html', {'warden': warden})

# def admin_delete_warden(request,id):
#     warden = Warden.objects.get(id=id)
#     login_id = warden.LOGIN_id
#     warden.delete()
#     LoginTable.objects.filter(id=login_id).delete()
#     return HttpResponse('''<script>alert("Deleted successfully");window.location="/admin_view_wardens"</script>''')

#---------------------------------------------------------------------------------------------------------------------------------
# @login_required(login_url='/')
def admin_view_departments(request):
    departments = Department.objects.all()
    return render(request, 'admin/admin_view_departments.html', {'departments': departments})
    
# @login_required(login_url='/')  
def admin_add_departments(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        department = Department.objects.create(
            name=name,
            image=image
        )
        department.save()
        return render(request, 'admin/admin_add_departments.html', {'success': True})
    return render(request, 'admin/admin_add_departments.html')

# @login_required(login_url='/')
def admin_edit_department(request, id):
    department = Department.objects.get(id=id)
    if request.method == 'POST':
        department.name = request.POST.get('name')
        if 'image' in request.FILES:
            department.image = request.FILES['image']
        department.save()
        return render(request, 'admin/admin_edit_department.html', {'department': department, 'success': True})
    return render(request, 'admin/admin_edit_department.html', {'department': department})


 
#---------------------------------------------------------------------------------------------------------------------------------   
# @login_required(login_url='/')    
def admin_view_courses(request):
    courses = Course.objects.all()
    return render(request, 'admin/admin_view_courses.html', {'courses': courses})

# @login_required(login_url='/')
def admin_add_course(request):
    departments = Department.objects.all() 
    if request.method == 'POST':
        department_id = request.POST.get('department')
        course_name = request.POST.get('course_name')
        course_type = request.POST.get('type')
        duration = request.POST.get('duration')
        
        department = Department.objects.get(id=department_id) 
        
        course = Course.objects.create(
            DEPARTMENT=department,
            course_name=course_name,
            type=course_type,
            duration=duration
        )
        course.save()
        return render(request, 'admin/admin_add_course.html', {'success': True, 'departments': departments})
    return render(request, 'admin/admin_add_course.html', {'departments': departments})

# @login_required(login_url='/')        
def admin_edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    departments = Department.objects.all()
    
    if request.method == 'POST':
        department_id = request.POST.get('department')
        course_name = request.POST.get('course_name')
        course_type = request.POST.get('type')
        duration = request.POST.get('duration')
        
        department = Department.objects.get(id=department_id)
        
        course.DEPARTMENT = department
        course.course_name = course_name
        course.type = course_type
        course.duration = duration
        course.save()
        
        return render(request, 'admin/admin_edit_course.html', {'course': course, 'departments': departments, 'success': True})
    return render(request, 'admin/admin_edit_course.html', {'course': course, 'departments': departments})
    
# @login_required(login_url='/')
def admin_view_tutors(request):
    tutors = Tutor.objects.all()
    return render(request, 'admin/admin_view_tutors.html', {'tutors':tutors})

# @login_required(login_url='/')   
def admin_add_tutor(request):
    if request.method == "POST":
        name = request.POST.get('tutor_name')
        id_number = request.POST.get('tutor_id')
        year = request.POST.get('year')
        phone_number = request.POST.get('tutor_phone')
        image = request.FILES.get('image')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        course_id = request.POST.get('course')

        # Create a new LoginTable entry
        tutor_login_details = LoginTable.objects.create(
            user_name=user_name,
            password=password,
            role='tutor'
        )

        # Fetch the selected course details
        course_details = Course.objects.get(id=course_id)

        # Create the Tutor profile
        Tutor.objects.create(
            LOGIN=tutor_login_details,
            COURSE=course_details,
            name=name,
            year=year,
            phone_number=phone_number,
            image=image,
            id_number=id_number
        )

        return redirect('admin_view_tutors')  # Redirect to the tutor list page after saving

    # Fetch all departments to display in the dropdown
    departments = Department.objects.all()
    return render(request, 'admin/admin_add_tutor.html', {'departments': departments})

# @login_required(login_url='/')
def get_courses(request):
    department_id = request.GET.get('department_id')
    courses = Course.objects.filter(DEPARTMENT_id=department_id).values('id', 'course_name')
    return JsonResponse(list(courses), safe=False)

# @login_required(login_url='/')   
def admin_edit_tutor(request, id):
    tutor_details = get_object_or_404(Tutor, id=id)
    departments = Department.objects.all()
    courses = Course.objects.filter(DEPARTMENT=tutor_details.COURSE.DEPARTMENT)

    if request.method == "POST":
        tutor_details.name = request.POST.get('name')
        tutor_details.id_number = request.POST.get('id_number')
        tutor_details.year = request.POST.get('year')
        tutor_details.phone_number = request.POST.get('phone_number')
        tutor_details.LOGIN.user_name = request.POST.get('user_name')
        tutor_details.LOGIN.password = request.POST.get('password')
        
        if request.FILES.get('image'):
            tutor_details.image = request.FILES['image']
        
        course_id = request.POST.get('course_id')
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            tutor_details.COURSE = selected_course
        
        tutor_details.LOGIN.save()
        tutor_details.save()
        
        return render(request, 'admin/admin_edit_tutor.html', {
            'tutor': tutor_details,
            'departments': departments,
            'courses': Course.objects.filter(DEPARTMENT=tutor_details.COURSE.DEPARTMENT),
            'success': True,
        })
    
    return render(request, 'admin/admin_edit_tutor.html', {
        'tutor': tutor_details,
        'departments': departments,
        'courses': courses,
    })

# @login_required(login_url='/')
def get_courses_by_department(request):
    department_id = request.GET.get('department_id')
    courses = Course.objects.filter(DEPARTMENT_id=department_id)
    course_list = [{'id': course.id, 'course_name': course.course_name} for course in courses]
    return JsonResponse({'courses': course_list})
    
# @login_required(login_url='/')
def admin_manage_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, "admin/admin_view_complaints.html",{"complaints":complaints})

# @login_required(login_url='/')
def admin_reply_complaint(request,id):
    complaint_object = get_object_or_404(Complaint, id=id)
    if request.method == "POST":
        reply = request.POST.get('complaint_reply')
        complaint_object.reply = reply
        complaint_object.replied_status = True
        complaint_object.save()
        return redirect('admin/admin_view_complaints.html')  # Redirect to the complaints list after replying
    return render(request, 'admin/admin_reply_complaint.html', {'complaint_object': complaint_object})
        
# @login_required(login_url='/')   
def admin_view_payments(request):
    payments = Payment.objects.all()
    return render(request, 'admin/admin_view_payments.html',{'payments':payments})

# @login_required(login_url='/')
def admin_send_payment_request(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payments = Payment.objects.filter(status='Pending')
        notification = Notification.objects.create(
            notification = "THE HOSTEL FEES PAGE IS LIVE NOW TO MAKE PAYMENTS",
            user_type = 'student'
        )
        notification.save()
        
        for payment in payments:
            payment.amount = amount 
            payment.is_requested = True
            payment.save()
        return HttpResponse('''<script>alert("Request Send Successfully");window.location="/admin_view_payments"</script>''')
    return render(request, 'admin/admin_view_payments.html')
    
# @login_required(login_url='/')
def admin_send_notification(request):
    if request.method == 'POST':
        notification_text = request.POST.get('notification')
        user_type = request.POST.get('user_type')
        
        Notification.objects.create(
            notification=notification_text,
            user_type=user_type
        )
        return HttpResponse('''<script>alert("Notification Send Successfully");window.location="/admin_home"</script>''')
    return render(request, 'admin/admin_send_notification.html')
   
# @login_required(login_url='/')        
def admin_view_students(request):
    student_details = Room.objects.filter(STUDENT__COURSE__duration__in=[1, 3])
    return render(request, 'admin/admin_view_students.html', {'student_details': student_details})

# @login_required(login_url='/')
def admin_view_alumini(request):
    alumini_details = Room.objects.filter(STUDENT__COURSE__duration__gt=3)
    return render(request, 'admin/admin_view_alumini.html', {'alumini_details': alumini_details})

#-------------------------------------------------------------------------------------------------------------------------------------

def warden_view_profile(request):
    warden_id = request.session.get('lid')
    login_objects = LoginTable.objects.get(id=warden_id)
    warden_profile = Warden.objects.get(LOGIN=login_objects)
    return render(request, 'warden/warden_view_profile.html',{'warden_profile':warden_profile})


def warden_edit_profile(request):
    warden_id = request.session.get('lid')
    if not warden_id:
        return HttpResponse('Warden ID not found in session.')

    warden = Warden.objects.get(LOGIN__id=warden_id)

    if request.method == 'POST':
        warden.name = request.POST.get('name')
        warden.phone = request.POST.get('phone')
        warden.address = request.POST.get('address')

        if 'image' in request.FILES:
            warden.image = request.FILES['image']

        warden.save()
        return HttpResponse('''<script>alert("Profile Edited");window.location="/warden_view_profile"</script>''')
    return render(request, 'warden/warden_edit_profile.html', {'warden': warden})

def warden_change_password(request):
    if request.method == "POST":
        old_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        new_username = request.POST.get('username')
        
        credentials = LoginTable.objects.filter(id=request.session['lid'], password=old_password)
        if credentials.exists():
            if new_password==confirm_password:
                new_credentials = credentials.update(password=confirm_password,user_name=new_username)        
                if new_credentials:
                    return HttpResponse('''<script>alert("User Name and Password Changed"); window.location="/warden_home";</script>''')
                else:
                    return HttpResponse('''<script>alert("Failed to change password"); window.location="/warden_change_password";</script>''')
            else:
                return HttpResponse('''<script>alert("New password and confirm password do not match"); window.location="/warden_change_password";</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid old password"); window.location="/warden_change_password";</script>''')
    return render(request, 'warden/warden_change_password.html')

def warden_verify_student(request):
    warden = get_object_or_404(Warden, LOGIN=request.session['lid'])
    hostel = warden.HOSTEL

    students = Student.objects.filter(
            COURSE__in=hostel.COURSE.all(),  # Courses accepted by the hostel
            # LOGIN__role='pending'  # Students whose login role is 'pending'
        )
    return render(request, 'warden/warden_verify_students.html', {'students': students})
    
def warden_accept_reject_student(request):
    action = request.POST['action']
    login_id = request.POST['login_id']

    login_obj = LoginTable.objects.get(id=login_id)

    if action == 'accept':
        login_obj.role = 'student'
    elif action == 'reject':
        login_obj.role = 'pending'

    login_obj.save()
    return HttpResponse(f'<script>alert("Status updated to {login_obj.role}"); window.location="/warden_verify_student";</script>')

def warden_block_unblock_student(request):
    action = request.POST['action']
    login_id = request.POST['login_id']

    login_obj = LoginTable.objects.get(id=login_id)

    if action == 'block':
        login_obj.role = 'blocked'
    elif action == 'unblock':
        login_obj.role = 'student'
    login_obj.save()
    return HttpResponse(f'<script>alert("Status updated to {login_obj.role}"); window.location="/warden_verify_student";</script>')

    








def warden_view_rooms(request):
    warden = Warden.objects.get(LOGIN_id=request.session['lid'])
    hostel = warden.HOSTEL
    room_list = Room.objects.filter(HOSTEL=hostel)
    return render(request, 'warden/warden_view_rooms.html',{'room_list':room_list})

def warden_add_new_room(request):
    warden = Warden.objects.get(LOGIN_id=request.session['lid']) 
    hostel = warden.HOSTEL 
    if request.method == "POST":
        room_number = request.POST['room_number']
        capacity = request.POST['capacity']
        image = request.FILES['image']
        
        room = Room.objects.create(
            room_number=room_number,
            capacity=capacity,
            image=image,
            HOSTEL=hostel  
        )
        room.save()
        return redirect('/warden_view_rooms')
    
    return render(request, 'warden/warden_add_new_room.html')

    
    


def student_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if LoginTable.objects.filter(user_name=username,password=password).exists():
            return HttpResponse('''<script>alert("Credentials already exists"); window.location="/";</script>''')
        student_login_details = LoginTable.objects.create(
            user_name=username,
            password=password,
            role='pending'
        )
        student_login_details.save()
        
        # Fetch the selected course
        course_id = request.POST['course']
        course_details = Course.objects.get(id=course_id)
        
        name = request.POST['name']
        number = request.POST['number']
        address = request.POST['address']
        dob = request.POST['dob']
        image = request.FILES['image']
        parent_phone_number = request.POST['parent_phone_number']
        academic_year = request.POST['academic_year']
        admission_number = request.POST['admission_number']
        
        student_details = Student.objects.create(
            LOGIN=student_login_details,
            COURSE=course_details,
            name=name,
            number=number,
            address=address,
            dob=dob,
            year=academic_year,  
            image=image,
            parent_phone_number=parent_phone_number,
            admission_number=admission_number
        )
        student_details.save()
        return HttpResponse('''<script>alert("Registration Successfully Completed"); window.location="/";</script>''')
    courses = Course.objects.all()
    return render(request, 'student/student_registration.html', {'courses': courses})

# def assign_student_to_hostel(request, student_id, hostel_id):
#     student = get_object_or_404(Student, id=student_id)
#     hostel = get_object_or_404(Hostel, id=hostel_id)
    
#     # Check if the student's course is in the hostel's accepted courses
#     if hostel.COURSES.filter(id=student.COURSE.id).exists():
#         # Proceed with the assignment
#         room = Room.objects.create(STUDENT=student, HOSTEL=hostel, room_number=1, capacity=2)
#         return HttpResponse("Student assigned to the hostel successfully.")
#     else:
#         return HttpResponse("This hostel does not accept the student's course.", status=400)