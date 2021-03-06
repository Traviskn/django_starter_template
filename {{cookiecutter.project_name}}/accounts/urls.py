from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^register/$',
        register,
        name='register'),
    url(r'^verify/(?P<email>[\w.%+-@]+)/(?P<token>[0-9A-Za-z_\-]+)/$',
        verify_email,
        name='verify'),
    url(r'^verification_sent/$',
        verification_sent,
        name='verification_sent'),
    url(r'^login/$',
        login,
        name='login'),
    url(r'^logout/$',
        logout,
        name='logout'),
    url(r'^profile/$',
        profile,
        name='profile'),
    url(r'^password_change/$',
        password_change,
        name='password_change'),
    url(r'^password_change_done/$',
        password_change_done,
        name='password_change_done'),
    url(r'^password_reset/$',
        password_reset,
        name='password_reset'),
    url(r'^password_reset_done/$',
        password_reset_done,
        name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password_reset_complete/$',
        password_reset_complete,
        name='password_reset_complete'),
    # url(r'^', include('django.contrib.auth.urls')),
]
