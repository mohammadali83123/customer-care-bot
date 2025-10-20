# Project Context & Documentation

## 🎯 Project Motive

**Customer Care Bot** - A modular, scalable workflow engine for processing customer service requests with intelligent routing and real-time visualization.

### Core Purpose
- **Automate customer service workflows** through a structured, step-by-step process
- **Intelligent routing** based on customer intent (refunds, order status, general queries)
- **Real-time monitoring** with dynamic visualization of workflow execution
- **Scalable architecture** using async processing with Celery and Redis
- **Developer-friendly** with modular design and comprehensive debugging tools

## 🏗️ Architecture Overview

### Technology Stack
- **Backend**: FastAPI (Python 3.13)
- **Task Queue**: Celery with Redis broker
- **Visualization**: Custom tree generation (ASCII, Mermaid, JSON)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest with async support

### Key Components

#### 1. **Modular Workflow System**
```
app/workflow/
├── workflow_manager.py    # Main orchestrator
├── visualizer.py         # Dynamic visualization engine
└── steps/                # Individual step modules
    ├── step_1.py         # Webhook trigger
    ├── step_2.py         # Initialize globals
    ├── step_3.py         # Call Internal API 1
    ├── step_4.py         # Transform API1 data
    ├── step_5.py         # Call Internal API 2
    ├── step_6.py         # Set final context
    ├── step_7.py         # Run agent (intent detection)
    ├── step_8.py         # Conditional routing
    └── step_9.py         # Terminate
```

#### 2. **Intelligent Routing**
- **Refund requests** → `routed_to_refunds`
- **Order status queries** → `order_status_returned`
- **General queries** → `auto_responded`

#### 3. **Visualization System**
- **ASCII trees** with Unicode characters
- **Mermaid diagrams** for interactive visualization
- **JSON exports** for programmatic access
- **Performance metrics** per step
- **Branch tracking** for conditional logic

## 🚀 Use Cases

### Primary Use Cases
1. **Customer Service Automation**
   - Process incoming webhook requests
   - Route to appropriate departments
   - Provide automated responses

2. **Workflow Debugging**
   - Visualize execution flow
   - Identify bottlenecks
   - Track performance metrics

3. **System Integration**
   - Connect with internal APIs
   - Transform data between systems
   - Maintain execution context

### Secondary Use Cases
1. **Documentation Generation**
   - Auto-generate workflow diagrams
   - Create execution reports
   - Export structured data

2. **Monitoring & Auditing**
   - Track workflow success rates
   - Log execution details
   - Generate analytics

## 📊 Workflow Execution Flow

```
Webhook → Initialize → API1 → Transform → API2 → Context → Agent → Route → Terminate
    ↓         ↓        ↓        ↓        ↓        ↓        ↓       ↓        ↓
  Step 1   Step 2   Step 3   Step 4   Step 5   Step 6   Step 7  Step 8   Step 9
```

### Step Details
1. **Webhook Triggered** - Receive customer request
2. **Initialize Globals** - Set up execution context
3. **Call Internal API 1** - Fetch customer data
4. **Transform Data** - Process API1 response
5. **Call Internal API 2** - Get additional context
6. **Set Final Context** - Combine all data
7. **Run Agent** - Analyze intent and determine action
8. **Conditional Routing** - Branch based on agent output
9. **Terminate** - Complete workflow and return results

## 🔧 Development Context

### Project Evolution
1. **Initial State**: Monolithic `workflow.py` (80 lines)
2. **Refactored**: Modular step-based architecture
3. **Enhanced**: Added visualization system
4. **Optimized**: Performance tracking and error handling

### Key Design Decisions

#### 1. **Modular Architecture**
- **Why**: Easier testing, maintenance, and extension
- **How**: Each step is a separate module with clear interface
- **Benefit**: Can modify individual steps without affecting others

