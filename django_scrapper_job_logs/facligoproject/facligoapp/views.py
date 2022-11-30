import datetime

from django.shortcuts import render
import pymysql
from django.http import HttpResponseRedirect
from facligoapp.models import Scrapper
from django.db.models import Q
from django.utils import timezone
import pytz
import warnings
warnings.filterwarnings("ignore")
get_records_by_date = ""

def check_drop_down_status(get_records_by_date,drop_down_status):
    if drop_down_status == "started":
        get_records_by_date = get_records_by_date.filter(scrapper_status=1)
    elif drop_down_status == "completed":
        get_records_by_date = get_records_by_date.filter(scrapper_status=3)
    else:
        get_records_by_date = get_records_by_date

    return get_records_by_date

def index(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        f_date = datetime.datetime.strptime(from_date,'%Y-%m-%d')
        print(f_date)
        to_date = request.POST.get("to_date")
        t_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        print(t_date)
        new_records_check_box_status = request.POST.get("new_records", None)
        print(new_records_check_box_status)
        error_records_check_box_status = request.POST.get("error_records", None)
        print(error_records_check_box_status)
        drop_down_status = request.POST.get("field",None)
        print(drop_down_status)
        global get_records_by_date
        if new_records_check_box_status is None and error_records_check_box_status is None:
            get_records_by_date = Scrapper.objects.filter(start_time__date__range=(f_date, t_date))
            get_records_by_date = check_drop_down_status(get_records_by_date,drop_down_status)
        elif new_records_check_box_status and error_records_check_box_status is None:
            get_records_by_date = Scrapper.objects.filter(start_time__date__range=(f_date, t_date)).filter(new_records__gt=0)
            get_records_by_date = check_drop_down_status(get_records_by_date, drop_down_status)
        elif error_records_check_box_status and new_records_check_box_status is None:
            get_records_by_date = Scrapper.objects.filter(start_time__date__range=(f_date, t_date)).filter(error_records__gt=0)
            get_records_by_date = check_drop_down_status(get_records_by_date, drop_down_status)
        else:
            get_records_by_date = Scrapper.objects.filter(start_time__date__range=(f_date, t_date)).filter(Q(new_records__gt=0)|Q(error_records__gt=0))
            get_records_by_date = check_drop_down_status(get_records_by_date, drop_down_status)
        # print(get_records_by_date)
    else:
        roles =  Scrapper.objects.all()
        return render(request, "home.html",{"scrappers": roles})

    return render(request, "home.html", {"scrappers": get_records_by_date})



#+++++++++++++++++++++++
#For other purpose

# get_records_by_date = Scrapper.objects.all().filter(Q(start_time__date=f_date) | Q(end_time__date=t_date))

#+++++++++++++++++++++++