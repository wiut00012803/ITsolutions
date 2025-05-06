from django.contrib import admin
from django.urls import path, include
from cashflow.views import CashFlowListView, CashFlowCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", CashFlowListView.as_view(), name="cashflow_list"),
    path("new/", CashFlowCreateView.as_view(), name="cashflow_create"),
    # для API
    path("", include("cashflow.urls")),
]