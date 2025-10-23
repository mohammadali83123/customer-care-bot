# app/utils/beautifier.py
"""
Beautification utilities for workflow steps and API responses.
Provides enhanced formatting with colors, emojis, and structured output.
"""
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class StepStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RUNNING = "running"
    PENDING = "pending"

@dataclass
class StepInfo:
    step_number: int
    step_name: str
    status: StepStatus
    duration_ms: float = 0.0
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class WorkflowBeautifier:
    """Enhanced formatting for workflow execution and API responses."""
    
    # Color codes for terminal output
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bg_red': '\033[41m',
        'bg_green': '\033[42m',
        'bg_yellow': '\033[43m',
        'bg_blue': '\033[44m',
    }
    
    # Emoji icons for different statuses
    EMOJIS = {
        'success': '✅',
        'failed': '❌',
        'running': '🔄',
        'pending': '⏳',
        'api': '🌐',
        'agent': '🤖',
        'data': '📊',
        'time': '⏱️',
        'branch': '🌿',
        'workflow': '⚡',
        'warning': '⚠️',
        'info': 'ℹ️',
        'error': '💥'
    }
    
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.start_time = datetime.now()
        self.steps: List[StepInfo] = []
    
    def add_step(self, step_number: int, step_name: str, status: StepStatus, 
                 duration_ms: float = 0.0, details: Optional[Dict[str, Any]] = None):
        """Add a step to the execution trace."""
        step = StepInfo(
            step_number=step_number,
            step_name=step_name,
            status=status,
            duration_ms=duration_ms,
            details=details,
            timestamp=datetime.now()
        )
        self.steps.append(step)
    
    def format_step_output(self, step: StepInfo, is_last: bool = False) -> str:
        """Format a single step with enhanced visual styling."""
        # Choose appropriate tree characters
        if is_last:
            tree_char = "└──"
            detail_prefix = "    "
        else:
            tree_char = "├──"
            detail_prefix = "│   "
        
        # Status icon and color
        status_config = {
            StepStatus.SUCCESS: (self.EMOJIS['success'], self.COLORS['green']),
            StepStatus.FAILED: (self.EMOJIS['failed'], self.COLORS['red']),
            StepStatus.RUNNING: (self.EMOJIS['running'], self.COLORS['yellow']),
            StepStatus.PENDING: (self.EMOJIS['pending'], self.COLORS['dim'])
        }
        
        emoji, color = status_config.get(step.status, (self.EMOJIS['info'], self.COLORS['white']))
        
        # Build the main step line
        step_line = f"{tree_char} {emoji} {color}{self.COLORS['bold']}Step {step.step_number}: {step.step_name}{self.COLORS['reset']}"
        
        # Add duration if available
        if step.duration_ms > 0:
            duration_color = self.COLORS['cyan']
            step_line += f" {duration_color}({step.duration_ms:.2f}ms){self.COLORS['reset']}"
        
        lines = [step_line]
        
        # Add details if present
        if step.details:
            for key, value in step.details.items():
                detail_line = f"{detail_prefix}  {self.COLORS['dim']}• {key}:{self.COLORS['reset']} {self._format_value(value)}"
                lines.append(detail_line)
        
        return "\n".join(lines)
    
    def _format_value(self, value: Any) -> str:
        """Format a value for display with appropriate styling."""
        if isinstance(value, dict):
            return f"{self.COLORS['blue']}{json.dumps(value, indent=2, default=str)}{self.COLORS['reset']}"
        elif isinstance(value, list):
            if len(value) > 3:
                return f"{self.COLORS['cyan']}[{len(value)} items]{self.COLORS['reset']}"
            return f"{self.COLORS['cyan']}{value}{self.COLORS['reset']}"
        elif isinstance(value, str):
            return f"{self.COLORS['yellow']}'{value}'{self.COLORS['reset']}"
        else:
            return f"{self.COLORS['white']}{value}{self.COLORS['reset']}"
    
    def get_beautified_tree(self) -> str:
        """Generate a beautifully formatted execution tree."""
        lines = []
        
        # Header with workflow info
        header_lines = [
            f"{self.COLORS['bold']}{self.COLORS['magenta']}{'='*80}{self.COLORS['reset']}",
            f"{self.EMOJIS['workflow']} {self.COLORS['bold']}{self.COLORS['blue']}Workflow Execution{self.COLORS['reset']}",
            f"{self.COLORS['dim']}ID: {self.workflow_id}{self.COLORS['reset']}",
            f"{self.COLORS['dim']}Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}{self.COLORS['reset']}",
            f"{self.COLORS['bold']}{self.COLORS['magenta']}{'='*80}{self.COLORS['reset']}",
            ""
        ]
        lines.extend(header_lines)
        
        # Steps
        for i, step in enumerate(self.steps):
            is_last = i == len(self.steps) - 1
            step_output = self.format_step_output(step, is_last)
            lines.append(step_output)
        
        # Footer with summary
        if self.steps:
            successful_steps = sum(1 for s in self.steps if s.status == StepStatus.SUCCESS)
            failed_steps = sum(1 for s in self.steps if s.status == StepStatus.FAILED)
            total_duration = sum(s.duration_ms for s in self.steps)
            
            footer_lines = [
                "",
                f"{self.COLORS['bold']}{self.COLORS['magenta']}{'='*80}{self.COLORS['reset']}",
                f"{self.EMOJIS['data']} {self.COLORS['bold']}Summary:{self.COLORS['reset']}",
                f"  {self.EMOJIS['success']} Successful: {self.COLORS['green']}{successful_steps}{self.COLORS['reset']}",
                f"  {self.EMOJIS['failed']} Failed: {self.COLORS['red']}{failed_steps}{self.COLORS['reset']}",
                f"  {self.EMOJIS['time']} Total Duration: {self.COLORS['cyan']}{total_duration:.2f}ms{self.COLORS['reset']}",
                f"{self.COLORS['bold']}{self.COLORS['magenta']}{'='*80}{self.COLORS['reset']}"
            ]
            lines.extend(footer_lines)
        
        return "\n".join(lines)
    
    def format_api_response(self, api_name: str, response_data: Dict[str, Any], 
                          duration_ms: float = 0.0, status_code: int = 200) -> str:
        """Format API response with enhanced styling."""
        lines = []
        
        # API header
        status_emoji = "✅" if 200 <= status_code < 300 else "❌"
        status_color = self.COLORS['green'] if 200 <= status_code < 300 else self.COLORS['red']
        
        lines.append(f"{self.EMOJIS['api']} {self.COLORS['bold']}{api_name}{self.COLORS['reset']}")
        lines.append(f"  {status_emoji} Status: {status_color}{status_code}{self.COLORS['reset']}")
        if duration_ms > 0:
            lines.append(f"  {self.EMOJIS['time']} Duration: {self.COLORS['cyan']}{duration_ms:.2f}ms{self.COLORS['reset']}")
        
        # Response data
        if response_data:
            lines.append(f"  {self.EMOJIS['data']} Response:")
            formatted_data = self._format_json_response(response_data)
            lines.append(formatted_data)
        
        return "\n".join(lines)
    
    def _format_json_response(self, data: Dict[str, Any], indent: int = 4) -> str:
        """Format JSON response with proper indentation and colors."""
        try:
            json_str = json.dumps(data, indent=2, default=str, ensure_ascii=False)
            # Add color to JSON keys and values
            lines = []
            for line in json_str.split('\n'):
                if ':' in line and not line.strip().startswith('{') and not line.strip().startswith('}'):
                    # Color the key
                    key_part, value_part = line.split(':', 1)
                    colored_line = f"{' ' * indent}{self.COLORS['blue']}{key_part.strip()}{self.COLORS['reset']}:{value_part}"
                    lines.append(colored_line)
                else:
                    lines.append(f"{' ' * indent}{line}")
            return '\n'.join(lines)
        except Exception:
            return f"{' ' * indent}{self.COLORS['red']}Error formatting JSON{self.COLORS['reset']}"
    
    def format_agent_output(self, agent_data: Dict[str, Any]) -> str:
        """Format agent output with enhanced styling."""
        lines = []
        
        lines.append(f"{self.EMOJIS['agent']} {self.COLORS['bold']}Agent Analysis{self.COLORS['reset']}")
        
        if 'intent' in agent_data:
            lines.append(f"  {self.COLORS['cyan']}Intent:{self.COLORS['reset']} {self.COLORS['yellow']}{agent_data['intent']}{self.COLORS['reset']}")
        
        if 'confidence' in agent_data:
            confidence_color = self.COLORS['green'] if agent_data['confidence'] > 0.8 else self.COLORS['yellow']
            lines.append(f"  {self.COLORS['cyan']}Confidence:{self.COLORS['reset']} {confidence_color}{agent_data['confidence']:.2f}{self.COLORS['reset']}")
        
        if 'action' in agent_data:
            lines.append(f"  {self.COLORS['cyan']}Action:{self.COLORS['reset']} {self.COLORS['blue']}{agent_data['action']}{self.COLORS['reset']}")
        
        if 'response' in agent_data:
            lines.append(f"  {self.COLORS['cyan']}Response:{self.COLORS['reset']}")
            lines.append(f"    {self.COLORS['white']}{agent_data['response']}{self.COLORS['reset']}")
        
        return "\n".join(lines)
    
    def get_enhanced_logs(self, logs: List[str]) -> str:
        """Format logs with enhanced styling."""
        if not logs:
            return f"{self.COLORS['dim']}No logs available{self.COLORS['reset']}"
        
        lines = [f"{self.COLORS['bold']}{self.EMOJIS['info']} Execution Logs{self.COLORS['reset']}"]
        lines.append(f"{self.COLORS['dim']}{'─' * 50}{self.COLORS['reset']}")
        
        for i, log in enumerate(logs, 1):
            timestamp = datetime.now().strftime('%H:%M:%S')
            lines.append(f"{self.COLORS['dim']}[{timestamp}]{self.COLORS['reset']} {self.COLORS['white']}{log}{self.COLORS['reset']}")
        
        return "\n".join(lines)

def create_beautifier(workflow_id: str) -> WorkflowBeautifier:
    """Factory function to create a beautifier instance."""
    return WorkflowBeautifier(workflow_id)
