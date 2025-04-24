from django.contrib import admin
from .models import (
    UserProfile, Trainer, AdminUser, Guest,
    Program, Workout, Mealplan, Blogpost, UserProgram, Lecture
)

class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1

class ProgramAdmin(admin.ModelAdmin):
    inlines = [LectureInline]

admin.site.register(UserProfile)
admin.site.register(Trainer)
admin.site.register(AdminUser)
admin.site.register(Guest)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Workout)
admin.site.register(Mealplan)
admin.site.register(Blogpost)
admin.site.register(UserProgram)
