from django.shortcuts import render,redirect ,get_object_or_404
from  django.views.generic import View
import json
import random,string
from .models import *
from django.db.models import Sum

def generate_code():
    return "".join(random.choices(string.ascii_letters+string.digits,k=6))


class HomeView(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        long = request.POST.get('long_url')
        code = generate_code()

        URLModel.objects.create(long_url=long,short_code=code)
        short_url = request.build_absolute_uri('/' + code)
        return render(request,'index.html',{'short_url':short_url})
    
class RedirectURLView(View):
    def get(self,request,code):
        Url_obj = get_object_or_404(URLModel,short_code=code) 
        Url_obj.clicks += 1
        Url_obj.save()
        return redirect(Url_obj.long_url)
    

class DashboardView(View):
    def get(self,request):
        url_list = URLModel.objects.all()
        total_urls = url_list.count()
        total_clicks = URLModel.objects.aggregate(Sum('clicks'))['clicks__sum'] or 0
        return render(request, 'dashboard.html', {
        'url_list': url_list,
        'total_links': total_urls,'total_clicks': total_clicks
    })