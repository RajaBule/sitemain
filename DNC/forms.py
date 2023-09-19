from django import forms
from .models import Samples, CuppingSCI

class newsample(forms.ModelForm):
    class Meta:
        model = Samples
        fields = ('id', 'name', 'location', 'stype','sampleweight',
                  'sampleweightunit', 'expweight', 'expweightunit',
                  'customer', 'project', 'notes', 'country', 'farm',
                  'tracknum', 'importer', 'exporter', 'wetmill', 'drymill',
                  'cooperative', 'assosiation', 'othertrac', 'moisture',
                  'wa', 'proccessing', 'density', 'screensize',
                  'varieties', 'cropyear', 'classification',
                  'grade', 'generalcomments', 'sensorial', 'sensorialdescriptors',
                  'regdate'
                  )
        

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CuppingFormSCI(forms.ModelForm):
    class Meta:
        model = CuppingSCI
        fields = '__all__'