from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from polls import views

urlpatterns = [
#url(r'^index/$', views.index, name='index'),
url(r'^review/$', views.review, name='review'),
]
