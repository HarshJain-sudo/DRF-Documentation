from django.urls import path ,include
from rest_framework import routers
from .views import article_list,article_detaiil,ArticleAPIView,ArticleDetails,GenericAPIView,ArticleViewSet
from rest_framework.routers import DefaultRouter


router =  DefaultRouter()
router.register('article',ArticleViewSet,basename='article')
    
urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)), 
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),
    # path('detail/<int:pk>/', article_detaiil),
    path('detail/<int:id>/',ArticleDetails.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view()),

]
