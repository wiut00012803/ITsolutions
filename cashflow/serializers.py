from rest_framework import serializers

from .models import (
    Status,
    TransactionType,
    Category,
    SubCategory,
    CashFlow,
)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = "__all__"
