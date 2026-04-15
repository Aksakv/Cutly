from django.shortcuts import render,redirect ,get_object_or_404
from  django.views.generic import View
import json
import random,string
from .models import *
from django.db.models import Sum,Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from .models import ClickEvent

def home(request):
    return HttpResponse("Hello Aksa! Updated code working 🚀")

def generate_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))

class HomeView(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        long = request.POST.get('long_url')
        
        existing = URLModel.objects.filter(long_url=long).first()
        if existing:
            obj = existing
        else:
            code = generate_code()
            obj = URLModel.objects.create(long_url=long, short_code=code)
        short_url = request.build_absolute_uri('/' + obj.short_code)


        return render(request,'index.html',{'short_url':short_url,'obj':obj})
    
class RedirectURLView(View):
    def get(self,request,code):
        Url_obj = get_object_or_404(URLModel,short_code=code) 
        Url_obj.clicks += 1
        Url_obj.save()
        ClickEvent.objects.create(url=Url_obj)
        return redirect(Url_obj.long_url)
    

class DashboardView(View):
    def get(self,request):
        url_list = URLModel.objects.all().order_by('-id')
        total_urls = url_list.count()
        total_clicks = URLModel.objects.aggregate(
            total=Sum('clicks')
        )['total'] or 0
        labels = [url.short_code for url in url_list]
        data = [url.clicks for url in url_list]
        top_urls = URLModel.objects.filter(clicks__gt=0).order_by('-clicks')[:5]

        if top_urls:
            pie_labels = [url.short_code for url in top_urls]
            pie_data = [url.clicks for url in top_urls]
        else:
            pie_labels = ["No Data"]
            pie_data = [1]
   
        daily_clicks = (
        ClickEvent.objects
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(total=Count('id'))
        .order_by('date')
                        )
        dates = [str(item['date']) for item in daily_clicks]
        clicks = [item['total'] for item in daily_clicks]
        return render(request, 'dashboard.html', {
        'url_list': url_list,
        'total_links': total_urls,
        'total_clicks': total_clicks,
        'labels': labels,
        'data': data,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'dates': dates,
        'clicks': clicks
        
    })