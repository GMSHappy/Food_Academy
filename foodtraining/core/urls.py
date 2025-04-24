from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('programs/', views.program_list, name='program_list'),
    path('workouts/', views.workout_list, name='workout_list'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('create-program/', views.create_program, name='create_program'),
    path('register/', views.register, name='register'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('post-login/', views.post_login_redirect, name='post_login_redirect'),
    path('profile/', views.view_profile, name='view_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('enroll/<int:program_id>/', views.enroll_program, name='enroll_program'),
    path('program/<int:program_id>/', views.program_detail, name='program_detail'),
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('post-login/', views.post_login_redirect, name='post_login_redirect'),
    path('trainer/programs/', views.trainer_programs, name='trainer_programs'),
    path('trainer/programs/<int:program_id>/lectures/', views.manage_lectures, name='manage_lectures'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
