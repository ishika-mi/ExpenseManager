from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from expenses.models import Expense

class ExpensesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ['id','date','description','amount','category','owner_id']
    
    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.is_authenticated:
            raise NotAuthenticated("USER_IS_NOT_AUTHENTICATED")
        return attrs
    