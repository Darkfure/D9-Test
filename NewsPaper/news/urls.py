from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, Categories, \
   subscribe_to_category


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', PostSearch.as_view()),
   path('news/create', PostCreate.as_view(), name='news_create'),
   path('articles/create', PostCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/update', PostUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
   path('categories', Categories.as_view(), name='categories'),
   path('categories/<int:pk>', subscribe_to_category, name='subscribe_to_category'),



]