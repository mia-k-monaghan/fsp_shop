# Generated by Django 3.2 on 2021-06-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displaypage',
            name='page',
            field=models.CharField(choices=[('ABOUT', 'About Page'), ('FAQ', 'FAQ'), ('LIST', 'Product List Page')], max_length=7),
        ),
    ]
