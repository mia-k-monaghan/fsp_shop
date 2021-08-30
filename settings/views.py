from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from . import models


class IconView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/set_icons.html'
class ThemeView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/set_themes.html'
class SocialView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/set_social.html'
class OptionalPageView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/set_pages.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        page_list = ['ABOUT','FAQ']

        for var in page_list:
            try:
                globals()[var] = models.DisplayPage.objects.get(page=var)
            except ObjectDoesNotExist:
                globals()[var] = ''
        context = {
            'about':ABOUT,
            'faq':FAQ,
        }

        return context

class CreateContentView(LoginRequiredMixin, CreateView):
    model=models.Content
    fields=['heading','details']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

    def form_valid(self, form):
        form.instance.page=self.kwargs['page']
        form.instance.type=self.kwargs['type']
        return super(CreateContentView, self).form_valid(form)

class UpdateContentView(LoginRequiredMixin, UpdateView):
    model=models.Content
    fields=['heading','details']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class DeleteContentView(LoginRequiredMixin, DeleteView):
    model=models.Content

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class CreateImageView(LoginRequiredMixin, CreateView):
    model=models.Image
    fields = ['image','alt']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

    def form_valid(self, form):
        form.instance.type=self.kwargs['type']
        return super(CreateImageView, self).form_valid(form)

class UpdateImageView(LoginRequiredMixin, UpdateView):
    model=models.Image
    fields = ['image','alt']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class DeleteImageView(LoginRequiredMixin, DeleteView):
    model=models.Image

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class CreateThemeView(LoginRequiredMixin, CreateView):
    model=models.Theme
    fields=['text_color','background_color']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

    def form_valid(self, form):
        form.instance.type=self.kwargs['type']
        return super(CreateThemeView, self).form_valid(form)

class UpdateThemeView(LoginRequiredMixin, UpdateView):
    model=models.Theme
    fields=['text_color','background_color']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class DeleteThemeView(LoginRequiredMixin, DeleteView):
    model=models.Theme

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class CreateSocialView(LoginRequiredMixin, CreateView):
    model=models.Social
    fields=['link']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

    def get_context_data(self,*args,**kwargs):
        context = super(CreateSocialView,self).get_context_data(*args,**kwargs)
        add_variables = {
            'type':self.kwargs['type']
        }
        context.update(add_variables)
        return context

    def form_valid(self, form):
        form.instance.type=self.kwargs['type']
        return super(CreateSocialView, self).form_valid(form)

class UpdateSocialView(LoginRequiredMixin, UpdateView):
    model=models.Social
    fields=['link','display']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class DeleteSocialView(LoginRequiredMixin, DeleteView):
    model=models.Social

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

class CreateDisplayPageView(LoginRequiredMixin, CreateView):
    model=models.DisplayPage
    template_name = 'settings/display_page_form.html'
    fields=['navbar_label','display']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')

    def get_context_data(self,*args,**kwargs):
        context = super(CreateDisplayPageView,self).get_context_data(*args,**kwargs)
        add_variables = {
            'page':self.kwargs['page']
        }
        context.update(add_variables)
        return context

    def form_valid(self, form):
        form.instance.page=self.kwargs['page']
        return super(CreateDisplayPageView, self).form_valid(form)

class UpdateDisplayPageView(LoginRequiredMixin, UpdateView):
    model=models.DisplayPage
    template_name = 'settings/display_page_form.html'
    fields=['navbar_label','display']

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse('core:index')
