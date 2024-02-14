from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from expenses.models import Expense
from rest_framework import permissions
from expenses.permissions import IsOwner

from expenses.serializers import ExpensesSerializers
from expenses.services import ExpenseListService, ExpenseDetailService

class ExpenseListAPIView(ListAPIView):
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return ExpenseListService(request=request,serializer_class=self.serializer_class,permissions_classes=self.permissions_classes).list_view()
    
    def post(self, request, format=None):
        return ExpenseListService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes).post_view()


class ExpenseDetailAPIView(APIView):
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, id, format=None):
        return ExpenseDetailService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes,id = id).get_view()

    def put(self, request, id, format=None):
        return ExpenseDetailService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes,id = id).put_view()

    def delete(self, request, id, format=None):
        return ExpenseDetailService(request = request, serializer_class = self.serializer_class, permissions_classes = self.permission_classes,id = id).delete_view()

    