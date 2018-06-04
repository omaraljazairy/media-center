"""mediaplayer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from useractivity import views

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
#    url('docs/', include('sphinxdoc.urls')),
    url('mediacenter/', include('library.urls')),
    url('alarmclock/', include('alarmclock.urls')),
    url('accounts/', include('django.contrib.auth.urls')), #login/, logout/, password_reset/, password_change/
#    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL,document_root=settings.BASE_DIR)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
