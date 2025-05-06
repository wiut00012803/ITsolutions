from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StatusViewSet,
    TransactionTypeViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    CashFlowViewSet,
)

router = DefaultRouter()
router.register("statuses", StatusViewSet)
router.register("types", TransactionTypeViewSet)
router.register("categories", CategoryViewSet)
router.register("subcategories", SubCategoryViewSet)
router.register("cashflows", CashFlowViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
