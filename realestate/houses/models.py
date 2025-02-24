import slugify
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import  TranslatableModel,TranslatedFields
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    name = models.CharField(_('title'),max_length=100, unique=True)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Property(TranslatableModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('flaw','Flaw')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name="Ev Sahibi")
    translations=TranslatedFields(
        title = models.CharField(_('title'),max_length=255),
        description = models.TextField(_('description'),max_length=400)
    )
    slug = models.SlugField(unique=True, editable=False, blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    address = models.CharField(max_length=255, verbose_name=_("Adres"))
    city = models.CharField(max_length=100, verbose_name=_("Şehir"))
    floor = models.IntegerField(verbose_name=_("Kat"),default=1)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Gecelik Ücret"))
    available = models.BooleanField(default=False, verbose_name="Mevcut")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name=_("Kategori"))
    room_count = models.IntegerField(verbose_name=_("Oda Sayısı"))
    square_meter = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Metrekare"))
    is_featured=models.BooleanField(default=False,verbose_name='is_featured')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default="draft")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('title', any_language=True))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="Kullanıcı")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings', verbose_name="Ev")
    check_in = models.DateField(verbose_name="Giriş Tarihi")
    check_out = models.DateField(verbose_name="Çıkış Tarihi")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                      verbose_name="Toplam Ücret")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            self.total_price = nights * self.property.price_per_night
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.property.title} ({self.check_in} to {self.check_out})'
