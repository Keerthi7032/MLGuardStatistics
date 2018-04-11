from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from polls import reports

def review(request):
    m="hello"
    h=reports.get()
    return render_to_response('Statistics.html',{"year":h[0],"month":h[1],"day":h[2],"date":h[3]})
    #return render_to_response("Welcome.html",{'message':m})