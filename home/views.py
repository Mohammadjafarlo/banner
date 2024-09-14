import random
import os
import time
import threading
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from .models import *
from django.conf import settings
from django.templatetags.static import static
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from itertools import chain

def delete_file_after_delay(orginal_file_path, file_path, delay):
    def delete_file():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
            os.remove(orginal_file_path)
            print(f'{file_path} has been deleted.')
        else:
            print(f'{file_path} does not exist.')

    threading.Thread(target=delete_file).start()





class HomeView(View):
    def get(self, request):
        latest_for_objects = monasebat_hay_bazdik.objects.order_by('-id')[:3]
        last_tuo_tarhay_akharin_monasebat = tarh_hay_akhrin_monasebat.objects.order_by('-id')[:2]
        vitrin = Vitrin_home.objects.order_by('-id')[:2]

        content = {
            'latest_for_objects': latest_for_objects,
            'last_tuo_tarhay_akharin_monasebat': last_tuo_tarhay_akharin_monasebat,
            'vitrin':vitrin
        }
        return render(request, 'home.html', content)


def mokap(foreground_image_path, final_image_path):
    background = Image.open(os.path.join(settings.BASE_DIR, 'static', 'mokap.jpg'))
    foreground = Image.open(foreground_image_path)

    if foreground.mode != 'RGBA':
        foreground = foreground.convert('RGBA')

    if foreground.width > foreground.height:
        new_width = 480
        aspect_ratio = foreground.height / foreground.width
        new_height = int(new_width * aspect_ratio)
    else:
        new_height = 480
        aspect_ratio = foreground.width / foreground.height
        new_width = int(new_height * aspect_ratio)

    foreground = foreground.resize((new_width, new_height), Image.LANCZOS)

    mask = Image.new('L', (new_width, new_height), 0)
    draw = ImageDraw.Draw(mask)
    radius = 20
    draw.rounded_rectangle([(0, 0), (new_width, new_height)], radius, fill=255)

    foreground.putalpha(mask)

    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size

    center_x = (bg_width - fg_width) // 2
    center_y = (bg_height - fg_height) // 2

    background.paste(foreground, (center_x, center_y), foreground)
    background.save(final_image_path, quality=95)




class ImagesView(View):
    form_class = ImagesForm
    template_name = 'image_form.html'
    success_url = reverse_lazy('home:home')  # به صفحه‌ای که پس از ذخیره موفقیت‌آمیز منتقل می‌شود

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # ذخیره نکردن فرم بلافاصله و دریافت شیء مربوطه
            image_instance = form.save(commit=False)
            # تنظیم فیلد created_by به کاربر لاگین شده
            image_instance.created_by = request.user
            # ذخیره نهایی شیء
            image_instance.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
            return self.get_subcategories(request)
        return super().dispatch(request, *args, **kwargs)



class ImagesTwoMadahView(View):
    form_class = ImagesTwoMadahForm
    template_name = 'image_form.html'
    success_url = reverse_lazy('home:home')  # به صفحه‌ای که پس از ذخیره موفقیت‌آمیز منتقل می‌شود

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form,'twoMadahForm': True})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # ذخیره نکردن فرم بلافاصله و دریافت شیء مربوطه
            image_instance = form.save(commit=False)
            # تنظیم فیلد created_by به کاربر لاگین شده
            image_instance.created_by = request.user
            # ذخیره نهایی شیء
            image_instance.save()
            messages.success(request, 'عکس با موفقیت ذخیره شد')
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
            return self.get_subcategories(request)
        return super().dispatch(request, *args, **kwargs)


def get_subcategories(request):
    category_id = request.GET.get('category')
    if category_id:
        category = Category.objects.get(id=category_id)
        subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
        subcategory_list = [{'id': subcategory.id, 'name': f"{subcategory.name} {category.title}"} for subcategory in subcategories]
        return JsonResponse({'subcategories': subcategory_list})
    return JsonResponse({'subcategories': []})


