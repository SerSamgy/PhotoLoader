from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.root, name="root"),
    url(r'^table/$', views.table, name="table"),
)