import os
import zipfile
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
import random
import baner.settings as settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.utils import timezone


def generate():
    return random.randint(9999, 100000)


@deconstructible
class RenameFile:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{instance.shenaseh}.{ext}'
        return os.path.join(self.path, filename)


@deconstructible
class RenameRandomFile:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{random.randint(100000, 999999)}.{ext}'
        return os.path.join(self.path, filename)




MONASEBAT_CHOICES = [
    ('allah', 'الله جلّ جلاله'),
    ('mohammad', 'حضرت رسول اکرم صلی الله علیه و آله'),
    ('ali', 'حضرت امیرالمومنین (ع)'),
    ('fateme', 'حضرت فاطمه الزهرا (س)'),
    ('hasan', 'امام حسن مجتبی (ع)'),
    ('hosein', 'امام حسین (ع)'),
    ('sajad', 'امام زین‌العابدین (ع)'),
    ('baqer', 'امام محمد باقر (ع)'),
    ('sadeq', 'امام جعفر صادق (ع)'),
    ('kazem', 'امام موسی کاظم (ع)'),
    ('reza', 'امام علی بن موسی الرضا (ع)'),
    ('javad', 'امام جواد (ع)'),
    ('naqi', 'امام هادی (ع)'),
    ('asgari', 'امام حسن عسگری (ع)'),
    ('mahdi', 'حضرت مهدی (ع)'),
    ('Destruction_of_Baqi_graves', 'سالروز تخریب قبور ائمه بقیع (ص)'),
    ('Holy_Quran', 'قرآن کریم'),
    ('zeynab' , 'حضرت زینب (س)'),
    ('abbas' , 'حضرت عباس (ع)'),
    ('roghaye' , 'حضرت رقیه (س)'),
    ('ali_akbar', 'حضرت علی اکبر (ع)'),
    ('ali_asghar' , 'حضرت علی اصغر (ع)'),
    ('sakine' , 'حضرت سکینه (ع)'),
    ('masomeh', 'حضرت معصومه (س)'),
    ('omolbanin' , 'حضرت ام البنین (س)'),
    ('ghasem' , 'حضرت قاسم (ع)'),
    ('khadije' , 'حضرت خدیجه (س)'),
    ('om_kolsom' , 'حضرت ام کلثوم (س)'),
    ('abdol_azim_hasani' , 'حضرت عبدالعظیم حسنی (ع)'),
    ('moslem' , 'حضرت مسلم (ع)'),
    ('haftegi' , 'هیئت هفتگی'),
    ('ramezan' , 'ماه رمضان'),
    ('adiye' , 'ادعیه'),
    ('ayad' , 'اعیاد'),


]
MONASEBAT_CHOICES2 = [
    ('الله جلّ جلاله', 'الله جلّ جلاله'),
    ('حضرت رسول اکرم صلی الله علیه و آله', 'حضرت رسول اکرم صلی الله علیه و آله'),
    ('حضرت امیرالمومنین (ع)', 'حضرت امیرالمومنین (ع)'),
    ('حضرت فاطمه الزهرا (س)', 'حضرت فاطمه الزهرا (س)'),
    ('امام حسن مجتبی (ع)', 'امام حسن مجتبی (ع)'),
    ('امام حسین (ع)', 'امام حسین (ع)'),
    ('امام زین‌العابدین (ع)', 'امام زین‌العابدین (ع)'),
    ('امام محمد باقر (ع)', 'امام محمد باقر (ع)'),
    ('امام جعفر صادق (ع)', 'امام جعفر صادق (ع)'),
    ('امام موسی کاظم (ع)', 'امام موسی کاظم (ع)'),
    ('امام علی بن موسی الرضا (ع)', 'امام علی بن موسی الرضا (ع)'),
    ('امام جواد (ع)', 'امام جواد (ع)'),
    ('امام هادی (ع)', 'امام هادی (ع)'),
    ('امام حسن عسگری (ع)', 'امام حسن عسگری (ع)'),
    ('حضرت مهدی (ع)', 'حضرت مهدی (ع)'),
    ('سالروز تخریب قبور ائمه بقیع (ص)', 'سالروز تخریب قبور ائمه بقیع (ص)'),
    ('قرآن کریم', 'قرآن کریم'),
    ('حضرت زینب (س)' , 'حضرت زینب (س)'),
    ('حضرت عباس (ع)' , 'حضرت عباس (ع)'),
    ('حضرت رقیه (س)' , 'حضرت رقیه (س)'),
    ('حضرت علی اکبر (ع)' , 'حضرت علی اکبر (ع)'),
    ('حضرت علی اصغر (ع)' , 'حضرت علی اصغر (ع)'),
    ('حضرت سکینه (ع)' , 'حضرت سکینه (ع)'),
    ('حضرت معصومه (س)', 'حضرت معصومه (س)'),
    ('حضرت ام البنین (س)', 'حضرت ام البنین (س)'),
    ('حضرت قاسم (ع)' , 'حضرت قاسم (ع)'),
    ('حضرت خدیجه (س)' , 'حضرت خدیجه (س)'),
    ('حضرت ام کلثوم (س)' , 'حضرت ام کلثوم (س)'),
    ('حضرت عبدالعظیم حسنی (ع)' , 'حضرت عبدالعظیم حسنی (ع)'),
    ('حضرت مسلم (ع)' , 'حضرت مسلم (ع)'),
    ('هیئت هفتگی' , 'هیئت هفتگی'),
    ('ماه رمضان' , 'ماه رمضان'),
    ('ادعیه' , 'ادعیه'),
    ('اعیاد' , 'اعیاد'),



]

