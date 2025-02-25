from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from .forms import PropertyForm
from django.utils import translation
from django.template.defaultfilters import slugify
from houses.models import Property
from django.contrib.auth.decorators import login_required



# Create your views here.

def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, _('Login Welcome {}').format(request.user.username))
                    return redirect('index')

                else:
                    messages.info(request, _('Disabled Account'))
            else:
                messages.error(request, _('username_password'))
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('register'))
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    auth.logout(request)
    messages.info(request, _('logout'))
    return redirect('index')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send reset ps email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, _('Password reset link has been sent to your email address.'))
            return redirect('login')
        else:
            messages.error(request, _('Account does not exist.'))
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, _('Please reset your password'))
        return redirect('reset_password')
    else:
        messages.error(request, _('This link has been expired'))
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, _('Password reset successful'))
            return redirect('login')

        else:
            messages.error(request, _('Password do not match!'))
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')

@login_required(login_url='login')
def dashboard(request):
    user=request.user
    houses=Property.objects.filter(owner=user)
    context={
        'houses':houses
    }
    return render(request, 'dashboard/dashboard.html',context)


@login_required(login_url='login')
def add_house(request):
    user_language = translation.get_language()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user
            house.set_current_language(user_language)
            house.save()

            # Çeviri alanlarını güncelle
            house.title = form.cleaned_data[f'title_{user_language}']
            house.description = form.cleaned_data[f'description_{user_language}']
            house.slug = slugify(house.title)
            house.save()

            messages.success(request, _('House added successfully.'))
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = PropertyForm()

    context = {'form': form}
    return render(request, 'dashboard/add_house.html', context)


