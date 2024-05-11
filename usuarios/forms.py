from django import forms
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User,Group


class NuevoUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2',]
    
    username = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': 'Username'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password Again'}))
    grupo=forms.ModelChoiceField(queryset=Group.objects.all().order_by('name'))


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para que no pregunte cuál era el passw anterior.
        self.fields.pop('old_password')
        self.fields['new_password1'].label = 'Nueva Clave: '
        self.fields['new_password2'].label = 'Confirme Nueva Clave: '

class CambioGrupoForm(forms.Form):
    grupo=forms.ModelChoiceField(label='Nivel Nuevo:',queryset=Group.objects.all().order_by('name'))

