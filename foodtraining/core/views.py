from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Program, Workout, Blogpost
from .forms import UserProfileForm, ProgramForm
from .models import UserProfile
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Enrollment
from .forms import BlogpostForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import UserProfile, Program, Workout, Blogpost, Mealplan
from django.contrib.auth.models import User
from .models import Program, Lecture, Trainer
from .forms import LectureForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Trainer
from django.shortcuts import render, get_object_or_404, redirect
from .models import Program, Lecture, Trainer




def home(request):
    return render(request, 'core/home.html')

def program_list(request):
    programs = Program.objects.all()

    enrolled_program_ids = []
    if request.user.is_authenticated:
        enrolled_program_ids = Enrollment.objects.filter(user=request.user).values_list('program_id', flat=True)

    return render(request, 'core/programs.html', {
        'programs': programs,
        'enrolled_program_ids': enrolled_program_ids
    })

def workout_list(request):
    workouts = Workout.objects.all()
    return render(request, 'core/workouts.html', {'workouts': workouts})

def blog_list(request):
    blogs = Blogpost.objects.all()
    return render(request, 'core/blogs.html', {'blogs': blogs})

@login_required
def my_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None  
    return render(request, 'core/my_profile.html', {'profile': profile})


def create_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'core/create_program.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def create_profile(request):
  
    if UserProfile.objects.filter(user=request.user).exists():
        return redirect('view_profile')

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('view_profile') 
    else:
        form = UserProfileForm()

    return render(request, 'core/create_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'core/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def enroll_program(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    Enrollment.objects.get_or_create(user=request.user, program=program)
    return redirect('program_detail', program_id=program.id)

@login_required
def program_detail(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    lectures = program.lectures.all()
    trainer = program.trainer
    return render(request, 'core/program_detail.html', {
        'program': program,
        'lectures': lectures,
        'trainer': trainer
    })

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blogpost, id=blog_id)
    return render(request, 'core/blog_detail.html', {'blog': blog})


def blog_list(request):
    blogs = Blogpost.objects.all().order_by('-date_posted')
    return render(request, 'core/blog_list.html', {'blogs': blogs})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogpostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogpostForm()
    return render(request, 'core/create_blog.html', {'form': form})

@staff_member_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blogpost, id=blog_id)
    blog.delete()
    return redirect('blog_list')

@staff_member_required
def admin_dashboard(request):
    from .models import UserProfile, Program, Workout, Blogpost, Mealplan
    context = {
        'user_count': UserProfile.objects.count(),
        'program_count': Program.objects.count(),
        'workout_count': Workout.objects.count(),
        'blog_count': Blogpost.objects.count(),
        'mealplan_count': Mealplan.objects.count(),
    }
    return render(request, 'core/admin_dashboard.html', context)

def post_login_redirect(request):
    user = request.user

  
    if user.is_staff:
        return redirect('admin_dashboard')

  
    if hasattr(user, 'trainer'):
        return redirect('trainer_programs')

    return redirect('create_profile')

@login_required
def trainer_programs(request):
    trainer = Trainer.objects.get(user=request.user)
    programs = Program.objects.filter(trainer=trainer)
    return render(request, 'core/trainer_programs.html', {'programs': programs})

@login_required
def manage_lectures(request, program_id):
    trainer = get_object_or_404(Trainer, user=request.user)
    program = get_object_or_404(Program, id=program_id, trainer=trainer)

    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.program = program
            lecture.save()
            return redirect('manage_lectures', program_id=program.id)
    else:
        form = LectureForm()

    lectures = program.lectures.all()
    return render(request, 'core/manage_lectures.html', {
        'program': program,
        'form': form,
        'lectures': lectures
    })