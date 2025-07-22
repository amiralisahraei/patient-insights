# Automated ETL Workflow

A FastAPI application with JWT authentication that manages patient data using PostgreSQL and MongoDB for reports, with GraphQL support.

## Features

- JWT-based authentication
- Patient data management (PostgreSQL)
- Report storage (MongoDB)
- GraphQL endpoint
- RESTful API endpoints
- Docker containerization
- ETL data processing

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (if running locally)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── graphql_schema.py  # GraphQL schema
│   └── etl.py            # ETL processing script
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repository>
cd <project-directory>
```

### 2. Start MongoDB

```bash
docker compose up -d mongo db
```

### 3. Run ETL Process

```bash
docker compose run --rm app python -m app.etl
```

### 4. Start the Application

```bash
docker compose up app
```

The API will be available at `http://localhost:8000`

### 5. Stop the Application

```bash
docker compose down
```

## Authentication

### Default Credentials

- **Username**: `admin`
- **Password**: `password123`

### Getting an Access Token

**Using curl:**
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=password123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## API Endpoints

### Authentication
- `POST /token` - Login and get JWT token

### Protected Endpoints (Require JWT Token)
- `GET /patients` - Get all patients
- `GET /patients/{patient_id}` - Get specific patient
- `GET /patients/{patient_id}/report` - Get patient report
- `GET /metrics` - Get API metrics

### GraphQL
- `POST /graphql` - GraphQL endpoint

## Using Protected Endpoints

Include the JWT token in the Authorization header:

```bash
curl -X GET "http://localhost:8000/patients" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## API Documentation

Once the application is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/patients_db
MONGO_URL=mongodb://mongo:27017

# JWT Configuration
SECRET_KEY=your_super_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Docker Commands Reference

```bash
# Start MongoDB and PostgreSQL
docker compose up -d mongo db

# Run ETL process
docker compose run --rm app python -m app.etl

# Start the FastAPI application
docker compose up app

# Start all services in detached mode
docker compose up -d

# View logs
docker compose logs app

# Stop all services
docker compose down

# Rebuild and start
docker compose up --build app

# Remove all containers and volumes
docker compose down -v
```

## Development

### Local Development Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export DATABASE_URL="postgresql://localhost:5432/patients_db"
export MONGO_URL="mongodb://localhost:27017"
```

3. **Run the application:**
```bash
uvicorn app.main:app --reload
```

### Adding New Users

Currently using a dummy user system. To add more users, modify the `fake_user` dictionary in the main application file or implement a proper user management system.

## Security Notes

⚠️ **Important for Production:**

1. **Change the SECRET_KEY** - Use a strong, randomly generated secret key
2. **Use environment variables** for sensitive configuration
3. **Implement proper user management** instead of the dummy user system
4. **Use HTTPS** in production
5. **Set appropriate CORS policies**
6. **Add rate limiting**
7. **Implement proper logging and monitoring**

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL and MongoDB containers are running
   - Check connection strings in environment variables

2. **Authentication Errors**
   - Verify JWT token is correctly included in Authorization header
   - Check if token has expired (default: 30 minutes)

3. **ETL Process Fails**
   - Ensure database containers are running before ETL
   - Check data source availability

4. **Port Conflicts**
   - Default ports: FastAPI (8000), PostgreSQL (5432), MongoDB (27017)
   - Modify docker-compose.yml if ports are in use

### Logs

View application logs:
```bash
docker compose logs -f app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions:
- Check the troubleshooting section
- Review the API documentation at `/docs`
- Create an issue in the repository