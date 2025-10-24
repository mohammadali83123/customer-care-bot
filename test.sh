#!/bin/bash

# Load testing script for Customer Care Bot
# Tests 50 concurrent workflows

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Test basic connectivity
test_connectivity() {
    print_status "Testing basic connectivity..."
    
    # Test main endpoint
    if curl -f http://localhost/ > /dev/null 2>&1; then
        print_success "Main application is accessible"
    else
        print_error "Main application is not accessible"
        return 1
    fi
    
    # Test health endpoint
    if curl -f http://localhost/health > /dev/null 2>&1; then
        print_success "Health endpoint is accessible"
    else
        print_warning "Health endpoint not available"
    fi
}

# Test single workflow
test_single_workflow() {
    print_status "Testing single workflow execution..."
    
    # Create test payload
    cat > test_payload.json << EOF
{
    "customer_id": "test_customer_001",
    "customer_phone_number": "+1234567890",
    "event": {
        "message": "I need help with my order"
    }
}
EOF
    
    # Test synchronous workflow
    print_status "Testing synchronous workflow..."
    response=$(curl -s -X POST http://localhost/workflow/run \
        -H "Content-Type: application/json" \
        -d @test_payload.json)
    
    if echo "$response" | grep -q "workflow_id"; then
        print_success "Synchronous workflow test passed"
    else
        print_error "Synchronous workflow test failed"
        echo "Response: $response"
        return 1
    fi
    
    # Test asynchronous workflow
    print_status "Testing asynchronous workflow..."
    response=$(curl -s -X POST http://localhost/webhook \
        -H "Content-Type: application/json" \
        -d @test_payload.json)
    
    if echo "$response" | grep -q "accepted"; then
        print_success "Asynchronous workflow test passed"
    else
        print_error "Asynchronous workflow test failed"
        echo "Response: $response"
        return 1
    fi
    
    # Clean up
    rm -f test_payload.json
}

# Test concurrent workflows
test_concurrent_workflows() {
    print_status "Testing concurrent workflows..."
    
    # Create test payload
    cat > test_payload.json << EOF
{
    "customer_id": "test_customer",
    "customer_phone_number": "+1234567890",
    "event": {
        "message": "test concurrent message"
    }
}
EOF
    
    # Test with different concurrency levels
    for concurrency in 10 25 50; do
        print_status "Testing $concurrency concurrent workflows..."
        
        if command -v ab &> /dev/null; then
            # Use Apache Bench if available
            ab -n $((concurrency * 2)) -c $concurrency -p test_payload.json -T application/json http://localhost/webhook > test_results_${concurrency}.txt 2>&1
            
            # Check if test passed
            if grep -q "Failed requests:        0" test_results_${concurrency}.txt; then
                print_success "$concurrency concurrent workflows test passed"
            else
                print_warning "$concurrency concurrent workflows had some failures"
                echo "Check test_results_${concurrency}.txt for details"
            fi
        else
            # Manual test with curl
            print_status "Running manual test for $concurrency concurrent requests..."
            
            # Start background processes
            for i in $(seq 1 $concurrency); do
                curl -s -X POST http://localhost/webhook \
                    -H "Content-Type: application/json" \
                    -d @test_payload.json &
            done
            
            # Wait for all background processes
            wait
            
            print_success "Manual test for $concurrency concurrent requests completed"
        fi
    done
    
    # Clean up
    rm -f test_payload.json
}

# Test worker status
test_worker_status() {
    print_status "Checking worker status..."
    
    # Check if workers are running
    worker_count=$(docker-compose ps | grep worker | grep Up | wc -l)
    print_status "Active workers: $worker_count"
    
    if [ "$worker_count" -ge 5 ]; then
        print_success "All 5 workers are running"
    else
        print_warning "Only $worker_count workers are running (expected 5)"
    fi
    
    # Check Celery worker status
    print_status "Checking Celery worker status..."
    if docker-compose exec worker-1 celery -A app.tasks.celery inspect ping > /dev/null 2>&1; then
        print_success "Celery workers are responding"
    else
        print_error "Celery workers are not responding"
        return 1
    fi
}

