from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
import os

User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True,editable=False,null=True,blank=True)
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

    def __str__(self):
        return str(self.user.email)
