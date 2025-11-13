from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q
from datetime import date
from .models import Hotel, Room, HotelReservation, Tour, TourBooking
from .serializers import (
    HotelSerializer, HotelListSerializer, RoomSerializer,
    HotelReservationSerializer, TourSerializer, TourListSerializer,
    TourBookingSerializer
)
from rest_framework import serializers as drf_serializers


class HotelViewSet(viewsets.ModelViewSet):
    """Hotel management viewset"""
    queryset = Hotel.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'country', 'description']
    ordering_fields = ['name', 'star_rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return HotelListSerializer
        return HotelSerializer

    def get_queryset(self):
        """Filter hotels based on query parameters"""
        queryset = super().get_queryset()

        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Filter by country
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__icontains=country)

        # Filter by star rating
        star_rating = self.request.query_params.get('star_rating', None)
        if star_rating:
            queryset = queryset.filter(star_rating=star_rating)

        return queryset

    @action(detail=True, methods=['get'])
    def rooms(self, request, pk=None):
        """Get all rooms for a specific hotel"""
        hotel = self.get_object()
        rooms = hotel.rooms.filter(available_rooms__gt=0)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search hotels by various criteria"""
        query = request.query_params.get('q', '')
        queryset = self.get_queryset()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query) |
                Q(description__icontains=query)
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    """Room management viewset"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['hotel__name', 'room_type']
    ordering_fields = ['price_per_night', 'capacity']
    ordering = ['price_per_night']

    def get_queryset(self):
        """Filter rooms based on query parameters"""
        queryset = super().get_queryset()

        # Filter by hotel
        hotel_id = self.request.query_params.get('hotel_id', None)
        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)

        # Filter by availability
        available = self.request.query_params.get('available', None)
        if available == 'true':
            queryset = queryset.filter(available_rooms__gt=0)

        # Filter by room type
        room_type = self.request.query_params.get('room_type', None)
        if room_type:
            queryset = queryset.filter(room_type=room_type)

        return queryset


class HotelReservationViewSet(viewsets.ModelViewSet):
    """Hotel reservation management viewset"""
    queryset = HotelReservation.objects.all()
    serializer_class = HotelReservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['check_in', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Users can only see their own reservations, staff can see all"""
        if self.request.user.is_staff:
            return HotelReservation.objects.all()
        return HotelReservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the user and update room availability"""
        room = serializer.validated_data['room']
        num_rooms = serializer.validated_data['num_rooms']

        # Check availability
        if room.available_rooms < num_rooms:
            raise drf_serializers.ValidationError(f"Only {room.available_rooms} rooms available")

        # Update room availability
        room.available_rooms -= num_rooms
        room.save()

        # Save reservation
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a reservation"""
        reservation = self.get_object()

        if reservation.status == 'CANCELLED':
            return Response({
                'error': 'Reservation is already cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)

        if reservation.status == 'COMPLETED':
            return Response({
                'error': 'Cannot cancel completed reservation'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update status
        reservation.status = 'CANCELLED'
        reservation.save()

        # Restore room availability
        room = reservation.room
        room.available_rooms += reservation.num_rooms
        room.save()

        return Response({
            'message': 'Reservation cancelled successfully'
        })

    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """Get current user's reservations"""
        reservations = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)


class TourViewSet(viewsets.ModelViewSet):
    """Tour management viewset"""
    queryset = Tour.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'destination', 'description']
    ordering_fields = ['start_date', 'price_per_person', 'created_at']
    ordering = ['start_date']

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return TourListSerializer
        return TourSerializer

    def get_queryset(self):
        """Filter tours based on query parameters"""
        queryset = super().get_queryset()

        # Filter by destination
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)

        # Filter by availability
        available = self.request.query_params.get('available', None)
        if available == 'true':
            queryset = queryset.filter(available_spots__gt=0, start_date__gte=date.today())

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search tours by various criteria"""
        query = request.query_params.get('q', '')
        queryset = self.get_queryset()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(destination__icontains=query) |
                Q(description__icontains=query)
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TourBookingViewSet(viewsets.ModelViewSet):
    """Tour booking management viewset"""
    queryset = TourBooking.objects.all()
    serializer_class = TourBookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Users can only see their own bookings, staff can see all"""
        if self.request.user.is_staff:
            return TourBooking.objects.all()
        return TourBooking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the user and update tour availability"""
        tour = serializer.validated_data['tour']
        num_participants = serializer.validated_data['num_participants']

        # Check availability
        if tour.available_spots < num_participants:
            raise drf_serializers.ValidationError(f"Only {tour.available_spots} spots available")

        # Update tour availability
        tour.available_spots -= num_participants
        tour.save()

        # Save booking
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a tour booking"""
        booking = self.get_object()

        if booking.status == 'CANCELLED':
            return Response({
                'error': 'Booking is already cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)

        if booking.status == 'COMPLETED':
            return Response({
                'error': 'Cannot cancel completed booking'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update status
        booking.status = 'CANCELLED'
        booking.save()

        # Restore tour availability
        tour = booking.tour
        tour.available_spots += booking.num_participants
        tour.save()

        return Response({
            'message': 'Booking cancelled successfully'
        })

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get current user's tour bookings"""
        bookings = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


# Legacy code removal - all old function-based views have been replaced with proper ViewSets
