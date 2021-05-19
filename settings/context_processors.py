from . import models
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def add_variable_to_context(request):
    add_context = {}
    image_list = ['logo','icon','a_icon']
    social_list = ['fb','ig','pin','tw']
    theme_list = ['navbar','footer']

    # images & icons
    for var in image_list:
        try:
            globals()[var] = models.Image.objects.get(type=var.upper())
        except ObjectDoesNotExist:
            globals()[var] = ''

    # social Links
    for var in social_list:
        try:
            globals()[var] = models.Social.objects.get(type=var.upper())
        except ObjectDoesNotExist:
            globals()[var] = ''

    #color themes
    for var in theme_list:
        try:
            globals()[var] = models.Theme.objects.get(type=var.upper())
        except ObjectDoesNotExist:
            globals()[var] = ''

    if navbar:
        if navbar.text_color=='LIGHT':
            nav_text='dark'
        else:
            nav_text='light'
    else:
        nav_text=''

    if footer:
        if footer.text_color=='LIGHT':
            footer_text='light'
        else:
            footer_text='dark'
    else:
        footer_text=''

    return {
        'logo': logo,
        'site_icon':icon,
        'apple_icon':a_icon,
        'display_list': models.DisplayPage.objects.filter(display=True).all(),
        'social_list': models.Social.objects.all(),
        'facebook':fb,
        'insta':ig,
        'pinterest':pin,
        'twitter':tw,
        'nav':navbar,
        'nav_text':nav_text,
        'footer':footer,
        'footer_text':footer_text,
    }
