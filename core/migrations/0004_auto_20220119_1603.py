# Generated by Django 3.2 on 2022-01-19 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210901_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='business_name',
            field=models.CharField(blank=True, help_text='The name of your business/website.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='confirmed_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, help_text='This email will be used to create your PythonAnywhere host account.', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='host_temporary_password',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='host_username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='includes_setup',
            field=models.BooleanField(default=False, help_text='Product includes deployment & hosting setup.'),
        ),
    ]
