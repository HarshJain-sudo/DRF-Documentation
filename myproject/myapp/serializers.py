from rest_framework import fields, serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
   class Meta:
       model = Article
    #    fields = ['id','title', 'author', 'email']
       fields = '__all__'

