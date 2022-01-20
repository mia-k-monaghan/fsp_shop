from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, UpdateView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect

from core.models import Order
from .forms import LoginForm, CreateAccountForm

import stripe
# Create your views here.

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})

class AccountSetUpView(FormView):
    form_class=CreateAccountForm
    template_name='users/set_password.html'

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse_lazy('users:profile',args=[pk])

    def form_valid(self,form):
        valid = super(AccountSetUpView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('new_password1')

        #get user account & set password
        UserModel = get_user_model()
        user = UserModel.objects.get(email=email)
        user.set_password(password)
        user.save()

        #login user
        user = authenticate(email=email, password=password)
        login(self.request, user)
        send_email(user)

        return valid

class ProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        order_list = Order.objects.filter(user=user)
        context = {
            'user':user,
            'orders':order_list,
        }
        return render(self.request, 'users/profile.html', context)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model=Order

def confirm_email(request, orderid):
    user = request.user
    order = Order.objects.get(pk=orderid)
    current_site = get_current_site(request)
    mail_subject = 'Confirm your Full Stack Pak Email'
    message = render_to_string('mail_body.html', {
        'user': user,
        'domain': current_site.domain,
        'orderid':urlsafe_base64_encode(force_bytes(orderid)),
        'token':account_activation_token.make_token(order),
    })
    to_email = order.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    return HttpResponseRedirect(reverse('users:check-inbox'))

class CheckInboxView(LoginRequiredMixin, TemplateView):
    template_name = 'core/check_your_email.html'

def activate(request, orderidb64, token):
    try:
        order_id = force_text(urlsafe_base64_decode(orderidb64))
        order = Order.objects.get(pk=order_id)
    except:
        order = None
    if order is not None and account_activation_token.check_token(order, token):
        order.confirmed_email = True
        order.save()
        return HttpResponseRedirect(reverse('users:order-detail', args=[order_id]))
    else:
        return HttpResponse('Activation link is invalid!')

class UpdateOrderView(LoginRequiredMixin, UpdateView):
    model=Order
    fields=['email', 'business_name']
