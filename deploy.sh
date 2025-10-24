#!/bin/bash

# Production deployment script for Customer Care Bot
# Handles 50 concurrent workflows with optimized scaling

set -e

echo "🚀 Starting Customer Care Bot Production Deployment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is running"
}

# Check if Docker Compose is available
check_docker_compose() {
    print_status "Checking Docker Compose..."
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
    
    print_success "Docker Compose is available"
}

# Create environment file if it doesn't exist
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file with default values..."
        cat > .env << EOF
# Redis Configuration
REDIS_URL=redis://redis:6379/0

# API Configuration
CHECK_CUSTOMER_REGISTRATION_API_URL=http://mock-api-1:8001/endpoint
FETCH_CUSTOMER_ORDERS_API_URL=http://mock-api-2:8002/endpoint

# Authentication
ACCESS_TOKEN=your_access_token_here

# Production Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
EOF
        print_warning "Please update .env file with your actual API URLs and access token"
    else
        print_success ".env file already exists"
    fi
}

# Build and start services
deploy_services() {
    print_status "Building and starting services..."
    
    # Stop existing services
    print_status "Stopping existing services..."
    docker-compose down --remove-orphans || true
    
    # Build images
    print_status "Building Docker images..."
    docker-compose build --no-cache
    
    # Start services
    print_status "Starting services..."
    docker-compose up -d
    
    print_success "Services started successfully"
}

# Wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to be healthy..."
    
    # Wait for Redis
    print_status "Waiting for Redis..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
            print_success "Redis is healthy"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Redis failed to start within 60 seconds"
        exit 1
    fi
    
    # Wait for web services
    print_status "Waiting for web services..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost/ > /dev/null 2>&1; then
            print_success "Web services are healthy"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Web services failed to start within 60 seconds"
        exit 1
    fi
}

# Show service status
show_status() {
    print_status "Service Status:"
    echo "=================="
    
    # Show running containers
    docker-compose ps
    
    echo ""
    print_status "Service URLs:"
    echo "=============="
    echo "🌐 Main Application: http://localhost"
    echo "📊 Flower Monitoring: http://localhost:5555"
    echo "🔧 Redis: localhost:6379"
    echo "🧪 Mock API 1: http://localhost:8001"
    echo "🧪 Mock API 2: http://localhost:8002"
    
    echo ""
    print_status "Worker Status:"
    echo "==============="
    docker-compose exec worker-1 celery -A app.tasks.celery inspect active || true
}

# Run load test
run_load_test() {
    print_status "Running load test to verify 50 concurrent workflows..."
    
    # Create test payload
    cat > test_payload.json << EOF
{
    "customer_id": "test_customer",
    "customer_phone_number": "+1234567890",
    "event": {
        "message": "test message"
    }
}
EOF
    
    # Check if ab (Apache Bench) is available
    if command -v ab &> /dev/null; then
        print_status "Running Apache Bench load test..."
        ab -n 100 -c 50 -p test_payload.json -T application/json http://localhost/webhook
    else
        print_warning "Apache Bench not available. Install with: brew install httpd (macOS) or apt-get install apache2-utils (Ubuntu)"
        print_status "Manual test: Send 50 concurrent requests to http://localhost/webhook"
    fi
    
    # Clean up
    rm -f test_payload.json
}

# Main deployment function
main() {
    echo "🎯 Deploying Customer Care Bot for 50 Concurrent Workflows"
    echo "========================================================="
    echo ""
    
    check_docker
    check_docker_compose
    create_env_file
    deploy_services
    wait_for_services
    show_status
    
    echo ""
    print_success "🚀 Deployment completed successfully!"
    echo ""
    print_status "Your Customer Care Bot is now running with:"
    echo "• 5 Celery workers with 10 concurrency each = 50 concurrent workflows"
    echo "• 3 FastAPI instances with load balancing"
    echo "• Optimized Redis with persistence"
    echo "• Nginx load balancer with rate limiting"
    echo "• HTTP connection pooling for external APIs"
    echo ""
    print_status "Next steps:"
    echo "1. Update .env file with your actual API URLs and access token"
    echo "2. Test the system with: ./test.sh"
    echo "3. Monitor with Flower: http://localhost:5555"
    echo ""
    
    # Ask if user wants to run load test
    read -p "Would you like to run a load test? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_load_test
    fi
}

# Run main function
main "$@"
