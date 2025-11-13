from rest_framework import serializers
from .models import Hotel, Room, HotelReservation, Tour, TourBooking


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'hotel', 'hotel_name', 'room_type', 'description', 'price_per_night',
                  'capacity', 'total_rooms', 'available_rooms', 'image']
        read_only_fields = ['id']


class HotelSerializer(serializers.ModelSerializer):
    """Serializer for Hotel model"""
    rooms = RoomSerializer(many=True, read_only=True)
    amenities_list = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'address', 'city', 'country', 'star_rating',
                  'amenities', 'amenities_list', 'image', 'phone', 'email', 'created_at',
                  'updated_at', 'is_active', 'rooms']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_amenities_list(self, obj):
        """Convert comma-separated amenities to list"""
        if obj.amenities:
            return [amenity.strip() for amenity in obj.amenities.split(',')]
        return []


class HotelListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for hotel listings"""
    amenities_list = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'city', 'country', 'star_rating',
                  'amenities_list', 'image', 'is_active', 'min_price']

    def get_amenities_list(self, obj):
        if obj.amenities:
            return [amenity.strip() for amenity in obj.amenities.split(',')]
        return []

    def get_min_price(self, obj):
        """Get minimum room price for the hotel"""
        rooms = obj.rooms.filter(available_rooms__gt=0)
        if rooms.exists():
            return min(room.price_per_night for room in rooms)
        return None


class HotelReservationSerializer(serializers.ModelSerializer):
    """Serializer for Hotel Reservation"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    hotel_name = serializers.CharField(source='room.hotel.name', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)

    class Meta:
        model = HotelReservation
        fields = ['id', 'user', 'user_name', 'room', 'hotel_name', 'room_type', 'check_in',
                  'check_out', 'num_guests', 'num_rooms', 'total_price', 'status',
                  'special_requests', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate reservation data"""
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')

        if check_out <= check_in:
            raise serializers.ValidationError("Check-out date must be after check-in date.")

        room = attrs.get('room')
        num_rooms = attrs.get('num_rooms')

        if room and num_rooms > room.available_rooms:
            raise serializers.ValidationError(f"Only {room.available_rooms} rooms available.")

        return attrs


class TourSerializer(serializers.ModelSerializer):
    """Serializer for Tour model"""
    included_services_list = serializers.SerializerMethodField()
    available = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ['id', 'name', 'description', 'destination', 'duration_days', 'price_per_person',
                  'max_participants', 'available_spots', 'start_date', 'end_date', 'itinerary',
                  'included_services', 'included_services_list', 'image', 'is_active', 'available',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_included_services_list(self, obj):
        """Convert comma-separated services to list"""
        if obj.included_services:
            return [service.strip() for service in obj.included_services.split(',')]
        return []

    def get_available(self, obj):
        """Check if tour has available spots"""
        return obj.available_spots > 0


class TourListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for tour listings"""
    included_services_list = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ['id', 'name', 'description', 'destination', 'duration_days', 'price_per_person',
                  'available_spots', 'start_date', 'end_date', 'included_services_list', 'image', 'is_active']

    def get_included_services_list(self, obj):
        if obj.included_services:
            return [service.strip() for service in obj.included_services.split(',')][:3]  # First 3 services
        return []


class TourBookingSerializer(serializers.ModelSerializer):
    """Serializer for Tour Booking"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    tour_name = serializers.CharField(source='tour.name', read_only=True)
    tour_destination = serializers.CharField(source='tour.destination', read_only=True)

    class Meta:
        model = TourBooking
        fields = ['id', 'user', 'user_name', 'tour', 'tour_name', 'tour_destination',
                  'num_participants', 'total_price', 'status', 'special_requests',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate booking data"""
        tour = attrs.get('tour')
        num_participants = attrs.get('num_participants')

        if tour and num_participants > tour.available_spots:
            raise serializers.ValidationError(f"Only {tour.available_spots} spots available for this tour.")

        return attrs