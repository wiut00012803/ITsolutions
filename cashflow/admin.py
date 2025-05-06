from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    Status,
    TransactionType,
    Category,
    SubCategory,
    CashFlow,
)

admin.site.unregister(Group)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "txn_type")
    list_filter = ("txn_type",)
    search_fields = ("name",)
    inlines = [SubCategoryInline]


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "status",
        "txn_type",
        "category",
        "subcategory",
        "amount",
        "comment",
    )
    list_filter = ("status", "txn_type", "category", "subcategory", "created_at")
    search_fields = ("comment",)
    date_hierarchy = "created_at"

    # ограничиваем выбор категорий и подкатегорий контекстно
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category" and "txn_type" in request.GET:
            txn_type_id = request.GET.get("txn_type")
            kwargs["queryset"] = kwargs["queryset"].filter(txn_type_id=txn_type_id)
        if db_field.name == "subcategory" and "category" in request.GET:
            category_id = request.GET.get("category")
            kwargs["queryset"] = kwargs["queryset"].filter(category_id=category_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
