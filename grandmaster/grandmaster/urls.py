"""grandmaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('authentication.urls')),
                  path('news/', include('news.urls')),
                  path('events/', include('event.urls')),
                  path('users/', include('profiles.urls')),
                  path('bitrix/', include('webhook.urls')),
                  path('club_content/', include('club_content.urls')),
                  path('sport_groups/', include('sport_groups.urls')),
                  path('gyms/', include('gyms.urls')),
                  path('qrcodes/', include('qrcodes.urls')),
                  path('invoices/', include('invoice.urls')),
                  path('videos/', include('videos.urls')),
                  path('instructions/', include('instructions.urls')),
                  path('schedule/', include('schedule.urls')),
                  path('visit_log/', include('visit_log.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
