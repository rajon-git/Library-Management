from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('book/', include('books.urls')),
    path('',views.home, name="homepage")
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
