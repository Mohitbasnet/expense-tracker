from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from .models import ExpenseIncome


class ExpenseIncomeTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )
        self.expense_data = {
            "title": "Test Expense",
            "description": "Test description",
            "amount": "100.00",
            "transaction_type": "debit",
            "tax": "10.00",
            "tax_type": "flat",
        }
        self.user1_expense = ExpenseIncome.objects.create(
            user=self.user1,
            title="User 1 Expense",
            amount=Decimal("100.00"),
            transaction_type="debit",
            tax=Decimal("10.00"),
            tax_type="flat",
        )
        self.user2_expense = ExpenseIncome.objects.create(
            user=self.user2,
            title="User 2 Expense",
            amount=Decimal("200.00"),
            transaction_type="credit",
            tax=Decimal("15.00"),
            tax_type="percentage",
        )
        self.list_create_url = reverse("expenses-list")
        self.detail_url = lambda pk: reverse(
            "expenses-detail", kwargs={"pk": pk}
        )

    def get_auth_header(self, user):
        refresh = RefreshToken.for_user(user)
        return f"Bearer {refresh.access_token}"

    def test_unauthenticated_access_denied(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_expense_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        response = self.client.post(self.list_create_url, self.expense_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.expense_data["title"])
        self.assertEqual(response.data["amount"], self.expense_data["amount"])
        self.assertEqual(response.data["total"], "110.00")
        self.assertTrue(
            ExpenseIncome.objects.filter(
                title=self.expense_data["title"], user=self.user1
            ).exists()
        )

    def test_create_expense_invalid_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        invalid_data = {"title": ""}
        response = self.client.post(self.list_create_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_expenses_user_only_sees_own(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["id"], self.user1_expense.id
        )

    def test_list_expenses_superuser_sees_all(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.superuser)
        )
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_own_expense(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        response = self.client.get(self.detail_url(self.user1_expense.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user1_expense.id)

    def test_retrieve_other_user_expense_denied(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        response = self.client.get(self.detail_url(self.user2_expense.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_retrieve_any_expense(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.superuser)
        )
        response = self.client.get(self.detail_url(self.user1_expense.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user1_expense.id)

    def test_update_own_expense(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        update_data = {
            "title": "Updated Expense",
            "amount": "150.00",
            "transaction_type": "credit",
            "tax": "5.00",
            "tax_type": "percentage",
        }
        response = self.client.put(
            self.detail_url(self.user1_expense.id), update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Expense")
        self.assertEqual(response.data["amount"], "150.00")
        self.assertEqual(response.data["total"], "157.50")

    def test_update_other_user_expense_denied(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        update_data = {"title": "Hacked Expense"}
        response = self.client.put(
            self.detail_url(self.user2_expense.id), update_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_own_expense(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        update_data = {"title": "Partially Updated Expense"}
        response = self.client.patch(
            self.detail_url(self.user1_expense.id), update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Partially Updated Expense")
        self.assertEqual(response.data["amount"], "100.00")

    def test_delete_own_expense(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        response = self.client.delete(self.detail_url(self.user1_expense.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            ExpenseIncome.objects.filter(id=self.user1_expense.id).exists()
        )

    def test_delete_other_user_expense_denied(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.user1)
        )
        response = self.client.delete(self.detail_url(self.user2_expense.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            ExpenseIncome.objects.filter(id=self.user2_expense.id).exists()
        )


class BusinessLogicTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_flat_tax_calculation(self):
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title="Flat Tax Test",
            amount=Decimal("100.00"),
            transaction_type="debit",
            tax=Decimal("10.00"),
            tax_type="flat",
        )
        self.assertEqual(expense.total, Decimal("110.00"))

    def test_percentage_tax_calculation(self):
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title="Percentage Tax Test",
            amount=Decimal("100.00"),
            transaction_type="debit",
            tax=Decimal("10.00"),
            tax_type="percentage",
        )
        self.assertEqual(expense.total, Decimal("110.00"))

    def test_zero_tax_calculation(self):
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title="Zero Tax Test",
            amount=Decimal("100.00"),
            transaction_type="debit",
            tax=Decimal("0.00"),
            tax_type="flat",
        )
        self.assertEqual(expense.total, Decimal("100.00"))

    def test_percentage_tax_different_amounts(self):
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title="Percentage Tax Test 2",
            amount=Decimal("250.00"),
            transaction_type="credit",
            tax=Decimal("8.50"),
            tax_type="percentage",
        )
        self.assertEqual(expense.total, Decimal("271.25"))
