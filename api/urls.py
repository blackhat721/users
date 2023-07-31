from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'topics',TopicViewSet)
router.register(r'rooms',RoomViewSet)
router.register(r'messages',MessageViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/',UserloginView.as_view(),name='login'),
    path('rr/',getRooms,name='rr'),
    path('messages/by_room/<int:room_id>', MessagesByRoomView.as_view(), name='messages_by_room'),
]

