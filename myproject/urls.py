from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
    re_path(r'^$', lambda r: HttpResponseRedirect('admin/')),  # Перенаправление с корневого URL на 'myapp/'
]
