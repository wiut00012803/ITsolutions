from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    # бизнес, личное, налог + расширяемое.
    name = models.CharField(_("Название статуса"), max_length=50, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    # пополнение, списание + расширяемое.
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    txn_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        unique_together = ("name", "txn_type")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name


class CashFlow(models.Model):
    # главная сущность учёта движения денежных средств.
    created_at = models.DateField("Дата записи", default=timezone.now,
                                  help_text="Если нужно, вы можете изменить дату записи вручную")
    status = models.ForeignKey(Status, verbose_name=_("Статус"), on_delete=models.PROTECT)
    txn_type = models.ForeignKey(
        TransactionType, verbose_name=_("Тип операции"), on_delete=models.PROTECT
    )
    category = models.ForeignKey(Category, verbose_name=_("Категория"), on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, verbose_name=_("Подкатегория"), on_delete=models.PROTECT)
    amount = models.DecimalField(_("Сумма, ₽"), max_digits=12, decimal_places=2)
    comment = models.TextField(_("Комментарий"), blank=True)

    def clean(self):
        # валидация логических зависимостей.
        if self.category.txn_type_id != self.txn_type_id:
            raise ValidationError(
                {"category": "Категория не относится к выбранному типу операции."}
            )
        if self.subcategory.category_id != self.category_id:
            raise ValidationError(
                {"subcategory": "Подкатегория не относится к выбранной категории."}
            )

    def __str__(self):
        return f"{self.created_at} | {self.status} | {self.txn_type} | {self.category} | {self.subcategory} | {self.amount}"
