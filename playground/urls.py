from django.urls import path,include
from rest_framework_nested import routers
from . import views
router=routers.DefaultRouter()
router.register('product', views.ProductViewset,basename='product')
router.register('collection', views.CollectionViewset)
router.register('cart',views.CartViewset,basename='cart')

product_router=routers.NestedDefaultRouter(router,'product',lookup='product')
product_router.register('review',views.ReviewViewset,basename='product-review')

cart_router=routers.NestedDefaultRouter(router,'cart',lookup='cart')
cart_router.register('item',views.CartItemViewset,basename='cart-item')
urlpatterns =[
    path(r'',include(router.urls)),
    path(r'',include(product_router.urls)),
    path('',include(cart_router.urls))
]