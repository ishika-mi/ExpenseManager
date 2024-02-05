from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from income.models import Income
from rest_framework import permissions
from income.permissions import IsOwner

from income.serializers import IncomeSerializers

class IncomeListAPIView(ListCreateAPIView):
    serializer_class = IncomeSerializers
    queryset = Income.objects.all()
    permissions_classes = (permissions.IsAuthenticated)
    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)

class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializers
    queryset = Income.objects.all()
    permissions_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)
