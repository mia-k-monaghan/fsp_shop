from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

import os

User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True,editable=False,null=True,blank=True)
    includes_setup = models.BooleanField(default=False,
        help_text = "Product includes deployment & hosting setup.")
    stripe_id = models.CharField(max_length=100,blank=True,
        help_text = "The product's Stripe Price ID")
    zip_file = models.FileField(upload_to='product_files',null=True)
    description = models.TextField(null=True,blank=True)
    additional_details = models.TextField(null=True,blank=True)
    keywords = models.CharField(max_length=250,blank=True, null=True)
    featured = models.BooleanField(default=False,
        help_text = "Display product on the homepage")
    archived = models.BooleanField(default=False,
        help_text = "Hide product from all listings to prevent new subscribers while keeping current ones.")

    def __str__(self):
        return str(self.title)

    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("core:product-detail", kwargs={'slug': self.slug})

    def filename(self):
        return os.path.basename(self.zip_file.name)

class ProductImage(models.Model):
    TYPE_CHOICES = [
        ('IMG', "Image"),
        ('VID', "Video"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    type = models.CharField(choices=TYPE_CHOICES, max_length=3)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    video_embed_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.product.title} | {self.type}"

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    order_date = models.DateTimeField(auto_now=True,editable=False)
    email = models.EmailField(max_length=254,blank=True, null=True,
        help_text="This email will be used to create your PythonAnywhere host account.")
    confirmed_email = models.BooleanField(default=False)
    business_name = models.CharField(max_length=100,blank=True, null=True,
        help_text="The name of your business/website.")
    host_username = models.CharField(max_length=100,blank=True, null=True)
    host_temporary_password = models.CharField(max_length=250,blank=True, null=True)

    def __str__(self):
        return str(self.user.email)
    def get_absolute_url(self):
        return reverse("users:order-detail", kwargs={'pk': self.pk})
