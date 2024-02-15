from django.urls import path

from . import views

urlpatterns = [
    path('',views.ExpenseListAPIView.as_view(),name="expenses"),
    path('<int:id>',views.ExpenseDetailAPIView.as_view(),name="expense"),
    path('create-expense/',views.ExpenseCreateAPIView.as_view(),name='create-expense')
]