from django.urls import path
from.import views
urlpatterns = [






    path('client_list', views.Subscriber_list, name='client_list'),
    path('clients/<int:pk>/', views.Subscriber_detail, name='client_detail'),
      path('invoice', views.invoice, name='invoice'),
]

