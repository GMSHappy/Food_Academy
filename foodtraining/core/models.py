from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

#User Profile Extension
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    enrolled_programs = models.ManyToManyField('Program', related_name='students', blank=True)
    def __str__(self):
        return self.user.username

#Trainer
from django.contrib.auth.models import User

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialty_field = models.CharField(max_length=100)
    email = models.EmailField()
    experience_year = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name

#AdminUser
class AdminUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Guest
class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#Program
class Program(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")

    def __str__(self):
        return self.title

#Workout
DIFFICULTY_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

class Workout(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    video_url = models.URLField(blank=True, null=True)
    recommended_meal = models.ForeignKey('Mealplan', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

#Mealplan
class Mealplan(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    calories = models.IntegerField()
    meals = models.TextField()

    def __str__(self):
        return self.title

#Blogpost
class Blogpost(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blogpost, id=blog_id)
    return render(request, 'core/blog_detail.html', {'blog': blog})

#User
class UserProgram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} → {self.program.title}"

class Lecture(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    pdf = models.FileField(upload_to='lectures/pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.program.title})"
    
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.lecture.title} - {'Done' if self.completed else 'Not yet'}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.program.title}" 

    class Meta:
        unique_together = ('user', 'program') 

class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1  
    fields = ('title', 'description', 'video_url', 'pdf')

class ProgramAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_display = ('title', 'trainer', 'duration')
    search_fields = ('title', 'trainer__name')

