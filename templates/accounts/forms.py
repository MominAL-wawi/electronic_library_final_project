from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("هذا البريد مستخدم مسبقاً.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', '')
            )
            # حفظ الاسم الكامل داخل first_name مثلاً
            user.first_name = self.cleaned_data['full_name']
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'photo')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')
