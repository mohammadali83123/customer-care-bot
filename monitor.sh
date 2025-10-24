#!/bin/bash

# Monitoring script for Customer Care Bot
# Provides real-time monitoring of the scaled system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}  Customer Care Bot Monitor     ${NC}"
    echo -e "${CYAN}================================${NC}"
    echo ""
}

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

# Check service health
check_service_health() {
    print_header
    print_status "Checking service health..."
    
    # Check Docker containers
    echo "🐳 Docker Container Status:"
    docker-compose ps
    
    echo ""
    
    # Check Redis
    print_status "Checking Redis..."
    if docker-compose exec redis redis-cli ping | grep -q "PONG"; then
        print_success "Redis is healthy"
    else
        print_error "Redis is not responding"
    fi
    
    # Check web services
    print_status "Checking web services..."
    if curl -f http://localhost/ > /dev/null 2>&1; then
        print_success "Web services are accessible"
    else
        print_error "Web services are not accessible"
    fi
    
    # Check Flower monitoring
    print_status "Checking Flower monitoring..."
    if curl -f http://localhost:5555/ > /dev/null 2>&1; then
        print_success "Flower monitoring is accessible at http://localhost:5555"
    else
        print_warning "Flower monitoring is not accessible"
    fi
}

# Monitor Celery workers
monitor_celery_workers() {
    print_status "Celery Worker Status:"
    echo "======================"
    
    # Get active workers
    echo "Active Workers:"
    docker-compose exec worker-1 celery -A app.tasks.celery inspect active 2>/dev/null || echo "No active workers"
    
    echo ""
    echo "Worker Statistics:"
    docker-compose exec worker-1 celery -A app.tasks.celery inspect stats 2>/dev/null || echo "Unable to get worker statistics"
    
    echo ""
    echo "Registered Tasks:"
    docker-compose exec worker-1 celery -A app.tasks.celery inspect registered 2>/dev/null || echo "Unable to get registered tasks"
}

# Monitor Redis
monitor_redis() {
    print_status "Redis Status:"
    echo "=============="
    
    # Memory usage
    echo "Memory Usage:"
    docker-compose exec redis redis-cli info memory | grep -E "(used_memory_human|maxmemory_human|used_memory_peak_human)"
    
    echo ""
    echo "Connection Info:"
    docker-compose exec redis redis-cli info clients | grep -E "(connected_clients|blocked_clients)"
    
    echo ""
    echo "Key Statistics:"
    docker-compose exec redis redis-cli info keyspace
}

# Monitor system resources
monitor_system_resources() {
    print_status "System Resource Usage:"
    echo "=========================="
    
    # Docker container stats
    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
    
    echo ""
    echo "Disk Usage:"
    df -h | grep -E "(Filesystem|/dev/)"
}

# Monitor API health
monitor_api_health() {
    print_status "API Health Check:"
    echo "==================="
    
    # Test mock APIs
    echo "Mock API 1 (Customer Registration):"
    if curl -f http://localhost:8001/endpoint/1234567890 > /dev/null 2>&1; then
        print_success "  ✅ Mock API 1 is healthy"
    else
        print_error "  ❌ Mock API 1 is not responding"
    fi
    
    echo "Mock API 2 (Customer Orders):"
    if curl -f -X POST http://localhost:8002/endpoint -H "Content-Type: application/json" -d '{"store_number":"1234567890"}' > /dev/null 2>&1; then
        print_success "  ✅ Mock API 2 is healthy"
    else
        print_error "  ❌ Mock API 2 is not responding"
    fi
}

# Monitor queue status
monitor_queue_status() {
    print_status "Queue Status:"
    echo "=============="
    
    # Check queue length
    echo "Queue Length:"
    docker-compose exec redis redis-cli llen celery
    
    echo ""
    echo "Queue Contents (first 10 items):"
    docker-compose exec redis redis-cli lrange celery 0 9
}

# Monitor workflow execution
monitor_workflow_execution() {
    print_status "Workflow Execution Monitor:"
    echo "==============================="
    
    # Test a single workflow
    echo "Testing single workflow execution..."
    
    # Create test payload
    cat > monitor_test.json << EOF
{
    "customer_id": "monitor_test",
    "customer_phone_number": "+1234567890",
    "event": {
        "message": "monitoring test"
    }
}
EOF
    
    # Execute test workflow
    start_time=$(date +%s)
    response=$(curl -s -X POST http://localhost/webhook \
        -H "Content-Type: application/json" \
        -d @monitor_test.json)
    end_time=$(date +%s)
    
    execution_time=$((end_time - start_time))
    
    if echo "$response" | grep -q "accepted"; then
        print_success "Workflow queued successfully (${execution_time}s)"
    else
        print_error "Workflow queuing failed"
        echo "Response: $response"
    fi
    
    # Clean up
    rm -f monitor_test.json
}

# Show real-time monitoring
show_realtime_monitoring() {
    print_status "Real-time Monitoring (Press Ctrl+C to stop):"
    echo "=================================================="
    
    while true; do
        clear
        print_header
        
        # Service health
        check_service_health
        
        echo ""
        
        # Celery workers
        monitor_celery_workers
        
        echo ""
        
        # Redis status
        monitor_redis
        
        echo ""
        
        # System resources
        monitor_system_resources
        
        echo ""
        print_status "Press Ctrl+C to stop monitoring"
        sleep 5
    done
}

# Show monitoring dashboard
show_dashboard() {
    print_header
    
    echo "📊 Monitoring Dashboard"
    echo "======================"
    echo ""
    echo "🌐 Web Application: http://localhost"
    echo "📈 Flower Monitoring: http://localhost:5555"
    echo "🔧 Redis: localhost:6379"
    echo "🧪 Mock APIs: localhost:8001, localhost:8002"
    echo ""
    echo "📋 Available Commands:"
    echo "  ./monitor.sh health    - Check service health"
    echo "  ./monitor.sh workers   - Monitor Celery workers"
    echo "  ./monitor.sh redis     - Monitor Redis"
    echo "  ./monitor.sh resources - Monitor system resources"
    echo "  ./monitor.sh realtime  - Real-time monitoring"
    echo "  ./monitor.sh test      - Test workflow execution"
    echo ""
}

# Main function
main() {
    case "${1:-dashboard}" in
        "health")
            check_service_health
            ;;
        "workers")
            monitor_celery_workers
            ;;
        "redis")
            monitor_redis
            ;;
        "resources")
            monitor_system_resources
            ;;
        "realtime")
            show_realtime_monitoring
            ;;
        "test")
            monitor_workflow_execution
            ;;
        "dashboard"|"")
            show_dashboard
            ;;
        *)
            echo "Usage: $0 [health|workers|redis|resources|realtime|test|dashboard]"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
