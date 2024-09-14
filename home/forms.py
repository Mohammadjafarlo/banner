from .models import *
from django import forms

MONASEBAT_CHOICES = [
    ('---', '---'),
    ('mohammad', 'حضرت محمد (ص)'),
    ('ali', 'امام علی بن ابی‌طالب (ع)'),
    ('fateme', 'حضرت فاطمه الزهرا (س)'),
    ('hasan', 'امام حسن (ع)'),
    ('hosein', 'امام حسین (ع)'),
    ('moharam', 'محرم'),
    ('sajad', 'امام زین‌العابدین (ع)'),
    ('baqer', 'امام محمد باقر (ع)'),
    ('sadeq', 'امام جعفر صادق (ع)'),
    ('kazem', 'امام موسی کاظم (ع)'),
    ('reza', 'امام علی رضا (ع)'),
    ('javad', 'امام جواد (ع)'),
    ('naqi', 'امام علی نقی (ع)'),
    ('asgari', 'امام حسن عسگری (ع)'),
    ('mahdi', 'حضرت مهدی (ع)'),
    ('ghadir' , 'عید غدیر'),
    ('ali_asghar' , 'حضرت علی اصغر (ع)'),
    ('abas' , 'حضرت عباس (ع)'),
    ('zeynab' , 'حضرت زینب (س)'),
    ('ghasem' , 'حضرت قاسم (ع)'),
    ('ali_akbar' , 'حضرت علی اکبر (ع)'),
    ('roghaye' , 'حضرت رقیه (س)'),
    ('masomeh' , 'حضرت معصومه (س)'),
    ('abdol_azim_hasani' , 'حضرت عبدالعظیم حسنی (ع)'),
    ('omolbanin' , 'حضرت ام البنین (س)'),


]
VELADAT_OR_SHAHADAT_CHOICES = [
    ('veladat', 'ولادت'),
    ('shahadat', 'شهادت'),
    ('digar', 'دیگر')
]








class ImagesForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Category')
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.none(), required=True, label='Subcategory')

    class Meta:
        model = images
        fields = [
            'title', 'shenaseh', 'image_asli', 'image_kham', 'leye_baz', 'to_madah', 'Price_virtual', 'Price_chap',
            'Scale_x_y_madah', 'x_madah', 'y_madah', 'font_size_madah', 'default_hex_color_madah', 'font_name_madah',
            'Scale_x_y_sokhanran','x_sokhanran', 'y_sokhanran', 'font_size_sokhanran', 'default_hex_color_sokhanran', 'font_name_sokhanran',
            'x_address', 'y_address', 'font_size_addres', 'default_hex_color_address', 'font_name_address','Scale_x_y_address', 'x_zaman',
            'y_zaman', 'font_size_zaman', 'default_hex_color_zaman', 'font_name_zaman','Scale_x_y_zaman', 'x_esmheyat', 'y_esmheyat',
            'font_size_esmheyat', 'default_hex_color_esmheyat', 'font_name_esmheyat','Scale_x_y_esmheyat', 'two_madah_True', 'subcategory'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # حذف فیلد shenaseh از فرم
        self.fields.pop('shenaseh', None)

        # اضافه کردن کلاس‌ها به تمامی فیلدها به جز to_madah
        for field_name, field in self.fields.items():
            if field_name != 'to_madah':
                field.widget.attrs.update({'class': 'form-control col-6'})

        # افزودن کلاس خاص برای چک‌باکس
        self.fields['to_madah'].widget.attrs.update({'class': 'form-check-input'})

        # فیلتر زیر دسته‌های مرتبط با دسته بندی انتخاب شده
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # اگر مقدار نامعتبر باشد، هیچ زیر دسته‌ای نمایش داده نشود
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')




class ImagesTwoMadahForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Category')
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.none(), required=True, label='Subcategory')

    class Meta:
        model = imagesTowMadah
        fields = [
            'title', 'shenaseh', 'image_asli', 'image_kham', 'leye_baz', 'Price_virtual', 'Price_chap',
            'Scale_x_y_madah', 'x_madah', 'y_madah', 'font_size_madah', 'default_hex_color_madah', 'font_name_madah',
            'x_madah2', 'y_madah2', 'font_size_madah2', 'default_hex_color_madah2', 'font_name_madah2','Scale_x_y_madah2',
            'x_sokhanran', 'y_sokhanran', 'font_size_sokhanran', 'default_hex_color_sokhanran', 'font_name_sokhanran','Scale_x_y_sokhanran',
            'x_address', 'y_address', 'font_size_addres', 'default_hex_color_address', 'font_name_address','Scale_x_y_address', 'x_zaman',
            'y_zaman', 'font_size_zaman', 'default_hex_color_zaman', 'font_name_zaman','Scale_x_y_zaman', 'x_esmheyat', 'y_esmheyat',
            'font_size_esmheyat', 'default_hex_color_esmheyat', 'font_name_esmheyat','Scale_x_y_esmheyat','subcategory'
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # حذف فیلد shenaseh از فرم
        self.fields.pop('shenaseh', None)


        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-6'})

        # فیلتر زیر دسته‌های مرتبط با دسته بندی انتخاب شده
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # اگر مقدار نامعتبر باشد، هیچ زیر دسته‌ای نمایش داده نشود
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')



class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget = forms.HiddenInput()