class tarh_hay_akhrin_monasebat(models.Model):
    image = models.ImageField(upload_to=RenameRandomFile('image_last_monasebat/'))

class Vitrin_home(models.Model):
    image = models.ImageField(upload_to=RenameRandomFile('vitrin/'))


class Category(models.Model):
    title = models.CharField(max_length=40,choices=MONASEBAT_CHOICES2,null=True)
    name = models.CharField(max_length=100,choices=MONASEBAT_CHOICES)

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories',null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self .name} - {self.category.title}"


class monasebat_hay_bazdik(models.Model):
    title = models.CharField(max_length=30,default='-')
    mah_monasebat = models.CharField(max_length=50,default='-')
    roz_monasebat = models.CharField(max_length=50,default='-')
    monasebat = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='monasebat_hay_bazdik', null=True)


class imagesTowMadah(models.Model):
    font_chois = (
        ('B titr', 'B titr'),
        ('yakan_bold', 'yakan_bakh'),
        ('Lyon', 'Lyon'),
        ('Almas', 'Almas'),
        ('Mj_Sayeh', 'Mj_Sayeh'),
    )
    title = models.CharField(max_length=50, null=True)

    shenaseh = models.IntegerField(default=generate, blank=True, null=True)
    image_asli = models.ImageField(upload_to=RenameFile('media/images_asli/'))
    image_kham = models.ImageField(upload_to=RenameFile('media/images_kham/'))
    leye_baz = models.FileField(upload_to=RenameFile('media/layebaz/'), null=True, blank=True)
    Price_virtual = models.DecimalField(max_digits=7, decimal_places=0, default=300000)
    Price_chap = models.DecimalField(max_digits=7, decimal_places=0, default=700000)

    Scale_x_y = models.CharField(max_length=7, choices=(('center', 'center'), ('right', 'right')), default='center')
    x_madah = models.CharField(max_length=10, default='center')
    y_madah = models.IntegerField(default=10)
    font_size_madah = models.IntegerField(default=10)
    default_hex_color_madah = models.CharField(max_length=8, default='#ffffff')
    font_name_madah = models.CharField(max_length=20, choices=font_chois, default='B titr')

    x_madah2 = models.CharField(max_length=10, default='center')
    y_madah2 = models.IntegerField(default=10)
    font_size_madah2 = models.IntegerField(default=10)
    default_hex_color_madah2 = models.CharField(max_length=8, default='#ffffff')
    font_name_madah2 = models.CharField(max_length=20, choices=font_chois, default='B titr')

    x_sokhanran = models.CharField(max_length=10, default='center')
    y_sokhanran = models.IntegerField(default=10)
    font_size_sokhanran = models.IntegerField(default=10)
    default_hex_color_sokhanran = models.CharField(max_length=8, default='#ffffff')
    font_name_sokhanran = models.CharField(max_length=20, choices=font_chois, default='B titr')

    x_address = models.CharField(max_length=10, default='center')
    y_address = models.IntegerField()
    font_size_addres = models.IntegerField(default=10)
    default_hex_color_address = models.CharField(max_length=8, default='#ffffff')
    font_name_address = models.CharField(max_length=20, choices=font_chois, default='B titr')

    x_zamn = models.CharField(max_length=10, default='center')
    y_zaman = models.IntegerField()
    font_size_zaman = models.IntegerField(default=10)
    default_hex_color_zaman = models.CharField(max_length=8, default='#ffffff')
    font_name_zaman = models.CharField(max_length=20, choices=font_chois, default='B titr')

    x_esmheyat = models.CharField(max_length=10, default='center')
    y_esmheyat = models.IntegerField()
    font_size_esmheyat = models.IntegerField(default=10)
    default_hex_color_esmheyat = models.CharField(max_length=8, default='#ffffff')
    font_name_esmheyat = models.CharField(max_length=20, choices=font_chois, default='B titr')

    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='createdT', null=True)
    def __str__(self):
        return f'{self.title} - {self.shenaseh}'


