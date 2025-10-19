# Workflow Structure Documentation

## Project Structure

```
customer-care-bot/
├── app/
│   ├── workflow/                    # ⭐ NEW: Modular workflow system
│   │   ├── __init__.py             # Package exports
│   │   ├── workflow_manager.py     # Main orchestrator (150 lines)
│   │   ├── visualizer.py           # Visualization engine (200 lines)
│   │   └── steps/                  # Individual step modules
│   │       ├── __init__.py
│   │       ├── step_1.py           # Webhook trigger
│   │       ├── step_2.py           # Initialize globals
│   │       ├── step_3.py           # Call Internal API 1
│   │       ├── step_4.py           # Set globals after API1
│   │       ├── step_5.py           # Call Internal API 2
│   │       ├── step_6.py           # Set final context
│   │       ├── step_7.py           # Run agent
│   │       ├── step_8.py           # Conditional routing
│   │       └── step_9.py           # Terminate
│   ├── services/
│   │   ├── agent.py               # Agentic response logic
│   │   └── apis.py                # External API calls
│   ├── config.py                  # Settings (Pydantic v2)
│   ├── main.py                    # FastAPI app with visualization endpoints
│   ├── models.py                  # Data models
│   └── tasks.py                   # Celery task definitions
├── tests/
│   ├── test_workflow.py           # Workflow tests
│   ├── mock_api1.py               # Mock API 1 for Docker
│   └── mock_api2.py               # Mock API 2 for Docker
├── demo_visualization.py          # ⭐ NEW: Visualization demo script
├── VISUALIZATION.md               # ⭐ NEW: Visualization documentation
├── docker-compose.yml             # 5 services (redis, mock APIs, web, worker)
├── Dockerfile                     # Container definition
└── requirements.txt               # Python dependencies
```

## Workflow Architecture

### Before Refactoring
```
app/workflow.py (80 lines)
  └─ All steps in one monolithic function
```

### After Refactoring
```
app/workflow/
├── workflow_manager.py          # Orchestration logic
├── visualizer.py                # Visualization system
└── steps/
    ├── step_1.py ... step_9.py  # Individual, testable modules
```

## Workflow Execution Flow

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Webhook Triggered          (Step 1)                       │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│ 2. Initialize Globals         (Step 2)                       │
│    - Set user_id                                             │
│    - Store event data                                        │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│ 3. Call Internal API 1        (Step 3)                       │
│    - POST to internal-api-1                                  │
│    - Store response in globals                               │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│ 4. Transform API1 Data        (Step 4)                       │
│    - Extract values                                          │
│    - Set intermediate_value                                  │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│ 5. Call Internal API 2        (Step 5)                       │
│    - POST to internal-api-2                                  │
│    - Use intermediate_value as context                       │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│ 6. Set Final Context          (Step 6)                       │
│    - Combine api1 + api2 responses                           │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│ 7. Run Agent                  (Step 7)                       │
│    - Analyze user message                                    │
│    - Determine intent & action                               │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│ 8. Conditional Routing        (Step 8)                       │
│                                                               │
│    ┌─────────────┬──────────────┬─────────────┐             │
│    │             │              │             │             │
│    ▼             ▼              ▼             │             │
│  refund?    order status?   general query    │             │
│    │             │              │             │             │
│    ▼             ▼              ▼             │             │
│ route_to_   order_status_  auto_responded    │             │
│  refunds      returned                        │             │
│                                               │             │
└───────────────────────────────────────────────┼─────────────┘
                                                │
┌───────────────────────────────────────────────▼─────────────┐
│ 9. Terminate                  (Step 9)                       │
│    - Log completion                                          │
│    - Return results with visualization                       │
└──────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Modular Design
- Each step is a separate, testable module
- Easy to add, remove, or modify steps
- Clear separation of concerns

### 2. Dynamic Visualization
- Real-time execution tracking
- Multiple export formats:
  - ASCII tree with Unicode characters
  - Mermaid flowchart syntax
  - JSON structured data
  - Simple indented tree
- Performance metrics per step
- Branch tracking for conditional logic

### 3. Error Handling
- Graceful failure at each step
- Detailed error messages
- Visualization shows where failures occur

### 4. Extensibility
- Add new steps by creating new files
- Register in workflow_manager.py
- Inherit visualization automatically

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/webhook` | POST | Queue workflow asynchronously (Celery) |
| `/workflow/run` | POST | Run workflow synchronously with full results |
| `/workflow/visualize` | POST | Get ASCII tree visualization only |
| `/workflow/diagram` | POST | Get Mermaid diagram for rendering |
| `/` | GET | API information |

## Usage Examples

### 1. Queue Workflow (Production)
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "event": {"message": "refund please"}}'
```

### 2. Run with Visualization (Debugging)
```bash
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "event": {"message": "where is my order?"}}' | jq .
```

### 3. View Tree
```bash
curl -X POST http://localhost:8000/workflow/visualize \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "event": {"message": "hello"}}'
```

### 4. Generate Diagram
```bash
curl -X POST http://localhost:8000/workflow/diagram \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "event": {"message": "help"}}' > diagram.mmd

# Open https://mermaid.live and paste diagram.mmd
```

## Running the Demo

```bash
# Activate virtual environment
source venv/bin/activate

# Run visualization demo
python demo_visualization.py
```

Output shows:
- 3 different scenarios (order status, refund, general)
- Full visualization trees
- Branch routing information
- Performance metrics
- Mermaid diagram syntax
- JSON export

## Testing

```bash
# Run tests
pytest tests/test_workflow.py -v

# Run specific test
pytest tests/test_workflow.py::test_workflow_happy_path -v
```

## Docker Services

```bash
# Start all services
docker-compose up --build

# Services running:
# - redis:6379          (Message broker)
# - mock-api-1:8001     (Mock internal API 1)
# - mock-api-2:8002     (Mock internal API 2)
# - web:8000            (FastAPI app)
# - worker              (Celery worker)
```

## Benefits of New Structure

### Modularity
- ✅ Each step is ~10-30 lines (vs 80-line monolith)
- ✅ Easy to understand individual steps
- ✅ Simple to test in isolation

### Maintainability
- ✅ Clear file organization
- ✅ Easy to locate specific logic
- ✅ Reduced cognitive load

### Extensibility
- ✅ Add new steps without touching existing code
- ✅ Modify individual steps safely
- ✅ Reuse steps across workflows

### Visibility
- ✅ See exactly what's happening at each step
- ✅ Track performance bottlenecks
- ✅ Debug failures quickly
- ✅ Generate documentation automatically

## Performance Impact

| Feature | Overhead |
|---------|----------|
| Modular structure | ~0ms (compile-time only) |
| Visualization enabled | ~0.1-0.5ms per workflow |
| Visualization disabled | ~0ms |

Recommendation: Enable visualization for debugging/testing, disable for high-throughput production.

## Next Steps

1. **Add More Steps**: Create new step files as needed
2. **Custom Visualizations**: Extend `WorkflowVisualizer` class
3. **Parallel Execution**: Modify workflow_manager for concurrent steps
4. **Dynamic Workflows**: Load step configuration from database
5. **Workflow Versioning**: Support multiple workflow versions

## Documentation

- `VISUALIZATION.md` - Complete visualization guide
- `README.md` - Project overview
- `commands.md` - Setup commands
- This file - Architecture documentation

