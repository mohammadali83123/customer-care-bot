#!/bin/bash

echo "🧪 Comprehensive Customer Care Bot Test"
echo "======================================="

# Create test payload
cat > test_payload.json << EOF
{
    "customer_id": "test_customer",
    "customer_phone_number": "+1234567890",
    "event": {
        "message": "I need help with my order status"
    }
}
EOF

echo "📊 Test 1: Single Workflow Test"
echo "==============================="
start_time=$(date +%s)
response=$(curl -s -X POST http://localhost:8000/webhook -H "Content-Type: application/json" -d @test_payload.json)
echo "Response: $response"
end_time=$(date +%s)
echo "Time taken: $((end_time - start_time)) seconds"

echo ""
echo "📊 Test 2: 10 Concurrent Requests"
echo "================================="
start_time=$(date +%s)
for i in {1..10}; do
    curl -s -X POST http://localhost:8000/webhook -H "Content-Type: application/json" -d @test_payload.json &
done
wait
end_time=$(date +%s)
echo "10 concurrent requests completed in $((end_time - start_time)) seconds"

echo ""
echo "📊 Test 3: 25 Concurrent Requests"
echo "================================="
start_time=$(date +%s)
for i in {1..25}; do
    curl -s -X POST http://localhost:8000/webhook -H "Content-Type: application/json" -d @test_payload.json &
done
wait
end_time=$(date +%s)
echo "25 concurrent requests completed in $((end_time - start_time)) seconds"

echo ""
echo "📊 Test 4: 50 Concurrent Requests"
echo "================================="
start_time=$(date +%s)
for i in {1..50}; do
    curl -s -X POST http://localhost:8000/webhook -H "Content-Type: application/json" -d @test_payload.json &
done
wait
end_time=$(date +%s)
echo "50 concurrent requests completed in $((end_time - start_time)) seconds"

echo ""
echo "📊 System Status:"
echo "================="
echo "Docker containers:"
docker-compose ps

echo ""
echo "Redis queue length:"
docker-compose exec redis redis-cli llen celery 2>/dev/null || echo "Redis check failed"

echo ""
echo "Worker logs (last 5 tasks):"
docker-compose logs worker --tail=20 | grep "Task.*succeeded" | tail -5

echo ""
echo "Resource usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Clean up
rm -f test_payload.json

echo ""
echo "🎉 Comprehensive test completed!"
