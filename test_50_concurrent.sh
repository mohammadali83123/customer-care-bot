#!/bin/bash

# Test script for 50 concurrent requests
echo "🚀 Testing 50 concurrent requests to Customer Care Bot"
echo "====================================================="

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

echo "📊 Starting 50 concurrent requests..."
echo "Time: $(date)"

# Start timing
start_time=$(date +%s)

# Send 50 concurrent requests in background
for i in {1..50}; do
    curl -s -X POST http://localhost:8000/webhook \
        -H "Content-Type: application/json" \
        -d @test_payload.json \
        -w "Request $i: %{http_code} - %{time_total}s\n" \
        -o /dev/null &
done

# Wait for all background processes to complete
wait

# Calculate total time
end_time=$(date +%s)
total_time=$((end_time - start_time))

echo ""
echo "✅ All 50 requests completed!"
echo "⏱️  Total time: ${total_time} seconds"
echo "📈 Average time per request: $(echo "scale=2; $total_time / 50" | bc -l) seconds"
echo "🚀 Requests per second: $(echo "scale=2; 50 / $total_time" | bc -l)"

# Check worker status
echo ""
echo "🔧 Checking worker status..."
docker-compose exec worker-1 celery -A app.tasks.celery inspect active 2>/dev/null || echo "Worker status check failed"

# Check Redis queue length
echo ""
echo "📊 Redis queue status..."
docker-compose exec redis redis-cli llen celery 2>/dev/null || echo "Redis check failed"

# Clean up
rm -f test_payload.json

echo ""
echo "🎉 Test completed successfully!"
