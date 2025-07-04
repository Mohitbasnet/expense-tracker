from rest_framework import serializers
from .models import ExpenseIncome


class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = ExpenseIncome
        fields = [
            "id",
            "title",
            "description",
            "amount",
            "transaction_type",
            "tax",
            "tax_type",
            "total",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "total"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ExpenseIncomeListSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = ExpenseIncome
        fields = [
            "id",
            "title",
            "amount",
            "transaction_type",
            "total",
            "created_at",
        ]
