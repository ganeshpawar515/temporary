from django.urls import path
from . import views
urlpatterns=[
    path('hello/', views.hello),
    path('books/get/',views.BookView.as_view()),
    path('books/<int:pk>/',views.BookUpdateView.as_view())
    ]