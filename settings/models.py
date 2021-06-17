from django.db import models

# Create your models here.
class DisplayPage(models.Model):
    DISPLAY_PAGE_CHOICES = [
        ('ABOUT' , 'About Page'),
        ('FAQ' , 'FAQ'),
    ]

    page = models.CharField(
        max_length=7,
        choices=DISPLAY_PAGE_CHOICES,
    )
    navbar_label = models.CharField(max_length=50,null=True,blank=True)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.page

class Social(models.Model):
    SOCIAL_TYPE_CHOICES = [
        ('FB','Facebook'),
        ('IG','Instagram'),
        ('PIN','Pinterest'),
        ('TW','Twitter'),

    ]
    type = models.CharField(
        max_length=3,
        choices=SOCIAL_TYPE_CHOICES,
        default='FB',
        unique=True
    )
    link = models.URLField(max_length=200,blank=True,null=True)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.type


class Content(models.Model):
    CONTENT_PAGE_CHOICES = [
        ('HOME' , 'Home Page'),
        ('ABOUT' , 'About Page'),
        ('FAQ' , 'FAQ'),
        ('LIST' , 'Product List Page'),
        ('TERMS','Terms of Service'),
        ('PRIVACY','Privacy Policy'),
    ]
    CONTENT_TYPE_CHOICES = [
        ('H1' , 'Heading 1'),
        ('H2' , 'Heading 2'),
    ]

    page = models.CharField(
        max_length=7,
        choices=CONTENT_PAGE_CHOICES,
        default='HOME'
    )
    type = models.CharField(
        max_length=2,
        choices=CONTENT_TYPE_CHOICES,
        default='H1'
    )
    heading = models.CharField(max_length=254)
    details = models.TextField(blank=True,null=True,
        help_text = "Add some details as a paragraph under the heading")

    class Meta:
        verbose_name_plural = "Website Content"

    def __str__(self):
        return f"{self.page} | {self.type}"

class Image(models.Model):
    IMAGE_TYPE_CHOICES = [
        ('MAIN',"Main Homepage Image"),
        ('ABOUT',"About Page Image"),
        ('ICON','Site Icon'),
        ('A_ICON','Apple Icon'),
        ('LOGO','Navbar Logo'),

    ]
    type = models.CharField(
        max_length=6,
        choices=IMAGE_TYPE_CHOICES,
        default='MAIN',
        unique = True
    )
    image = models.ImageField(upload_to='website_images',null=True)
    alt = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.type

class Seo(models.Model):
    PAGE_CHOICES = [
        ('HOME' , 'Home Page'),
        ('ABOUT' , 'About Page'),
        ('FAQ' , 'FAQ'),
        ('LIST','Product List Page'),
    ]
    page = models.CharField(
        max_length=7,
        choices=PAGE_CHOICES,
        default='HOME',
        unique=True,
    )
    title = models.CharField(max_length=50,blank=True,null=True,
        help_text = "This will display on the browser tab")
    description = models.CharField(max_length=250,blank=True,null=True,
        help_text = "This will display a text preview in internet search results")
    keywords = models.TextField(blank=True,null=True,
        help_text = "Enter keywords separated by a comma. (Example: subscription website, affordable)")
    #TODO: add social url, title, img, & description

    class Meta:
        verbose_name_plural = "SEO"

    def __str__(self):
        return self.page

class Theme(models.Model):
    TYPE_CHOICES = [
        ('NAVBAR', 'Navbar'),
        ('FOOTER','Footer'),
    ]
    TEXT_COLOR_CHOICES = [
        ('LIGHT', 'light'),
        ('DARK','dark'),
    ]

    type = models.CharField(max_length=6,choices=TYPE_CHOICES, unique=True)
    text_color = models.CharField(max_length=5,choices=TEXT_COLOR_CHOICES)
    background_color = models.CharField(max_length=20,
        help_text='Enter a valid hex code. (Example: #301934)')

    def __str__(self):
        return self.type
