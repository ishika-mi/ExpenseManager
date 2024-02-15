from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from expenses.models import Expense
from rest_framework import permissions
from expenses.permissions import IsOwner
from rest_framework.filters import SearchFilter, OrderingFilter
from expenses.serializers import ExpensesSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from expenses.services import ExpenseDetailService, ExpensePostService
from incomeexpenseapi.custom_pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema

class ExpenseListAPIView(ListAPIView):
    serializer_class = ExpensesSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-amount']
    pagination_class = CustomPagination
    # ordering = ['-id']

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.raw(
            "SELECT * FROM expenses_expense WHERE owner_id = %s", [user.id]
        )

    def list(self, request, *args, **kwargs):
        expenses = self.get_queryset()
        serializer = self.serializer_class(expenses, many=True)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data)


class ExpenseCreateAPIView(APIView):    
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, format=None):
        return ExpensePostService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes).post_view()


class ExpenseDetailAPIView(APIView):
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, id, format=None):
        return ExpenseDetailService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes,id = id).get_view()

    def put(self, request, id, format=None):
        return ExpenseDetailService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes,id = id).put_view()

    def delete(self, request, id, format=None):
        return ExpenseDetailService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes,id = id).delete_view()

    