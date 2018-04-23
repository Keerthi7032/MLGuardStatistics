from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from polls import views

urlpatterns = [
    #url(r'^index/$', views.index, name='index'),
    url(r'^review/$', views.review, name='review'),
    url(r'^base/$', views.mlguard_base, name="mlguard_base"),
    url(r'^home/$', views.home, name="home"),
    # url(r'^gen_charts/$', views.gen_charts, name="gen_charts"),
]
