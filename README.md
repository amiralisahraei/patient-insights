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
- Ansible deployment automation

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (if running locally)
- Ansible (for automated deployment)

## Project Structure

```
.
├── ansible/
│   ├── deploy.yml
│   ├── group_vars/
│   │   └── all.yml
│   ├── inventory.ini
│   └── roles/
│       └── app/
│           ├── tasks/
│           │   └── main.yml
│           └── templates/
│               └── your-configs.j2
├── app/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── graphql_schema.py  # GraphQL schema
│   ├── main.py           # FastAPI application
│   └── etl.py            # ETL processing script
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── sample_patients.csv
├── create_ansible_structure.sh
└── README.md
```

## Deployment Options

### Option 1: Ansible Deployment (Recommended for Production)

Deploy the application easily on your own server (e.g., AWS EC2) using Ansible automation. The deployment can be done locally or automated through GitHub Actions CI/CD.

#### Prerequisites for Ansible Deployment

- Ansible installed on your local machine
- SSH access to your target server
- Target server with Docker and Docker Compose installed

#### 1. Configure Inventory

Edit `ansible/inventory.ini` with your server details:

```ini
[servers]
your-server ansible_host=YOUR_SERVER_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/your-key.pem
```

#### 2. Deploy with Ansible

**Local Deployment:**
```bash
# Deploy the application locally
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
```

**Automated Deployment with GitHub Actions:**

The project includes automated CI/CD deployment using GitHub Actions. The deployment is triggered automatically on:
- Push to `main` or `master` branch
- Pull requests to `main` or `master` branch

To set up automated deployment:

1. **Add SSH Private Key to GitHub Secrets:**
   - Go to your repository Settings → Secrets and variables → Actions
   - Add a new secret named `SSH_PRIVATE_KEY`
   - Paste your private SSH key content

2. **Push to main/master branch:**
   ```bash
   git push origin main
   ```

The GitHub Action will automatically:
- Set up Python and install Ansible
- Configure SSH authentication
- Run the Ansible playbook to deploy your application

#### 3. Access Your Application

After successful deployment, your application will be available at:
- **API**: `http://YOUR_SERVER_IP:8000`
- **Swagger UI**: `http://YOUR_SERVER_IP:8000/docs`
- **ReDoc**: `http://YOUR_SERVER_IP:8000/redoc`

### Option 2: Local Docker Development

For local development and testing.

#### 1. Clone and Setup

```bash
git clone <your-repository>
cd <project-directory>
```

#### 2. Start MongoDB

```bash
docker compose up -d mongo db
```

#### 3. Run ETL Process

```bash
docker compose run --rm app python -m app.etl
```

#### 4. Start the Application

```bash
docker compose up app
```

The API will be available at `http://localhost:8000`

#### 5. Stop the Application

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

## Ansible Deployment Details

### What Ansible Does

The Ansible playbook automates the following tasks:

1. **System Setup**
   - Updates system packages
   - Installs Docker and Docker Compose
   - Creates application directory structure
   - Sets up firewall rules

2. **Application Deployment**
   - Copies application files to the server
   - Generates configuration files from templates
   - Builds and starts Docker containers
   - Runs ETL process initialization

3. **Service Management**
   - Configures systemd services for auto-start
   - Sets up log rotation
   - Configures health checks

### Ansible Commands Reference

```bash
# Check connectivity to servers
ansible -i ansible/inventory.ini all -m ping

# Run only specific tasks
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags "docker,app"

# Check what would be changed (dry run)
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --check

# Deploy with verbose output
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml -v

# Deploy to specific host
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --limit "your-server"
```

### Customizing Ansible Deployment

1. **Add new variables** in `ansible/group_vars/all.yml`
2. **Modify tasks** in `ansible/roles/app/tasks/main.yml`
3. **Update templates** in `ansible/roles/app/templates/`
4. **Add new roles** for additional services (monitoring, backup, etc.)

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
4. **Use HTTPS** in production (configure reverse proxy with SSL)
5. **Set appropriate CORS policies**
6. **Add rate limiting**
7. **Implement proper logging and monitoring**
8. **Configure firewall rules** (Ansible playbook includes basic setup)
9. **Regular security updates** for the server OS
10. **Use SSH key authentication** instead of passwords

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

5. **Ansible Deployment Issues**
   - Check SSH connectivity: `ansible -i ansible/inventory.ini all -m ping`
   - Verify sudo permissions on target server
   - Check Docker installation on target server
   - Review Ansible logs for specific error messages

### Logs

**Docker logs:**
```bash
docker compose logs -f app
```

**Ansible deployment logs:**
```bash
# Logs are displayed during playbook execution
# For persistent logs, check /var/log/ansible/ on control machine
```

**Server logs (after Ansible deployment):**
```bash
# Application logs
sudo journalctl -u etl-workflow -f

# System logs
sudo tail -f /var/log/syslog
```

## Monitoring and Maintenance

### Health Checks

The application includes health check endpoints:
- `GET /health` - Basic health check
- `GET /metrics` - Application metrics

### Backup Recommendations

1. **Database Backups**
   - PostgreSQL: Use `pg_dump` for regular backups
   - MongoDB: Use `mongodump` for regular backups

2. **Application Backups**
   - Backup configuration files
   - Backup uploaded data files
   - Version control your infrastructure code

### Updates and Maintenance

1. **Application Updates**
   ```bash
   # Update application code
   ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags "app"
   ```

2. **System Updates**
   ```bash
   # Update system packages
   ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags "system"
   ```

