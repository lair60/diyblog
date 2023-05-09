"""diyblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('', RedirectView.as_view(url='blog/', permanent=True)),
	path('accounts/', include('django.contrib.auth.urls')),
	path('createnewuser/', RedirectView.as_view(url='/blog/newuser/', permanent=True), name='create-new-user'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from diyblog.clock import start_jobs
import os
initialized = os.environ.get('CLOCK_INITIALIZED', 'False')
if initialized == 'False':
    os.environ['CLOCK_INITIALIZED'] = 'True'
    print('id: '+str(os.getpid()))
    start_jobs()
