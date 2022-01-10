from django import http
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, response
from rest_framework import request, serializers
import rest_framework
from rest_framework.fields import MISSING_ERROR_MESSAGE
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication,SessionAuthentication ,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Create your views here.
# viewsets
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset  = Article.objects.all()
    

    
         

# mixins class start
class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset  = Article.objects.all()

    lookup_field = 'id'
    # authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id =None):

        if id:
            return self.retrieve(request,id)

        else:
            return self.list(request)

    def post(self,request,id =None):
        return self.create(request,id)

    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)
       
 
#  mixins class end

# class based APIView
class ArticleAPIView(APIView):

    def get(self,request):
        articles =  Article.objects.all()
        serializer = ArticleSerializer(articles,many= True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
        





# APIVIEW() DECORATOR

@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles =  Article.objects.all()
        serializer = ArticleSerializer(articles,many= True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def article_detaiil(request,pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializers.errors,status = status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



class ArticleDetails(APIView):

    def get_object(self,id):
        try:
            return Article.objects.get(id = id)

        except Article.DoesNotExist:
          return HttpResponse(status=status.HTTP_404_NOT_FOUND)


    def get(self,request,id):
        article =  self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request,id):
        article =  self.get_object(id)
        serializer = ArticleSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializers.errors,status = status.HTTP_404_NOT_FOUND)


    def delete(self,request,id):
        article =  self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



