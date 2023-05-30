
from django.contrib import admin
from django.urls import path, include, re_path 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('group/', include("groups.urls")),
    path('meeting/', include("meetings.urls")),
    path('tutorial/', include("tutorials.urls")),
    path('G-AUTH/', include("g_auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
