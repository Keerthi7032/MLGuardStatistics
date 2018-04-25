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

def charts(request):
    users = reports.get_users()
    years = reports.get_years()
    months = reports.get_months()
    days = reports.get_days()
    return render_to_response("charts.html", {"users": users, "years": years, "months": months, "days": days})

# def generate_charts(request):
#     if request.method == "POST":
#         selected_user = request.POST["selected_user"]
#         selected_year = request.POST["selected_year"]
#         selected_month = request.POST["selected_month"]
#         selected_day = request.POST["selected_day"]
#
#         data = reports.get_chart_data(selected_user, selected_year, selected_month, selected_day)

def mlguard_base(request):
    return render_to_response("mlguard_base.html", {'user': request.user.get_full_name})

def gen_charts(request):
    if request.method == "POST":
        data = json.loads(request.body.decode(encoding='UTF-8'))
        print(data)
        chart_data = reports.get_chart_data(data)
        return HttpResponse(json.dumps(chart_data))


