# Trekker - Travel Booking Platform

A full-stack travel booking platform built with Django REST Framework (backend) and React (frontend). Features include hotel reservations, tour bookings, and travel blogging.

## Features

- **User Authentication**: JWT-based authentication with registration, login, and profile management
- **Hotel Bookings**: Browse hotels, view rooms, and make reservations
- **Tour Packages**: Explore and book tour packages to various destinations
- **Travel Blog**: Create, read, and interact with travel blog posts
- **User Profiles**: Manage personal information and view booking history

## Technology Stack

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Simple JWT for authentication
- SQLite (development) / PostgreSQL (production ready)
- Python 3.8+

### Frontend
- React 18.2.0
- React Router DOM 5.2.0
- Axios 1.1.2
- Bootstrap 5.2.0
- Material-UI 5.10.11

## Project Structure

```
Trekker_/
├── trekker-backend/
│   └── trekker-backend-main/
│       └── djangoApi/
│           ├── AuthenApp/          # User authentication
│           ├── EmployeeApp/        # Hotels & Tours
│           ├── PostsApp/           # Blog functionality
│           └── djangoApi/          # Main project settings
└── trekker-frontend/
    └── trekker-master/
        └── src/
            ├── components/         # React components
            └── services/           # API service layer
```

## Installation & Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd trekker-backend/trekker-backend-main/djangoApi
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from .env.example):
```bash
cp .env.example .env
```

5. Configure your `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create superuser (optional):
```bash
python manage.py createsuperuser
```

8. Run development server:
```bash
python manage.py runserver
```

Backend will be available at `http://127.0.0.1:8000/`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd trekker-frontend/trekker-master
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Configure your `.env` file:
```env
REACT_APP_API_URL=http://127.0.0.1:8000/api
```

5. Start development server:
```bash
npm start
```

Frontend will be available at `http://localhost:3000/`

## API Documentation

### Authentication Endpoints

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Hotel Endpoints

- `GET /api/hotels/` - List all hotels
- `GET /api/hotels/{id}/` - Get hotel details
- `GET /api/hotels/{id}/rooms/` - Get hotel rooms
- `POST /api/hotel-reservations/` - Create reservation
- `GET /api/hotel-reservations/my_reservations/` - Get user reservations
- `POST /api/hotel-reservations/{id}/cancel/` - Cancel reservation

### Tour Endpoints

- `GET /api/tours/` - List all tours
- `GET /api/tours/{id}/` - Get tour details
- `POST /api/tour-bookings/` - Create tour booking
- `GET /api/tour-bookings/my_bookings/` - Get user bookings
- `POST /api/tour-bookings/{id}/cancel/` - Cancel booking

### Blog Endpoints

- `GET /api/categories/` - List categories
- `GET /api/posts/` - List blog posts
- `GET /api/posts/{slug}/` - Get post details
- `POST /api/posts/` - Create post (authenticated)
- `POST /api/posts/{slug}/like/` - Like/unlike post
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create comment

### User Endpoints

- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/update_profile/` - Update profile
- `POST /api/users/upload_profile_picture/` - Upload profile picture
- `POST /api/users/change_password/` - Change password

## Frontend API Usage

The frontend includes a centralized API service layer. Example usage:

```javascript
import { authService, hotelService, tourService, blogService } from './services';

// Login
const response = await authService.login('username', 'password');

// Get hotels
const hotels = await hotelService.getAllHotels({ city: 'Paris' });

// Create hotel reservation
const reservation = await hotelService.createReservation({
  room: roomId,
  check_in: '2025-01-15',
  check_out: '2025-01-20',
  num_guests: 2,
  num_rooms: 1,
  total_price: 500.00
});

// Get tours
const tours = await tourService.getAllTours({ destination: 'Bali' });

// Get blog posts
const posts = await blogService.getAllPosts({ category: 'adventure' });
```

## Database Models

### User Profile
- Extends Django's User model
- Fields: phone, address, birthday, gender, profile_picture

### Hotel & Room
- Hotel: name, description, address, city, country, star_rating, amenities
- Room: hotel (FK), room_type, price_per_night, capacity, availability

### Tour & Booking
- Tour: name, destination, duration, price, dates, itinerary
- TourBooking: user (FK), tour (FK), participants, status

### Blog
- Category: name, slug, description
- Post: author (FK), title, body, categories (M2M), likes (M2M)
- Comment: post (FK), author (FK), content, parent (self-referencing FK)

## Security Features

- JWT token authentication
- Password hashing with Django's built-in validators
- CORS configuration
- Environment-based configuration
- Protected API endpoints
- Input validation and sanitization

## Development

### Running Tests

Backend:
```bash
cd trekker-backend/trekker-backend-main/djangoApi
python manage.py test
```

Frontend:
```bash
cd trekker-frontend/trekker-master
npm test
```

### Code Quality

Backend uses Django's built-in validation.
Frontend follows React best practices.

## Deployment

### Backend (Django)

1. Set `DEBUG=False` in production
2. Generate a new `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Set up static file serving
6. Use a WSGI server (Gunicorn recommended)

### Frontend (React)

1. Build production bundle:
```bash
npm run build
```

2. Serve the `build` folder with a web server (Nginx, Apache, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Changelog

### Version 2.0.0 (Current)
- Complete backend rewrite with Django REST Framework
- JWT authentication implementation
- Proper model relationships and validation
- Comprehensive API endpoints with ViewSets
- Centralized frontend API service layer
- Environment-based configuration
- Security improvements

### Version 1.0.0 (Legacy)
- Initial release with basic functionality
