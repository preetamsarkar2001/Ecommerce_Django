# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'address')
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#         }

#     def save(self, commit=True):
#         user = super(SignUpForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.address = self.cleaned_data['address']
#         if commit:
#             user.save()
#         return user
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'address')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user
