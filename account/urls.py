from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'account'

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list', views.UserListView.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('user/create', views.UserCreateView.as_view(), name='user-create')
]