class BannersDetailView(View):
    def get(self, request, shenase):
        if images.objects.filter(shenaseh=shenase).exists():
            product = get_object_or_404(images, shenaseh=shenase)


        elif imagesTowMadah.objects.filter(shenaseh=shenase).exists():
            product = get_object_or_404(imagesTowMadah, shenaseh=shenase)

        if request.user.is_authenticated:
            if images.objects.filter(shenaseh=shenase).exists():
                user_likes = Like.objects.filter(user=request.user, product=product).exists()
            elif imagesTowMadah.objects.filter(shenaseh=shenase).exists():
                user_likes = LikeTwoMadah.objects.filter(user=request.user, product=product).exists()
            return render(request, 'banner_detale.html', {'object': product, 'user_likes': user_likes})
        return render(request, 'banner_detale.html', {'object': product, 'user_likes': None})


class TitlesView(View):
    def get(self, request):
        objects = Category.objects.all()
        return render(request, 'Titles.html', {'objects': objects})


class BannersView(View):
    def get(self, request, name):
        category = Category.objects.get(name=name)

        # فیلتر کردن تمام تصاویر (محصولات) مرتبط با این معصوم
        products = images.objects.filter(subcategory__category=category)
        products_tow_madah = imagesTowMadah.objects.filter(subcategory__category=category)

        # ترکیب کردن دو QuerySet
        combined_products = list(chain(products, products_tow_madah))
        return render(request, 'banners.html', {
            'objects': combined_products,
        })


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))


