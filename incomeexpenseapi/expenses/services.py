from expenses.models import Expense
from django.http import JsonResponse


class ExpensePostService:
    def __init__(self, request, serializer_class, permissions_classes):
        self.request = request
        self.serializer_class = serializer_class
        self.permissions_classes = permissions_classes    
    
    def post_view(self):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class ExpenseDetailService:
    def __init__(self, request, serializer_class, permissions_classes,id):
        self.request = request
        self.serializer_class = serializer_class
        self.permissions_classes = permissions_classes
        self.id = id
    
    def get_object(self):
        user = self.request.user
        try:
            return Expense.objects.raw(
                "SELECT * FROM expenses_expense WHERE id = %s AND owner_id = %s",
                [self.id, user.id],
            )[0]
        except Expense.DoesNotExist:
            return None
    
    def get_view(self):
        expense = self.get_object()
        if expense is not None:
            serializer = self.serializer_class(expense)
            return JsonResponse(serializer.data)
        else:
            return JsonResponse({"error": "Expense not found"}, status=404)
    
    def put_view(self):
        expense = self.get_object()
        if expense is None:
            return JsonResponse({"error": "Expense not found"}, status=404)
        serializer = self.serializer_class(expense, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    def delete_view(self):
        expense = self.get_object()
        if expense is None:
            return JsonResponse({"error": "Expense not found"}, status=404)
        expense.delete()
        return JsonResponse({"message": "Expense deleted successfully"})