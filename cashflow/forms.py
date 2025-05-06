from django import forms

from .models import CashFlow, Category, SubCategory


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = [
            "created_at", "status", "txn_type",
            "category", "subcategory",
            "amount", "comment",
        ]
        widgets = {
            "created_at": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "txn_type": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "subcategory": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"step": "0.01", "class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["subcategory"].queryset = SubCategory.objects.all()

    def clean(self):
        cleaned = super().clean()
        txn = cleaned.get("txn_type")
        cat = cleaned.get("category")
        sub = cleaned.get("subcategory")
        if cat and txn and cat.txn_type != txn:
            self.add_error("category",
                           "Категория не относится к выбранному типу операции.")
        if sub and cat and sub.category != cat:
            self.add_error("subcategory",
                           "Подкатегория не относится к выбранной категории.")
        return cleaned
