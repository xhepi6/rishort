# RiShort - URL Shortener

RiShort is a modern URL shortener service built with FastAPI, Next.js, and Redis.

## Prerequisites

- Docker
- Docker Compose

## How URL Shortening Works

RiShort uses a robust approach to generate and manage shortened URLs:

1. **Short Code Generation**:
   - When a long URL is submitted, a unique 6-character code is generated
   - The code combines a timestamp-based hash and URL-specific elements
   - This ensures uniqueness while keeping codes short and readable

2. **Storage and Retrieval**:
   - URLs are stored in Redis with a 24-hour expiration
   - Each shortened URL is automatically removed after 24 hours
   - Fast lookups and redirects using Redis as the backend store
   - When a shortened URL is accessed, the system looks up the original URL using the code
   - Redirects are handled using HTTP 307 (Temporary Redirect) status

3. **URL Format**:
   ```
   Original: https://very-long-website.com/with/many/parameters?id=123
   Shortened: http://localhost:8000/abc123
   ```

4. **Features**:
   - Validation of input URLs
   - Consistent length short codes (6 characters)
   - Case-sensitive codes for increased uniqueness
   - 24-hour expiration for all shortened URLs
   - Redis-backed storage for high performance
   - Load balanced in production setup

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/xhepi6/rishort
cd rishort
```

2. Set up environment variables:

For the backend:
```bash
cd back
cp .env.example .env
```

For the frontend:
```bash
cd front
cp .env.example .env
```

3. Run the application:

For development:
```bash
docker-compose up --build
```

For production:
```bash
docker-compose -f docker-compose.production.yml up --build
```

The application will be available at:
- Development:
  - Frontend: http://localhost:3000
  - Backend API: http://localhost:8000
- Production:
  - Frontend & API: https://your-domain.com

## Environment Variables

### Backend (.env)
```env
# Redis Settings
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_strong_password_here
REDIS_USERNAME=default
REDIS_DB=0

# CORS Settings
CORS_ORIGINS=http://localhost:3000,https://productionurl.com

# Base URL for shortened links
BASE_URL=http://localhost:8000/
```

### Frontend (.env)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development vs Production

### Development Setup
- Hot reloading for both frontend and backend
- Volume mounting for local development
- Redis without authentication
- Direct service access

### Production Setup
- Nginx reverse proxy with SSL termination
- Load balancing for backend services
- Redis with password authentication
- Automatic SSL certificate management with Certbot
- Health checks for all services
- Resource limits and monitoring
- Multiple backend instances for high availability

## Features

- Create shortened URLs with 24-hour expiration
- Access original URLs through shortened links
- Copy shortened URLs to clipboard
- Visual feedback for URL expiration time
- Responsive design
- Environment-based configuration
- Load balanced backend
- Secure Redis storage
- SSL/TLS support in production

## Tech Stack

- **Frontend**: Next.js, React, TailwindCSS
- **Backend**: FastAPI, Python, Redis
- **Infrastructure**: Docker, Docker Compose, Nginx
- **Security**: Certbot, SSL/TLS
- **Monitoring**: Health checks, Resource limits

## License

[MIT](https://choosealicense.com/licenses/mit/)
