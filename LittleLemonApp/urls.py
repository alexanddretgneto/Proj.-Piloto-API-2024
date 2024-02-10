# # urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import MenuItemViewSet, CartViewSet, OrderViewSet, OrderItemViewSet

# router = DefaultRouter()
# router.register(r'menu-items', MenuItemViewSet)
# router.register(r'carts', CartViewSet)
# router.register(r'orders', OrderViewSet)
# router.register(r'order-items', OrderItemViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]


from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, CartViewSet, OrderItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'menuitems', MenuItemViewSet, basename='menuitems')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'orderitems', OrderItemViewSet, basename='orderitems')

urlpatterns = [
      path('', include(router.urls)),
]
