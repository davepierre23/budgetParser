from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [ 
    path('api/tutorials', views.tutorial_list),
    path('api/tutorials', views.tutorial_detail),
    path('api/tutorials', views.tutorial_list_published),
    path('SaveFile', views.Save_File)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)