class images(models.Model):
    font_chois = (
        ('B titr', 'B titr'),
        ('yakan_bold', 'yakan_bakh'),
        ('Lyon', 'Lyon'),
        ('Almas', 'Almas'),
        ('Mj_Sayeh', 'Mj_Sayeh'),
    )
    title = models.CharField(max_length=50 ,null=True)

    shenaseh = models.IntegerField(default=generate, blank=True, null=True)
    image_asli = models.ImageField(upload_to=RenameFile('media/images_asli/'))
    image_kham = models.ImageField(upload_to=RenameFile('media/images_kham/'))
    leye_baz = models.FileField(upload_to=RenameFile('media/layebaz/'), null=True, blank=True)
    to_madah = models.BooleanField(default=False)
    Price_virtual = models.DecimalField(max_digits=7, decimal_places=0 , default=300000)
    Price_chap = models.DecimalField(max_digits=7, decimal_places=0 , default=700000)

    Scale_x_y = models.CharField(max_length=7,choices=(('center', 'center'),('right', 'right')),default='center')
    x_madah = models.CharField(max_length=10, default='center')
    y_madah = models.IntegerField(default=10)
    font_size_madah = models.IntegerField(default=10)
    default_hex_color_madah = models.CharField(max_length=8, default='#ffffff')
    font_name_madah = models.CharField(max_length=20,choices=font_chois,default='B titr')

    x_sokhanran = models.CharField(max_length=10, default='center')
    y_sokhanran = models.IntegerField(default=10)
    font_size_sokhanran = models.IntegerField(default=10)
    default_hex_color_sokhanran = models.CharField(max_length=8, default='#ffffff')
    font_name_sokhanran = models.CharField(max_length=20,choices=font_chois,default='B titr')


    x_address = models.CharField(max_length=10, default='center')
    y_address = models.IntegerField()
    font_size_addres = models.IntegerField(default=10)
    default_hex_color_address = models.CharField(max_length=8, default='#ffffff')
    font_name_address = models.CharField(max_length=20,choices=font_chois,default='B titr')


    x_zamn = models.CharField(max_length=10, default='center')
    y_zaman = models.IntegerField()
    font_size_zaman = models.IntegerField(default=10)
    default_hex_color_zaman = models.CharField(max_length=8, default='#ffffff')
    font_name_zaman = models.CharField(max_length=20,choices=font_chois,default='B titr')

    x_esmheyat = models.CharField(max_length=10, default='center')
    y_esmheyat = models.IntegerField()
    font_size_esmheyat = models.IntegerField(default=10)
    default_hex_color_esmheyat = models.CharField(max_length=8, default='#ffffff')
    font_name_esmheyat = models.CharField(max_length=20,choices=font_chois,default='B titr')

    two_madah_True = models.ForeignKey(imagesTowMadah , on_delete=models.CASCADE , blank=True,null=True)

    created_at = models.DateTimeField(default=timezone.now)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='productsTwo',null=True)

    created = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE , related_name='created',null=True)

    def save(self, *args, **kwargs):
        # اطمینان از عدم ذخیره کردن فیلد در زمانی که نباید باشد
        if not self.to_madah:
            self.two_madah_True = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    product = models.ForeignKey(images, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class LikeTwoMadah(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    product = models.ForeignKey(imagesTowMadah, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
class generated_image(models.Model):
    shenaseh = models.IntegerField(blank=True, null=True)
    Price_virtual = models.DecimalField(max_digits=7, decimal_places=0, default=300000)
    Price_chap = models.DecimalField(max_digits=7, decimal_places=0, default=700000)
    image = models.ImageField(upload_to='media/image_with_watermark/')

class history_banner(models.Model):
    user = models.CharField(max_length=100)
    shenase_banner = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
