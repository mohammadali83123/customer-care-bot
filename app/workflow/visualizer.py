# app/workflow/visualizer.py
"""
Workflow visualization module for generating execution trees.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

class WorkflowVisualizer:
    """Generates visual representations of workflow execution."""
    
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.steps: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        
    def add_step(self, step_name: str, step_number: int, status: str, 
                 details: Optional[Dict[str, Any]] = None, duration_ms: float = 0):
        """Add a step to the execution trace."""
        self.steps.append({
            "step_number": step_number,
            "step_name": step_name,
            "status": status,
            "details": details or {},
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat()
        })
    
    def mark_complete(self):
        """Mark workflow execution as complete."""
        self.end_time = datetime.now()
    
    def get_text_tree(self) -> str:
        """Generate ASCII tree representation of workflow execution."""
        lines = []
        lines.append(f"Workflow Execution Tree: {self.workflow_id}")
        lines.append(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() * 1000
            lines.append(f"Duration: {duration:.2f}ms")
        lines.append("=" * 60)
        lines.append("")
        
        for i, step in enumerate(self.steps):
            is_last = i == len(self.steps) - 1
            prefix = "└── " if is_last else "├── "
            
            # Status icon
            status_icon = {
                "completed": "✓",
                "failed": "✗",
                "skipped": "○",
                "running": "→"
            }.get(step["status"], "?")
            
            # Main step line
            step_line = f"{prefix}{status_icon} Step {step['step_number']}: {step['step_name']}"
            if step["duration_ms"] > 0:
                step_line += f" ({step['duration_ms']:.2f}ms)"
            lines.append(step_line)
            
            # Details
            if step["details"]:
                detail_prefix = "    " if is_last else "│   "
                for key, value in step["details"].items():
                    lines.append(f"{detail_prefix}  • {key}: {value}")
        
        return "\n".join(lines)
    
    def get_mermaid_diagram(self) -> str:
        """Generate Mermaid flowchart syntax."""
        lines = ["flowchart TD"]
        lines.append(f"    Start([Workflow: {self.workflow_id}])")
        
        prev_node = "Start"
        for step in self.steps:
            node_id = f"Step{step['step_number']}"
            step_text = f"Step {step['step_number']}: {step['step_name']}"
            
            # Node styling based on status
            if step["status"] == "completed":
                lines.append(f"    {node_id}[{step_text}]")
                lines.append(f"    {node_id}:::success")
            elif step["status"] == "failed":
                lines.append(f"    {node_id}[{step_text}]")
                lines.append(f"    {node_id}:::failure")
            else:
                lines.append(f"    {node_id}[{step_text}]")
            
            # Connect to previous
            lines.append(f"    {prev_node} --> {node_id}")
            
            # Add branch info if present
            if "branch" in step["details"]:
                branch_info = step["details"]["branch"]
                lines.append(f"    {node_id} -.-> BranchInfo{step['step_number']}{{{{Branch: {branch_info}}}}}")
            
            prev_node = node_id
        
        # End node
        lines.append(f"    {prev_node} --> End([Complete])")
        
        # Styles
        lines.append("")
        lines.append("    classDef success fill:#90EE90,stroke:#006400,stroke-width:2px")
        lines.append("    classDef failure fill:#FFB6C1,stroke:#8B0000,stroke-width:2px")
        
        return "\n".join(lines)
    
    def get_json_tree(self) -> str:
        """Generate JSON representation of execution."""
        data = {
            "workflow_id": self.workflow_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": (
                (self.end_time - self.start_time).total_seconds() * 1000 
                if self.end_time else None
            ),
            "steps": self.steps,
            "total_steps": len(self.steps),
            "successful_steps": sum(1 for s in self.steps if s["status"] == "completed"),
            "failed_steps": sum(1 for s in self.steps if s["status"] == "failed")
        }
        return json.dumps(data, indent=2)
    
    def get_simple_tree(self) -> str:
        """Generate simple indented tree view."""
        lines = []
        lines.append(f"Workflow: {self.workflow_id}")
        
        for step in self.steps:
            status = "✓" if step["status"] == "completed" else "✗"
            indent = "  " * (step["step_number"] - 1)
            lines.append(f"{indent}{status} {step['step_name']}")
            
            if step["details"]:
                for key, value in step["details"].items():
                    lines.append(f"{indent}  └─ {key}: {value}")
        
        return "\n".join(lines)
    
    def export_html(self) -> str:
        """Generate interactive HTML visualization."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Workflow Execution: {self.workflow_id}</title>
    <style>
        body {{ font-family: 'Courier New', monospace; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
        .step {{ margin: 10px 0; padding: 10px; border-left: 3px solid #ccc; }}
        .step.success {{ border-left-color: #4CAF50; background: #f1f8f4; }}
        .step.failed {{ border-left-color: #f44336; background: #fef1f1; }}
        .step-name {{ font-weight: bold; font-size: 14px; }}
        .step-details {{ margin-left: 20px; color: #666; font-size: 12px; }}
        .duration {{ color: #999; font-size: 11px; float: right; }}
        .summary {{ background: #e3f2fd; padding: 10px; border-radius: 4px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Workflow Execution Visualization</h2>
            <p><strong>Workflow ID:</strong> {self.workflow_id}</p>
            <p><strong>Started:</strong> {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """
        
        for step in self.steps:
            status_class = "success" if step["status"] == "completed" else "failed"
            html += f"""
        <div class="step {status_class}">
            <div class="step-name">
                Step {step['step_number']}: {step['step_name']}
                <span class="duration">{step['duration_ms']:.2f}ms</span>
            </div>
            """
            
            if step["details"]:
                html += '<div class="step-details">'
                for key, value in step["details"].items():
                    html += f"<div>• {key}: {value}</div>"
                html += '</div>'
            
            html += "</div>"
        
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() * 1000
            success_count = sum(1 for s in self.steps if s["status"] == "completed")
            html += f"""
        <div class="summary">
            <strong>Summary:</strong> {success_count}/{len(self.steps)} steps completed in {duration:.2f}ms
        </div>
            """
        
        html += """
    </div>
</body>
</html>
        """
        return html

