from django import forms
from .models import UserProfile, Program
from .models import Blogpost
from .models import Lecture



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date']
        
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['trainer', 'title', 'description', 'duration']

class BlogpostForm(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ['program', 'title', 'content']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ['title', 'content']

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'video_url', 'pdf']