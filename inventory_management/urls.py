# coding=utf-8
from django.conf.urls import include
from django.contrib.auth.views import login as django_login, logout as django_logout
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views as auth_token_views

from inventory_management.forms import *
from inventory_management.views import *
from core_settings import settings

# register api with default router
router = routers.DefaultRouter()
router.register(r'purchase', PurchaseRecordViewSet, base_name="purchaserecord")
# router.register(r'sales')

urlpatterns = [
    # Login Logout
    path('login/', django_login, {'template_name': 'common/login.html', 'authentication_form': LoginForm}, name='login'),
    path('logout/', django_logout, {'next_page': '/login/'}, name='logout'),
    # Home
    path('', HomePageView.as_view(), name='home'),
    # REST API
    path('api/v1/', include(router.urls)),
    # path('^api/', RedirectView.as_view(url='/api/v1/')),
    # API AUTH
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', auth_token_views.obtain_auth_token, name='get_auth_token'),
    # API DOCS
    path('api-docs/', include_docs_urls(title='Api doc')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
