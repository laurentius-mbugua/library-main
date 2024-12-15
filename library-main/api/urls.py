from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
# TransactionViewSet is not a ModelViewSet, so we add URLs manually

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/check_out/', TransactionViewSet.as_view({'post': 'check_out'}), name='check_out'),
    path('transactions/return/', TransactionViewSet.as_view({'post': 'return_book'}), name='return_book'),
    path('transactions/history/', TransactionViewSet.as_view({'get': 'my_borrowing_history'}), name='borrowing_history'),
]
