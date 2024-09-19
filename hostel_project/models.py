from django.db import models

class LoginTable(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user_name

class Department(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='department_images/')
    
    def __str__(self):
        return self.name
    
class Course(models.Model):
    DEPARTMENT = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()

    
    def __str__(self):
        return self.course_name
    
    
class Hostel(models.Model):
    COURSE = models.ManyToManyField(Course, related_name='hostels')
    name = models.CharField(max_length=100)
    number = models.BigIntegerField()
    details = models.CharField(max_length=300)
    image = models.ImageField(upload_to='hostel_images/')
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class Warden(models.Model):
    LOGIN = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    HOSTEL = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=30)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=300)
    image = models.ImageField(upload_to='warden_images/')
    
    def __str__(self):
        return self.name
   
# Student nne add akkumbo hostel number koode add akkanm
class Student(models.Model):
    LOGIN = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.BigIntegerField()
    address = models.CharField(max_length=200)
    dob = models.DateField()
    year = models.CharField(max_length=10)
    image = models.ImageField(upload_to='student_images/')
    admission_number = models.CharField(max_length=30)
    parent_phone_number = models.BigIntegerField()
    date_of_joining = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    
class Room(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    HOSTEL = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.BigIntegerField()
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='room_images/') 
    
    def __str__(self):
        return f'Room {self.room_number} - {self.HOSTEL.name}'

 
class Tutor(models.Model):
    LOGIN = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    year = models.IntegerField()
    phone_number = models.BigIntegerField()
    image = models.ImageField(upload_to='tutor_images/')
    
    def __str__(self):
        return self.name

class Parent(models.Model):
    LOGIN = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone_number = models.BigIntegerField()
    
    def __str__(self):
        return self.name
    
class LateComer(models.Model):
    ROOM = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.STUDENT.name} - {self.date}'


class LocalMovement(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    exit_time = models.TimeField()
    entry_time = models.TimeField()
    date = models.DateField(auto_now_add=True)
    reason = models.CharField(max_length=300)
    
    def __str__(self):
        return f'{self.STUDENT.name} - {self.date}'

class LeavingRegister(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    TUTOR = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.CharField(max_length=500)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.STUDENT.name} - {self.start_date} to {self.end_date}'

class Payment(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Pending')
    screenshot = models.ImageField(upload_to='payment_screenshots/')
    is_requested = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.STUDENT.name} - {self.amount}'

class Complaint(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=500)
    reply = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='complaints/')
    replied_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.STUDENT.name} - {self.date}'
    
class Notification(models.Model):
    notification = models.CharField(max_length=400)
    notification_date = models.DateField(auto_now_add=True)
    user_type = models.CharField(max_length=20)
    
    def __str__(self):
        return self.notification
    
