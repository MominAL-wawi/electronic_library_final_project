from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ProfileEditForm, UserEditForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الحساب. يمكنك تسجيل الدخول الآن.")
            return redirect('login')
        messages.error(request, "تأكد من البيانات (يوزر/إيميل فريد + كلمة مرور قوية).")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            # محاولة تسجيل دخول بالإيميل
            from django.contrib.auth.models import User
            try:
                u = User.objects.get(email=username_or_email)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح.")
            return redirect('home')
        messages.error(request, "بيانات الدخول غير صحيحة.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج.")
    return redirect('home')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        uform = UserEditForm(request.POST, instance=request.user)
        pform = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "تم تحديث الحساب.")
            return redirect('profile')
        messages.error(request, "تأكد من البيانات.")
    else:
        uform = UserEditForm(instance=request.user)
        pform = ProfileEditForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'uform': uform, 'pform': pform})
