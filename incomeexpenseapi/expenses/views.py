# from django.shortcuts import render
# from django.db import connection
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from expenses.models import Expense
# from rest_framework import permissions,status
# from expenses.permissions import IsOwner
# from expenses.serializers import ExpensesSerializers
# from rest_framework.response import Response

# class ExpenseListAPIView(ListCreateAPIView):
#     serializer_class = ExpensesSerializers
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         user_id = self.request.user.id
#         return Expense.objects.raw("SELECT * FROM expenses_expense WHERE owner_id = %s", [user_id])

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data)

# class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
#     serializer_class = ExpensesSerializers
#     permission_classes = (permissions.IsAuthenticated, IsOwner,)
#     lookup_field = "id"

#     def get_queryset(self):
#         user_id = self.request.user.id
#         print(type(user_id),type(self.kwargs['id']),"-----------------------------")
#         print(user_id,self.kwargs['id'],"-----------------------------")
#         expense_id = self.kwargs['id']
#         return Expense.objects.raw(f"SELECT * FROM expenses_expense WHERE id = {expense_id} AND owner_id = {user_id}")

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)



# from django.shortcuts import render
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from expenses.models import Expense
# from rest_framework import permissions
# from expenses.permissions import IsOwner

# from expenses.serializers import ExpensesSerializers

# class ExpenseListAPIView(ListCreateAPIView):
#     serializer_class = ExpensesSerializers
#     queryset = Expense.objects.all()
#     permissions_classes = (permissions.IsAuthenticated)
#     def perform_create(self, serializer):
#         return serializer.save(owner = self.request.user)
    
#     def get_queryset(self):
#         return self.queryset.filter(owner = self.request.user)

# class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
#     serializer_class = ExpensesSerializers
#     queryset = Expense.objects.all()
#     permissions_classes = (permissions.IsAuthenticated, IsOwner,)
#     lookup_field = "id"

#     def perform_create(self, serializer):
#         return serializer.save(owner = self.request.user)
    
#     def get_queryset(self):
#         return self.queryset.filter(owner = self.request.user)


from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from expenses.models import Expense
from rest_framework import permissions
from expenses.permissions import IsOwner

from expenses.serializers import ExpensesSerializers

class ExpenseListAPIView(ListAPIView):
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.raw(
            "SELECT * FROM expenses_expense WHERE owner_id = %s", [user.id]
        )

    def list(self, request, *args, **kwargs):
        expenses = self.get_queryset()
        serializer = self.serializer_class(expenses, many=True)
        return JsonResponse(serializer.data, safe=False)


class ExpenseDetailAPIView(APIView):
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_object(self, id):
        user = self.request.user
        try:
            return Expense.objects.raw(
                "SELECT * FROM expenses_expense WHERE id = %s AND owner_id = %s",
                [id, user.id],
            )[0]
        except Expense.DoesNotExist:
            return None

    def get(self, request, id, format=None):
        expense = self.get_object(id)
        if expense is not None:
            serializer = self.serializer_class(expense)
            return JsonResponse(serializer.data)
        else:
            return JsonResponse({"error": "Expense not found"}, status=404)

    def put(self, request, id, format=None):
        expense = self.get_object(id)
        if expense is not None:
            serializer = self.serializer_class(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "Expense not found"}, status=404)

    def delete(self, request, id, format=None):
        expense = self.get_object(id)
        if expense is None:
            return JsonResponse({"error": "Expense not found"}, status=404)
        expense.delete()
        return JsonResponse({"message": "Expense deleted successfully"})

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
