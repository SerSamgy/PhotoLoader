from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.upload_file, name="root"),
    url(r'^table/$', views.table, name="table"),
)