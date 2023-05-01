from django.urls import path
from .views import(
    ProductList,
    ProductSearchView,
    ProductStatistics,
    ProductCreateAPIView,
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
    CategoryUpdateAPIView,
    CategoryDeleteAPIView,
)
urlpatterns = [
    path('list/', ProductList.as_view(), name='product-list'),
    path('search/', ProductSearchView.as_view(), name='product-search'),
    path('stats/', ProductStatistics.as_view(), name='product-stats'),
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('<int:id>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('<int:id>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('category/update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='product-update'),
    path('category/delete/<int:pk>/', CategoryDeleteAPIView.as_view(), name='product-delete'),
]