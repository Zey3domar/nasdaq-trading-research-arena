#!/usr/bin/env python3
"""
Quick start script for Trading Research Arena
"""
import os, sys, subprocess, time

def main():
    print("🚀 Starting Trading Research Arena...")
    
    # Install dependencies
    print("Installing dependencies...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    # Start services
    print("Starting services...")
    
    # Start Redis
    if os.name == 'nt':
        os.system("redis-server --daemonize yes")
    else:
        os.system("redis-server --daemonize yes")
    
    time.sleep(2)
    
    # Start MLflow
    mlflow = subprocess.Popen([
        sys.executable, "-m", "mlflow", "server", 
        "--host", "0.0.0.0", "--port", "5000"
    ])
    
    time.sleep(3)
    
    # Start Dashboard
    dashboard = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "dashboard.app:app", 
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])
    
    print("✅ All services started!")
    print("📊 Dashboard: http://localhost:8000")
    print("📈 MLflow: http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    try:
        mlflow.wait()
        dashboard.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        mlflow.terminate()
        dashboard.terminate()

if __name__ == "__main__":
    main()
