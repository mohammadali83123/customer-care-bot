# Workflow Visualization

Dynamic visual tree structure for workflow execution tracking and debugging.

## Features

✅ **Real-time Execution Tracking** - Monitors each step as it executes  
✅ **Performance Metrics** - Tracks execution time for each step  
✅ **Branch Visualization** - Shows which conditional path was taken  
✅ **Multiple Export Formats** - ASCII tree, Mermaid diagrams, JSON, HTML  
✅ **Success/Failure Indicators** - Clear visual status for each step  

## Usage

### 1. Via API Endpoints

#### Get Full Visualization
```bash
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer123",
    "event": {"message": "where is my order?"}
  }'
```

Response includes:
```json
{
  "workflow_id": "...",
  "status": "completed",
  "final_status": "order_status_returned",
  "visualization": {
    "text_tree": "ASCII tree visualization...",
    "mermaid": "Mermaid diagram syntax...",
    "json": "JSON export...",
    "simple_tree": "Simple indented tree..."
  },
  "logs": [...],
  "globals": {...}
}
```

#### Get ASCII Tree Only
```bash
curl -X POST http://localhost:8000/workflow/visualize \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer123",
    "event": {"message": "I want a refund"}
  }'
```

Output:
```
Workflow Execution Tree: 945fea33-acb5-43e3-880d-34935dd5fcf5
Started: 2025-10-20 01:41:54
Duration: 0.06ms
============================================================

├── ✓ Step 1: Webhook Triggered (0.00ms)
├── ✓ Step 2: Initialize Globals (0.00ms)
├── ✓ Step 3: Call Internal API 1 (0.02ms)
├── ✓ Step 4: Set Globals After API1 (0.00ms)
├── ✓ Step 5: Call Internal API 2 (0.00ms)
├── ✓ Step 6: Set Final Context
├── ✓ Step 7: Run Agent (0.00ms)
├── ✓ Step 8: Conditional Routing (0.00ms)
│     • branch: routed_to_refunds
└── ✓ Step 9: Terminate (0.00ms)
```

#### Get Mermaid Diagram
```bash
curl -X POST http://localhost:8000/workflow/diagram \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer123",
    "event": {"message": "Hi"}
  }'
```

Copy the output to [mermaid.live](https://mermaid.live) for interactive visualization.

### 2. Programmatically

```python
from app.workflow.workflow_manager import run_workflow_instance
import uuid

# Run workflow with visualization enabled
result = await run_workflow_instance(
    workflow_id=str(uuid.uuid4()),
    customer_id="customer123",
    event={"message": "where is my order?"},
    enable_visualization=True  # Default is True
)

# Access visualizations
print(result["visualization"]["text_tree"])
print(result["visualization"]["mermaid"])

# Export to JSON
import json
viz_data = json.loads(result["visualization"]["json"])
```

### 3. Demo Script

Run the included demo to see all visualization formats:

```bash
python demo_visualization.py
```

## Visualization Formats

### 1. ASCII Text Tree
Human-readable tree with Unicode box-drawing characters:
- ✓ Success indicator
- ✗ Failure indicator
- Execution time per step
- Branch information

### 2. Mermaid Diagram
Flowchart syntax compatible with [Mermaid](https://mermaid.js.org/):
- Visual graph representation
- Color-coded success/failure
- Branch annotations
- Interactive when rendered

### 3. Simple Tree
Indented text representation:
- Minimal formatting
- Easy to parse programmatically
- Good for logs

### 4. JSON Export
Structured data format:
```json
{
  "workflow_id": "...",
  "start_time": "2025-10-20T01:41:54",
  "end_time": "2025-10-20T01:41:54",
  "duration_ms": 0.06,
  "steps": [
    {
      "step_number": 1,
      "step_name": "Webhook Triggered",
      "status": "completed",
      "details": {},
      "duration_ms": 0.00,
      "timestamp": "2025-10-20T01:41:54"
    }
  ],
  "total_steps": 9,
  "successful_steps": 9,
  "failed_steps": 0
}
```

## Integration with Celery

By default, Celery tasks run without visualization for performance. To enable:

```python
# In app/tasks.py - modify run_workflow_task

@celery.task(bind=True, acks_late=True, max_retries=3)
def run_workflow_task(self, customer_id: str, event: dict, enable_viz: bool = False):
    workflow_id = str(uuid.uuid4())
    try:
        return asyncio.get_event_loop().run_until_complete(
            run_workflow_instance(workflow_id, customer_id, event, enable_viz)
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

## Performance Impact

- **Enabled**: ~0.1-0.5ms overhead per workflow
- **Disabled**: No overhead
- Recommended: Enable for debugging/testing, disable for production high-throughput

## Custom Visualizers

Create custom visualization formats by extending `WorkflowVisualizer`:

```python
# app/workflow/visualizer.py

class WorkflowVisualizer:
    def get_custom_format(self) -> str:
        """Your custom format here."""
        # Access self.steps, self.workflow_id, etc.
        return custom_output
```

## Use Cases

1. **Debugging** - Identify which step is failing or slow
2. **Monitoring** - Track execution patterns
3. **Documentation** - Auto-generate workflow diagrams
4. **Testing** - Verify correct branch execution
5. **Auditing** - Log complete execution traces

## API Documentation

Access interactive API docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Examples

See `demo_visualization.py` for complete examples of:
- Order status queries → `order_status_returned` branch
- Refund requests → `routed_to_refunds` branch  
- General queries → `auto_responded` branch

