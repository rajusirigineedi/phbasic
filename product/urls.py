from django.urls import path
from product import views

app_name = 'product'

urlpatterns = [
    path('', views.allProducts, name='home'),
    path('create/', views.create, name='create'),
    path('<int:product_id>/', views.display, name='display'),
    path('upvote/<int:product_id>/', views.upvote, name='upvote'),
    path('upvote_wo/<int:product_id>/', views.upvote_wo, name='upvote_wo')

]
