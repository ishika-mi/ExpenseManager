from rest_framework import serializers

from income.models import Income

class IncomeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ['date','description','amount','source']