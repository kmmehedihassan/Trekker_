from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Hotel(models.Model):
    """Hotel information and details"""
    STAR_RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    star_rating = models.IntegerField(choices=STAR_RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    amenities = models.TextField(help_text="Comma-separated list of amenities")
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ['-created_at']


class Room(models.Model):
    """Hotel room types and availability"""
    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
        ('DELUXE', 'Deluxe'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    total_rooms = models.IntegerField(validators=[MinValueValidator(1)])
    available_rooms = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class HotelReservation(models.Model):
    """Hotel booking reservations"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotel_reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField(validators=[MinValueValidator(1)])
    num_rooms = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.hotel.name} ({self.check_in} to {self.check_out})"

    class Meta:
        verbose_name = 'Hotel Reservation'
        verbose_name_plural = 'Hotel Reservations'
        ordering = ['-created_at']


class Tour(models.Model):
    """Tour packages and information"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    destination = models.CharField(max_length=200)
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    max_participants = models.IntegerField(validators=[MinValueValidator(1)])
    available_spots = models.IntegerField(validators=[MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField()
    itinerary = models.TextField()
    included_services = models.TextField(help_text="Comma-separated list of included services")
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.destination}"

    class Meta:
        verbose_name = 'Tour'
        verbose_name_plural = 'Tours'
        ordering = ['start_date']


class TourBooking(models.Model):
    """Tour booking records"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_bookings')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    num_participants = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"

    class Meta:
        verbose_name = 'Tour Booking'
        verbose_name_plural = 'Tour Bookings'
        ordering = ['-created_at']
