"""djangoApi URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# Import ViewSets
from AuthenApp.views import RegisterView, LoginView, LogoutView, UserProfileViewSet
from EmployeeApp.views import (
    HotelViewSet, RoomViewSet, HotelReservationViewSet,
    TourViewSet, TourBookingViewSet
)
from PostsApp.views import CategoryViewSet, PostViewSet, CommentViewSet

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'hotel-reservations', HotelReservationViewSet, basename='hotel-reservation')
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'tour-bookings', TourBookingViewSet, basename='tour-booking')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Routes
    path('api/', include(router.urls)),

    # Authentication
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
