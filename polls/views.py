from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from polls import reports
from django.contrib.auth import logout as auth_logout
import json

def login(request):
    return render(request, 'login.html')

def logout(request):  #for logout
    auth_logout(request)
    return redirect('/login/')

def review(request):
    h = reports.get()
    return render_to_response('Statistics.html', {"year": h[0], "month": h[1], "day": h[2], "date": h[3], "uptime": h[4], "downtime": h[5]})

def home(request):
    cid = reports.get_cid(request.user.email)
    if request.method=="POST":
        response = reports.get_data(cid)
        return HttpResponse(response)
    else:
        data = reports.get_data(cid)
        return render_to_response("data.html", {"data": data, "user": request.user.get_full_name})

# def gen_charts(request):
#     cid = reports.get_cid(request.user.email)
#     data = reports.gen_charts(cid)
#     return render_to_response("mlguard_charts.html", {"data": data, "user": request.user.get_full_name})

def mlguard_base(request):
    return render_to_response("mlguard_base.html", {'user': request.user.get_full_name})