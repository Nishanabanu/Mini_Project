from django.urls import path
from . import views

urlpatterns = [
    path('',views.kmct_home,name='kmct_home'),
    path('kmct_login_page',views.kmct_login_page,name='kmct_login_page'),
    path('kmct_about_page',views.kmct_about_page,name='kmct_about_page'),
    path('kmct_gallery_page',views.kmct_gallery_page,name='kmct_gallery_page'),
    path('user_login',views.user_login,name='login'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('logout',views.logout,name='logout'),
    path('student_home',views.student_home,name='student_home'),
    path('warden_home',views.warden_home,name='warden_home'),
    path('tutor_home',views.tutor_home,name='tutor_home'),
    path('parent_home',views.parent_home,name='parent_home'),
    
#----------------------------------------------------------------------------------------
# Admin
path('admin_view_wardens',views.admin_view_wardens,name='admin_view_wardens'),
path('admin_add_warden',views.admin_add_warden,name='admin_add_warden'),
path('admin_view_students',views.admin_view_students,name='admin_view_students'),
path('admin_view_alumini',views.admin_view_alumini,name='admin_view_alumini'),
path('admin_edit_warden/<id>',views.admin_edit_warden,name='admin_edit_warden'),
# path('admin_delete_warden/<id>',views.admin_delete_warden,name='admin_delete_warden'),
path('admin_view_hostel',views.admin_view_hostel,name='admin_view_hostel'),
path('admin_add_hostel',views.admin_add_hostel,name='admin_add_hostel'),
# path('admin_delete_hostel/<id>',views.admin_delete_hostel,name='admin_delete_hostel'),
path('admin_edit_hostel/<id>',views.admin_edit_hostel,name='admin_edit_hostel'),
path('admin_view_departments',views.admin_view_departments,name='admin_view_departments'),
path('admin_add_departments',views.admin_add_departments,name='admin_add_departments'),
path('admin_edit_department/<id>',views.admin_edit_department,name='admin_edit_department'),
path('admin_add_course',views.admin_add_course,name='admin_add_course'),
path('admin_view_courses',views.admin_view_courses,name='admin_view_courses'),
path('admin_edit_course/<id>',views.admin_edit_course,name='admin_edit_course'),
path('admin_view_tutors',views.admin_view_tutors,name='admin_view_tutors'),
path('admin_add_tutor',views.admin_add_tutor,name='admin_add_tutor'),
path('get_courses',views.get_courses,name='get_courses'),
path('admin_edit_tutor/<id>',views.admin_edit_tutor,name='admin_edit_tutor'),
path('api/courses',views.get_courses_by_department,name='get_courses_by_department'),
path('admin_manage_complaints',views.admin_manage_complaints,name='admin_manage_complaints'),
path('admin_reply_complaint/<id>',views.admin_reply_complaint,name='admin_reply_complaint'),
path('admin_send_payment_request',views.admin_send_payment_request,name='admin_send_payment_request'),
path('admin_view_payments',views.admin_view_payments,name='admin_view_payments'),
path('admin_send_payment_request',views.admin_send_payment_request,name='admin_send_payment_request'),
path('admin_send_notification',views.admin_send_notification,name='admin_send_notification'),

#--------------------------------------------------------------------------------------------------------------------------

path('warden_view_profile',views.warden_view_profile,name='warden_view_profile'),
path('warden_edit_profile',views.warden_edit_profile,name='warden_edit_profile'),
path('warden_change_password',views.warden_change_password,name='warden_change_password'),
path('warden_verify_student',views.warden_verify_student,name='warden_verify_student'),
path('warden_view_rooms',views.warden_view_rooms,name='warden_view_rooms'),
path('warden_add_new_room',views.warden_add_new_room,name='warden_add_new_room'),

path('warden_accept_reject_student',views.warden_accept_reject_student,name='warden_accept_reject_student'),
path('warden_block_unblock_student',views.warden_block_unblock_student,name='warden_block_unblock_student'),



path('student_registration',views.student_registration,name='student_registration')





]
