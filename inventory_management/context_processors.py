# coding=utf-8
from core_settings.settings import COMPANY_TITLE, COMPANY_LOGO, PRODUCT_TYPE


def site_details(request):
    return {
        "SITE_NAME": COMPANY_TITLE,
        "PRODUCT_TYPE": PRODUCT_TYPE,
        "SITE_LOGO": COMPANY_LOGO
    }
