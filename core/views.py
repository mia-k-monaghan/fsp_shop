from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core import mail
from mimetypes import guess_type

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from settings import models as setting_models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import models

User = get_user_model()

import stripe
import os

stripe.api_key = settings.STRIPE_SECRET_KEY

def download(request, path):
    file_path=settings.MEDIA_ROOT / path
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response=HttpResponse(fh.read(),content_type='application/zip')
            response['Content-Disposition']='attachment;filename='+os.path.basename(file_path)
            return response
    raise HttpResponse(status=404)

class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if models.Product.objects.all():
            products = models.Product.objects.all()
        else:
            products = ''

        # seo data
        try:
            seo=setting_models.Seo.objects.get(page='HOME')
        except ObjectDoesNotExist:
            seo=''

    # image & content data
        # Main Background Image
        try:
            main=setting_models.Image.objects.get(type='MAIN')
        except ObjectDoesNotExist:
            main=''

        # h1 block content
        if setting_models.Content.objects.filter(page='HOME'):
            content = True
            try:
                h1=setting_models.Content.objects.filter(type='H1',page='HOME').first()
            except ObjectDoesNotExist:
                h1=''
            try:
                h2=setting_models.Content.objects.filter(type='H2',page='HOME').first()
            except ObjectDoesNotExist:
                h2=''
        else:
            content = ''
            h1=''
            h2=''

        context = {
            'featured_products': models.Product.objects.filter(featured=True, archived=False)[0:],
            'seo': seo,
            'products': products,
            'content':content,
            'main':main,
            'h1':h1,
            'h2':h2,
        }
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get(self,*args,**kwargs):
        try:
            display=setting_models.DisplayPage.objects.get(page='ABOUT',display=True)
        except ObjectDoesNotExist:
            display=False

        if not display:
            return redirect('/')
        else:
            context = super().get(self.request,**kwargs)

            # seo data
            try:
                seo=setting_models.Seo.objects.get(page='ABOUT')
            except ObjectDoesNotExist:
                seo=''

                # image & content data
            # Main Background Image
            try:
                about_image =setting_models.Image.objects.get(type='ABOUT')
            except ObjectDoesNotExist:
                about_image=''

            # h1 block content
            if setting_models.Content.objects.filter(page='ABOUT'):
                content = True
            else:
                content = ''

            try:
                h1=setting_models.Content.objects.get(type='H1',page='ABOUT')
            except ObjectDoesNotExist:
                h1=''

            context = {
                'seo': seo,
                'content':content,
                'about_image':about_image,
                'h1':h1,
            }
            return render(self.request,'core/about.html',context)

class FAQView(TemplateView):
    template_name = 'core/faq.html'

    def get(self,*args,**kwargs):
        try:
            display=setting_models.DisplayPage.objects.get(page='FAQ',display=True)
        except ObjectDoesNotExist:
            display=False

        if not display:
            return redirect('/')
        else:
            context = super().get(self.request,**kwargs)

            # seo data
            try:
                seo=setting_models.Seo.objects.get(page='FAQ')
            except ObjectDoesNotExist:
                seo=''

        # image & content data
            # Main Background Image
            try:
                faq_image=setting_models.Image.objects.get(type='FAQ')
            except ObjectDoesNotExist:
                faq_image=''

            # h1 block content
            if setting_models.Content.objects.filter(page='FAQ'):
                content = True
            else:
                content = ''

            try:
                h1=setting_models.Content.objects.get(type='H1',page='FAQ')
            except ObjectDoesNotExist:
                h1=''

            context = {
                'seo': seo,
                'content':content,
                'faq_image':faq_image,
                'h1':h1,
                'h2':setting_models.Content.objects.filter(page='FAQ',type='H2')[0:],
            }
            return render(self.request,'core/faq.html',context)

class ProductListView(ListView):
    model = models.Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if setting_models.Content.objects.filter(page='LIST'):
            content = True
        else:
            content = ''
        try:
            h1=setting_models.Content.objects.filter(type='H1',page='LIST').first()
        except ObjectDoesNotExist:
            h1=''
        # seo data
        try:
            seo=setting_models.Seo.objects.get(page='LIST')
        except ObjectDoesNotExist:
            seo=''

        context = {
            'products': models.Product.objects.filter(archived=False)[0:],
            'content': content,
            'h1':h1,
            'seo':seo,
        }
        return context

class ProductDetailView(DetailView):
    model = models.Product
    context_object_name = 'product'

    def get_context_data(self, *args,**kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)

        add_variables = {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'cancel_url': settings.CANCEL_URL,
            'success_url': settings.SUCCESS_URL,
        }
        context.update(add_variables)
        return context

class TermsView(TemplateView):
    template_name = 'core/terms.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        try:
            h1=setting_models.Content.objects.get(type='H1',page='TERMS')
        except ObjectDoesNotExist:
            h1=''
        context = {
            'h1':h1,
        }
        return context

class PrivacyView(TemplateView):
    template_name = 'core/privacy.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        try:
            h1=setting_models.Content.objects.get(type='H1',page='PRIVACY')
        except ObjectDoesNotExist:
            h1=''
        context = {
            'h1':h1,
        }
        return context

class SuccessView(TemplateView):
    template_name = 'core/success.html'

@require_POST
@csrf_exempt
def webhook_view(request):
    payload=request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload,sig_header, settings.STRIPE_SIGNING_SECRET)
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)

    # Handle a completed checkout
    if event['type'] == 'checkout.session.completed':
        #set variables
        order = event['data']['object']
        line_items = stripe.checkout.Session.list_line_items(order['id'], limit=5)
        price_id = line_items['data'][0]['price']['id']

        try:
            product = models.Product.objects.get(stripe_id=price_id)
            email = order['customer_details']['email']

            # Check if user exists
            if User.objects.filter(email=email).exists():
                user=User.objects.get(email=email)
            # create new user
            else:
                user = User.objects.create_user(
                    email=email,
                    password = None,
                )
                user.save()

            # create new order
            new_order = models.Order.objects.create(
                user=user,
                product=product,
            )
            new_order.save()

        except ObjectDoesNotExist:
            print("Purchased Product Does Not Exist")


    return HttpResponse(status=200)
