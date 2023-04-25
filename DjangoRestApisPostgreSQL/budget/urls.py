from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [ 
    path('transactions', views.transaction_list),
    path('transactions/details', views.transaction_detail),
    # path('transactions/bankActions', views.distinct_bank_actions),
    path('users', views.login_user),
    path('saveFile', views.save_file),
    path('users', views.login_user),
    path('register', views.create_user)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)