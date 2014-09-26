from django.conf.urls import patterns, include, url
from django.contrib import admin
from screlp import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Screlp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home),
    url(r'^search/', views.result)

)