#### 2. **Visualization System**
- **Why**: Debugging complex workflows is difficult without visibility
- **How**: Real-time tracking with multiple export formats
- **Benefit**: Immediate feedback on execution flow and performance

#### 3. **Async Processing**
- **Why**: Handle multiple requests concurrently
- **How**: Celery workers with Redis message broker
- **Benefit**: Scalable and responsive system

#### 4. **Mock APIs for Development**
- **Why**: External dependencies make testing difficult
- **How**: Docker services that simulate real APIs
- **Benefit**: Reliable testing environment

## 📈 Performance Characteristics

### Execution Times
- **Full workflow**: ~20-50ms (with mocked APIs)
- **Individual steps**: ~0.01-0.1ms each
- **Visualization overhead**: ~0.1-0.5ms when enabled

### Scalability
- **Concurrent workflows**: Limited by Celery worker count
- **Memory usage**: ~10-20MB per worker
- **Redis throughput**: ~10,000+ operations/second

## 🛠️ Development Workflow

### Local Development
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run demo
python examples/demo_visualization.py

# Start services
docker-compose up --build
```

### Testing Strategy
- **Unit tests**: Individual step functions
- **Integration tests**: Full workflow execution
- **Mock APIs**: Reliable external dependencies
- **Visualization tests**: Output format validation

## 📚 Documentation Structure

### Core Documentation
- `README.md` - Project overview and quick start
- `CONTEXT.md` - This file (project context and architecture)
- `WORKFLOW_STRUCTURE.md` - Detailed technical documentation
- `VISUALIZATION.md` - Visualization system guide

### Code Documentation
- Inline docstrings for all functions
- Type hints throughout codebase
- Comprehensive error messages

### Examples
- `examples/demo_visualization.py` - Complete usage examples
- API endpoint documentation via FastAPI auto-docs

## 🔮 Future Enhancements

### Planned Features
1. **Parallel Step Execution** - Run independent steps concurrently
2. **Dynamic Workflow Loading** - Load workflows from database
3. **Workflow Versioning** - Support multiple workflow versions
4. **Custom Visualizers** - Plugin system for new formats
5. **Metrics Dashboard** - Real-time monitoring interface

### Potential Integrations
1. **Database Persistence** - Store workflow state and results
2. **Message Queues** - Kafka/RabbitMQ for high-throughput
3. **Monitoring** - Prometheus/Grafana integration
4. **Authentication** - JWT-based API security
5. **Webhooks** - Outbound notifications

## 🎯 Success Metrics

### Technical Metrics
- **Test Coverage**: >90%
- **Response Time**: <100ms for simple workflows
- **Uptime**: >99.9%
- **Error Rate**: <0.1%

### Business Metrics
- **Workflow Completion Rate**: >95%
- **Customer Satisfaction**: Measured via routing accuracy
- **Developer Productivity**: Faster debugging and development
- **System Reliability**: Reduced manual intervention

## 🔍 Troubleshooting Guide

### Common Issues
1. **API Connection Failures** - Check mock services are running
2. **Celery Worker Issues** - Verify Redis connection
3. **Visualization Errors** - Check step execution logs
4. **Performance Issues** - Monitor step execution times

### Debug Tools
- **Workflow Visualization** - See execution flow in real-time
- **Step-by-step Logging** - Detailed execution logs
- **Performance Metrics** - Timing for each step
- **Error Tracking** - Clear failure points and reasons

## 📞 Support & Maintenance

### Code Ownership
- **Primary Maintainer**: [Your Name]
- **Repository**: customer-care-bot
- **Documentation**: Self-contained in repository

### Maintenance Tasks
- **Regular Updates**: Dependencies and security patches
- **Performance Monitoring**: Track execution metrics
- **Feature Development**: Based on customer feedback
- **Documentation**: Keep examples and guides current

---

*This document serves as the single source of truth for understanding the project's purpose, architecture, and development context. Update as the project evolves.*
