from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView,DestroyAPIView
from .models import Book,Author

@api_view(['GET'])
def hello(request):
    return Response({"message":"welcome to practice app"})

from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'

class BookSerializer(serializers.ModelSerializer):
    # author=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Book
        fields=['id','title','price','rating','published','author']

class BookReadSerializer(serializers.ModelSerializer):
    author=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Book
        fields=['id','title','price','rating','published','author']

class BookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=["title","price","rating","published","author"]
class BookView(APIView):
    def get(self,request):
        books=Book.objects.all()
        serializer=BookSerializer(books, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"201 success"})
        return Response({"message":"400 bad request"})

class BookReadView():
    queryset=Book.objects.all()
    serializer_class=BookReadSerializer


class BookUpdateView(DestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=BookWriteSerializer