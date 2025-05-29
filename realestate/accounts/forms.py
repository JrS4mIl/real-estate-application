from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from houses.models import Property
from django.utils.translation import get_language, gettext_lazy as _
from parler.forms import TranslatableModelForm
from .models import Profile
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Re-Type Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kullanımda.")
        return email


class PropertyForm(TranslatableModelForm):
    class Meta:
        model = Property
        fields = [
            'address',
            'city',
            'floor',
            'price_per_night',
            'category',
            'room_count',
            'square_meter',
            'photo',
            'photo_1',
            'photo_2',
            'photo_3',
            'photo_4',
        ]
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'room_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'square_meter': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Kullanıcının aktif dilini al
        lang = get_language()

        # Eğer aktif dil Türkçe ise "title_tr", İngilizce ise "title_en" gibi alanları kullan
        self.fields[f'title_{lang}'] = forms.CharField(
            label=_("Başlık"),
            max_length=255,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

        self.fields[f'description_{lang}'] = forms.CharField(
            label=_("Açıklama"),
            max_length=400,
            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        )