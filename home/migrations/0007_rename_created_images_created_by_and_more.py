# Generated by Django 5.0.1 on 2024-09-14 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_rename_x_zamn_images_x_zaman_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='created',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='imagestowmadah',
            old_name='created',
            new_name='created_py',
        ),
    ]
