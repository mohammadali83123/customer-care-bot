#!/usr/bin/env python3
"""
Development worker script with hot reload.
This script monitors file changes and restarts the Celery worker automatically.
"""
import subprocess
import sys
import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WorkerRestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.worker_process = None
        self.start_worker()
    
    def start_worker(self):
        """Start the Celery worker process."""
        if self.worker_process:
            self.worker_process.terminate()
            self.worker_process.wait()
        
        print("Starting Celery worker...")
        self.worker_process = subprocess.Popen([
            "celery", "-A", "app.celery_config.tasks.celery", "worker", 
            "--loglevel=info", "-Q", "celery"
        ])
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only restart for Python files
        if event.src_path.endswith('.py'):
            print(f"File changed: {event.src_path}")
            print("Restarting worker...")
            self.start_worker()

def main():
    print("Starting development worker with hot reload...")
    
    # Set up file watcher
    event_handler = WorkerRestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path='app', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        observer.stop()
        if event_handler.worker_process:
            event_handler.worker_process.terminate()
            event_handler.worker_process.wait()
    
    observer.join()

if __name__ == "__main__":
    main()
