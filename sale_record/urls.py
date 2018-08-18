from django.urls import path
from pygments.lexer import include
from rest_framework import routers

from .views import *
router = routers.DefaultRouter()
router.register("data_post", TempAPIViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('generate_invoice/<int:pk>/', InvoiceGenerateView.as_view(), name="generate_invoice"),
    path('se_lab/', TableTemplateView.as_view(), name="table_display"),
    # path('api/', include(router.urls)),
]