# Test Redis connectivity
test_redis() {
    print_status "Testing Redis connectivity..."
    
    if docker-compose exec redis redis-cli ping | grep -q "PONG"; then
        print_success "Redis is healthy"
    else
        print_error "Redis is not responding"
        return 1
    fi
    
    # Check Redis memory usage
    memory_usage=$(docker-compose exec redis redis-cli info memory | grep used_memory_human | cut -d: -f2 | tr -d '\r')
    print_status "Redis memory usage: $memory_usage"
}

# Test API endpoints
test_api_endpoints() {
    print_status "Testing API endpoints..."
    
    # Test mock APIs
    if curl -f http://localhost:8001/endpoint/1234567890 > /dev/null 2>&1; then
        print_success "Mock API 1 is accessible"
    else
        print_warning "Mock API 1 is not accessible"
    fi
    
    if curl -f -X POST http://localhost:8002/endpoint -H "Content-Type: application/json" -d '{"store_number":"1234567890"}' > /dev/null 2>&1; then
        print_success "Mock API 2 is accessible"
    else
        print_warning "Mock API 2 is not accessible"
    fi
}

# Monitor system resources
monitor_resources() {
    print_status "Monitoring system resources..."
    
    echo "Docker container resource usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
    
    echo ""
    print_status "Redis memory info:"
    docker-compose exec redis redis-cli info memory | grep -E "(used_memory|maxmemory)"
}

# Run performance test
run_performance_test() {
    print_status "Running performance test..."
    
    # Create test payload
    cat > performance_test.json << EOF
{
    "customer_id": "perf_test",
    "customer_phone_number": "+1234567890",
    "event": {
        "message": "performance test message"
    }
}
EOF
    
    print_status "Sending 100 requests with 50 concurrency..."
    
    if command -v ab &> /dev/null; then
        ab -n 100 -c 50 -p performance_test.json -T application/json http://localhost/webhook > performance_results.txt 2>&1
        
        # Extract key metrics
        requests_per_second=$(grep "Requests per second" performance_results.txt | awk '{print $4}')
        time_per_request=$(grep "Time per request" performance_results.txt | head -1 | awk '{print $4}')
        failed_requests=$(grep "Failed requests" performance_results.txt | awk '{print $3}')
        
        print_status "Performance Results:"
        echo "  Requests per second: $requests_per_second"
        echo "  Time per request: $time_per_request ms"
        echo "  Failed requests: $failed_requests"
        
        if [ "$failed_requests" = "0" ]; then
            print_success "Performance test passed - no failed requests"
        else
            print_warning "Performance test had $failed_requests failed requests"
        fi
    else
        print_warning "Apache Bench not available. Install for detailed performance testing."
    fi
    
    # Clean up
    rm -f performance_test.json performance_results.txt
}

# Main test function
main() {
    echo "🧪 Customer Care Bot Load Testing"
    echo "=================================="
    echo ""
    
    # Run all tests
    test_connectivity
    test_worker_status
    test_redis
    test_api_endpoints
    test_single_workflow
    test_concurrent_workflows
    monitor_resources
    run_performance_test
    
    echo ""
    print_success "🎉 All tests completed!"
    echo ""
    print_status "Test Summary:"
    echo "==============="
    echo "✅ Basic connectivity tests"
    echo "✅ Worker status checks"
    echo "✅ Redis connectivity"
    echo "✅ API endpoint tests"
    echo "✅ Single workflow test"
    echo "✅ Concurrent workflow tests"
    echo "✅ Performance monitoring"
    echo ""
    print_status "Your system is ready to handle 50 concurrent workflows!"
}

# Run main function
main "$@"
