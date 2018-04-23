from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from polls import reports
import json

def login(request):
    return render(request, 'login.html')

def review(request):
    h = reports.get()
    return render_to_response('Statistics.html', {"year": h[0], "month": h[1], "day": h[2], "date": h[3], "uptime": h[4], "downtime": h[5]})

def home(request):
    # cid = reports.get_cid(request.user.email)
    cid = 6
    if request.method=="POST":
        data = json.loads(request.body.decode(encoding='UTF-8'))
        # f = data['fd']
        # t = data['td']
        response = reports.get_data(cid)
        return HttpResponse(response)
    else:
        # f, t = reports.get_min_max_date(cid)
        data = reports.get_data(cid)
        return render_to_response("data.html", {"data": data, "user": request.user.get_full_name})

# def gen_charts(request):
#     cid = reports.get_cid(request.user.email)
#     data = reports.gen_charts(cid)
#     return render_to_response("mlguard_charts.html", {"data": data, "user": request.user.get_full_name})

def mlguard_base(request):
    cid = reports.get_cid(request.user.email)
    return render_to_response("mlguard_base.html", {'user': request.user.get_full_name})