from django.shortcuts import render
from core.models import Order,Product

# Create your views here.
def deployment_guide_view(request, slug):
    template_name=f"documentation/deploy/{slug}.html"
    product=Product.objects.get(slug=slug)
    try:
        ordered=Order.objects.get(user=request.user,product=product)
    except:
        ordered=''
    return render(request,template_name,{'ordered':ordered})
