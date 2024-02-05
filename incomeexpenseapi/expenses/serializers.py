from rest_framework import serializers

from expenses.models import Expense

class ExpensesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ['date','description','amount','category']