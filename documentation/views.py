from django.shortcuts import render
from core.models import Product

# Create your views here.
def deployment_guide_view(request, slug):
    template_name=f"documentation/deploy/{slug}.html"
    return render(request,template_name)
