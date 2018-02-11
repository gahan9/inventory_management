# coding=utf-8
from django.conf.urls import url, include
from django.contrib.auth.views import login as django_login, logout as django_logout
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from rest_framework import routers

from inventory_management.views import *
from core_settings import settings

# register api with default router
router = routers.DefaultRouter()
router.register(r'purchase', PurchaseRecordViewSet)
# router.register(r'sales')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/', RedirectView.as_view(url='/api/v1/')),
    url(r'^login/', django_login, {'template_name': 'common/login.html'}, name='login'),
    url(r'^logout/', django_logout, {'next_page': '/login/'}, name='logout'),
    url(r'^', HomePageView.as_view(), name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