def add_text_to_image(img, text, font_name, font_path, font_size, color, position, c_or_r):
    position = list(position)
    if font_name == 'Yekan':
        position[1] = position[1] - 6
    elif font_name == 'Lyon':
        position[1] = position[1] - 4
    elif font_name == 'Almas':
        font_size = font_size - 3
        position[1] = position[1] - 20
    elif font_name == 'Mj_Sayeh':
        font_size = font_size + 8
        position[1] = position[1] - 8
    elif font_name == 'yakan_bold':
        position[1] = position[1] - 37
    position = tuple(position)
    draw = ImageDraw.Draw(img)
    text_color = tuple(color)
    font = ImageFont.truetype(font_path, font_size)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)

    bbox = draw.textbbox((0, 0), bidi_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    image_width, image_height = img.size

    if c_or_r == 'right':

        x = image_width - int(position[0]) - text_width
    elif c_or_r == 'center':

        if position[0] == 'center':
            x = (image_width - text_width) / 2
        else:
            x = int(position[0]) - (text_width / 2)
    else:
        x = int(position[0])
    y = position[1] - (text_height / 2)

    draw.text((x, y), bidi_text, font=font, fill=text_color)


class GeneratePhotosView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(GeneratePhotosView, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'شما باید وارد شوید و یا ثبت نام کنید', 'l_r')
            return redirect('accounts:register')

    def get(self, request, shenase):

        if images.objects.filter(shenaseh=shenase).exists():
            image = get_object_or_404(images, shenaseh=shenase)

        elif imagesTowMadah.objects.filter(shenaseh=shenase).exists():
            image = get_object_or_404(imagesTowMadah, shenaseh=shenase)

        context = {
            'image': image,
            'font_size_madah': int(image.font_size_madah),
            'font_name_madah': image.font_name_madah,
            'font_name_sokhanran': image.font_name_sokhanran,
            'font_size_sokhanran': image.font_size_sokhanran,
            'font_size_addres': image.font_size_addres,
            'font_name_addres': image.font_name_address,
            'font_size_zaman': image.font_size_zaman,
            'font_name_zaman': image.font_name_zaman,
            'font_size_esmheyat': image.font_size_esmheyat,
            'font_name_esmheyat': image.font_name_esmheyat,
            'default_hex_color_madah': image.default_hex_color_madah,
            'default_hex_color_sokhanran': image.default_hex_color_sokhanran,
            'default_hex_color_addres': image.default_hex_color_address,
            'default_hex_color_zaman': image.default_hex_color_zaman,
            'default_hex_color_esmheyat': image.default_hex_color_esmheyat,
        }
        if imagesTowMadah.objects.filter(shenaseh=shenase).exists():
            context['font_name_madah2']: image.font_name_madah2
            context['font_size_madah2'] = int(image.font_size_madah2)
            context['default_hex_color_madah2']: image.default_hex_color_madah2

        return render(request, 'generate.html', context)

    def post(self, request, shenase):
        try:
            if images.objects.filter(shenaseh=shenase).exists():
                my_model_instance = images.objects.get(shenaseh=shenase)
            elif imagesTowMadah.objects.filter(shenaseh=shenase).exists():
                my_model_instance = imagesTowMadah.objects.get(shenaseh=shenase)
        except images.DoesNotExist:
            return HttpResponse(f'Image with shenase {shenase} does not exist', status=404)

        image_path = my_model_instance.image_kham.path

        try:
            original_img = Image.open(image_path).convert('RGB')
        except FileNotFoundError:
            return HttpResponse(f'File not found: {image_path}', status=404)

        sokhanran = request.POST.get('sokhanran')
        madah = request.POST.get('madah')
        zaman = request.POST.get('zaman')
        esmheyat = request.POST.get('esmheyat')
        address = request.POST.get('addres')

        c_madah = request.POST.get('c_madah')
        c_sokhanran = request.POST.get('c_sokhanran')
        c_addres = request.POST.get('c_addres')
        c_zaman = request.POST.get('c_zaman')
        c_esm_heyat = request.POST.get('c_esmheyat')

        f_n_sokhanran = request.POST.get('font_name-sokhanran')
        f_n_madah = request.POST.get('font_name-madah')
        f_n_addres = request.POST.get('font_name-addres')
        f_n_zaman = request.POST.get('font_name-zaman')
        f_n_esm_heyat = request.POST.get('font_name-esmheyat')

        f_s_sokhanran = request.POST.get('font_size_sokhanran')
        f_s_madah = request.POST.get('font_size_madah')
        f_s_addres = request.POST.get('font_size_addres')
        f_s_zaman = request.POST.get('font_size_zaman')
        f_s_esmheyat = request.POST.get('font_size_esmheyat')

        if imagesTowMadah.objects.filter(shenaseh=shenase).exists():
            madah2 = request.POST.get('madah2')
            f_s_madah2 = request.POST.get('font_size_madah2')
            f_n_madah2 = request.POST.get('font_name-madah2')
            c_madah2 = request.POST.get('c_madah2')
        original_width, original_height = original_img.size
        new_height = 2000
        new_width = int(new_height * original_img.width / original_img.height)
        resized_img = original_img.resize((new_width, new_height), Image.LANCZOS)
        def split_text_to_two_parts(text):
            mid_index = len(text) // 2
            if ' ' in text[:mid_index]:
                mid_index = text[:mid_index].rfind(' ')
            elif ' ' in text[mid_index:]:
                mid_index = text[mid_index:].find(' ') + mid_index
            first_part = text[:mid_index].strip()
            second_part = text[mid_index:].strip()
            return [first_part, second_part]

        address_lines = split_text_to_two_parts(address) if len(address) > 15 else [address]

        texts = [sokhanran, madah, zaman] + address_lines + [esmheyat]
        font_sizes = [f_s_sokhanran, f_s_madah, f_s_zaman] + [f_s_addres] * len(address_lines) + [f_s_esmheyat]
        colors = [hex_to_rgb(c_sokhanran), hex_to_rgb(c_madah), hex_to_rgb(c_zaman)] + [hex_to_rgb(c_addres)] * len(
            address_lines) + [hex_to_rgb(c_esm_heyat)]

        positions = [
            (my_model_instance.x_sokhanran, my_model_instance.y_sokhanran),
            (my_model_instance.x_madah, my_model_instance.y_madah),
            (my_model_instance.x_zamn, my_model_instance.y_zaman),
            (my_model_instance.x_address, my_model_instance.y_address)
        ]
        fonts = [f_n_sokhanran, f_n_madah, f_n_zaman, f_n_addres]
        if len(address_lines) > 1:
            positions.append((my_model_instance.x_address, my_model_instance.y_address + (int(f_s_addres) / 0.81)))
            fonts.append(f_n_addres)
        positions.append((my_model_instance.x_esmheyat, my_model_instance.y_esmheyat))
        fonts.append(f_n_esm_heyat)
        if imagesTowMadah.objects.filter(shenaseh=shenase).exists():
            texts.append(madah2)
            font_sizes.append(f_s_madah2)
            colors.append(hex_to_rgb(c_madah2))
            positions.append((my_model_instance.x_madah2, my_model_instance.y_madah2))
            fonts.append(f_n_madah2)

        for i in range(len(texts)):
            add_text_to_image(resized_img, texts[i], fonts[i],
                              os.path.join(settings.BASE_DIR, 'static', 'font', f'{fonts[i]}.ttf'),
                              int(font_sizes[i]), colors[i], positions[i], my_model_instance.Scale_x_y)

        # Resize the image back to the original dimensions
        final_img = resized_img.resize((original_width, original_height), Image.LANCZOS)

        random_generate_image_name = random.randint(9999, 100000)
        Original_photo_path = os.path.join(settings.BASE_DIR, 'static', 'generate_iimage',
                                           f'{random_generate_image_name}.jpg')
        final_img.save(Original_photo_path)

        Original_photo = generated_image(image=Original_photo_path, shenaseh=random_generate_image_name)
        Original_photo.save()

        watermark_path = os.path.join(settings.BASE_DIR, 'static', 'watermark.png')
        generate_image_path = os.path.join(settings.BASE_DIR, 'static', 'generate_iimage',
                                           f'{random_generate_image_name}.jpg')
        background = Image.open(generate_image_path)
        foreground = Image.open(watermark_path)
        foreground = foreground.resize(background.size, Image.LANCZOS)
        background.paste(foreground, (0, 0), foreground)

        random_generate_image_with_watermark_name = random.randint(9999, 100000)
        final_image_pat = os.path.join(settings.BASE_DIR, 'static', 'image_with_watermark',
                                       f'{random_generate_image_with_watermark_name}.jpg')
        background.save(final_image_pat)

        foreground_path = final_image_pat
        random_namber = random.randint(9999, 100000)
        final_image_path = os.path.join(settings.BASE_DIR, 'static', 'image_with_watermark', f'{random_namber}.jpg')

        mokap(foreground_path, final_image_path)
        os.remove(final_image_pat)

        image = generated_image.objects.filter(shenaseh=random_generate_image_name)
        return render(request, 'view_img.html', {'image_name': final_image_path, 'image': image})


def d(request):
    return render(request, 'viwe_img_asli.html')


def like_product(request, shenase):
    if request.user.is_authenticated:
        if images.objects.filter(shenaseh=shenase):
            product = get_object_or_404(images, shenaseh=shenase)
            like, created = Like.objects.get_or_create(user=request.user, product=product)
        elif imagesTowMadah.objects.filter(shenaseh=shenase):
            product = get_object_or_404(imagesTowMadah, shenaseh=shenase)
            like, created = LikeTwoMadah.objects.get_or_create(user=request.user, product=product)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({'liked': liked, 'likes_count': product.likes.count()})
    else:
        return JsonResponse({'error': 'شما باید ثبت نام کنید و یا وارد شوید.'}, status=401)


def product_detail(request, shenase):
    product = get_object_or_404(images, shenaseh=shenase)
    likes_count = product.likes.count()
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = product.likes.filter(user=request.user).exists()
    return render(request, 'banners.html', {
        'product': product,
        'likes_count': likes_count,
        'user_has_liked': user_has_liked
    })


def buy_banner(request, shenaseh_generated, c_or_v):
    banner = get_object_or_404(generated_image, shenaseh=str(shenaseh_generated))

    # ذخیره اطلاعات بنر در session
    return render(request, 'viwe_img_asli.html', {'banner': banner.image.path})
    request.session['shenaseh_generated'] = shenaseh_generated
    request.session['banner_price'] = int(banner.Price_chap)

    return redirect('accounts:payment')


def custom_404(request, exception):
    return render(request, '404.html', status=404)
