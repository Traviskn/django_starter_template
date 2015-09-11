from django.conf.urls import include, url
from django.contrib import admin

admin.site.site_header = '{{cookiecutter.project_name}}'

urlpatterns = [
    url(r'^$', '{{cookiecutter.project_name}}.views.home', name='home'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
]
