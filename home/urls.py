from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('s/', d, name='1'),
    path('banners/<str:name>', BannersView.as_view(), name='banners'),
    path('titles/', TitlesView.as_view(), name='Titles'),
    path('showbanners/<shenase>/', BannersDetailView.as_view(), name='showbanners'),
    path('generate/<shenase>/', GeneratePhotosView.as_view(), name='generate_photos'),
    path('createimage/', ImagesView.as_view(), name='createimage'),
    path('createimagetwomadah/', ImagesTwoMadahView.as_view(), name='createimagetwomadah'),
    path('ajax/subcategories/', get_subcategories, name='get_subcategories'),  # اضافه کردن این خط
    path('banners/<shenase>/like/', like_product, name='like_product'),
    path('buy_banner/<int:shenaseh_generated>/<str:c_or_v>', buy_banner, name='buy_banner'),
]
