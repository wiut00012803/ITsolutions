from datetime import date

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from rest_framework import viewsets

from .filters import CashFlowFilter
from .forms import CashFlowForm
from .models import Status, TransactionType, Category, SubCategory, CashFlow
from .serializers import (
    StatusSerializer,
    TransactionTypeSerializer,
    CategorySerializer,
    SubCategorySerializer,
    CashFlowSerializer,
)


# api viewsets для справочников и записей ддс

class StatusViewSet(viewsets.ModelViewSet):
    """
    crud для статусов
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TransactionTypeViewSet(viewsets.ModelViewSet):
    """
    crud для типов операций
    """
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    crud для категорий (привязка к типу операции)
    """
    queryset = Category.objects.select_related("txn_type").all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    """
    crud для подкатегорий (привязка к категории → тип операции)
    """
    queryset = SubCategory.objects.select_related(
        "category", "category__txn_type"
    ).all()
    serializer_class = SubCategorySerializer


class CashFlowViewSet(viewsets.ModelViewSet):
    """
    crud и фильтрация записей ддс
    """
    queryset = CashFlow.objects.select_related(
        "status", "txn_type", "category", "subcategory"
    ).all()
    serializer_class = CashFlowSerializer
    filterset_class = CashFlowFilter


# веб представления для списка, создания, редактирования и удаления

class CashFlowListView(ListView):
    model = CashFlow
    template_name = "cashflow_list.html"
    context_object_name = "object_list"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            "status", "txn_type", "category", "subcategory"
        )
        params = self.request.GET

        # фильтры
        if params.get("date_from"):
            qs = qs.filter(created_at__gte=params["date_from"])
        if params.get("date_to"):
            qs = qs.filter(created_at__lte=params["date_to"])
        if params.get("status"):
            qs = qs.filter(status_id=params["status"])
        if params.get("txn_type"):
            qs = qs.filter(txn_type_id=params["txn_type"])
        if params.get("category"):
            qs = qs.filter(category_id=params["category"])
        if params.get("subcategory"):
            qs = qs.filter(subcategory_id=params["subcategory"])

        # сортировка
        ordering = params.get("ordering", "-created_at")
        return qs.order_by(ordering)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        # убираем page, чтобы не дублировался
        params.pop("page", None)
        # сохраняем "чистый" qs
        ctx["clean_qs"] = params.urlencode()

        # ваш остальной контекст
        ctx["statuses"] = Status.objects.all()
        ctx["types"] = TransactionType.objects.all()
        ctx["categories"] = Category.objects.select_related("txn_type").all()
        ctx["subcategories"] = SubCategory.objects.select_related("category").all()
        ctx["selected_status"] = params.get("status", "")
        ctx["selected_type"] = params.get("txn_type", "")
        ctx["selected_category"] = params.get("category", "")
        ctx["selected_subcategory"] = params.get("subcategory", "")
        ctx["current_order"] = self.request.GET.get("ordering", "-created_at")
        return ctx


class CashFlowCreateView(CreateView):
    model = CashFlow
    form_class = CashFlowForm
    template_name = "cashflow_form.html"
    success_url = reverse_lazy("cashflow_list")

    def get_initial(self):
        ini = super().get_initial()
        ini["created_at"] = date.today().strftime("%Y-%m-%d")
        return ini

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cats"] = Category.objects.select_related("txn_type").all()
        ctx["subs"] = SubCategory.objects.select_related("category").all()
        return ctx
