from django.urls import path
from . import views
urlpatterns=[
    path('home/',views.save_user_data),
    path('user/get/<str:uid>',views.get_user_data),
    path("user/create_order/",views.create_order_api,name="create_order")
]