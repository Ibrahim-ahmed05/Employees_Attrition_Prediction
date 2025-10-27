#!/usr/bin/env python3
"""
Start both FastAPI servers simultaneously:
- main.py (ML Prediction API) on port 8000
- test.py (Supabase API) on port 8001
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_server(script_name, port, description):
    """Start a FastAPI server using uvicorn"""
    print(f"🚀 Starting {description} on port {port}...")
    
    try:
        # Use uvicorn to start the server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            script_name.replace('.py', ':app'), 
            "--host", "0.0.0.0", 
            "--port", str(port), 
            "--reload"
        ], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
        )
        
        print(f"✅ {description} started successfully (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start {description}: {e}")
        return None

def main():
    print("🎯 Starting Dual FastAPI Servers")
    print("=" * 50)
    
    # Check if both files exist
    if not os.path.exists("main.py"):
        print("❌ main.py not found!")
        return
    
    if not os.path.exists("test.py"):
        print("❌ test.py not found!")
        return
    
    # Start both servers
    processes = []
    
    # Start ML Prediction API (main.py) on port 8000
    ml_process = start_server("main.py", 8000, "ML Prediction API")
    if ml_process:
        processes.append(("ML Prediction API", ml_process))
    
    # Wait a moment between starts
    time.sleep(2)
    
    # Start Supabase API (test.py) on port 8001
    supabase_process = start_server("test.py", 8001, "Supabase API")
    if supabase_process:
        processes.append(("Supabase API", supabase_process))
    
    if not processes:
        print("❌ No servers started successfully!")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Servers started successfully!")
    print("\n📋 Available endpoints:")
    print("   🔮 ML Prediction API: http://localhost:8000")
    print("      - /predict - Make attrition predictions")
    print("      - /health - Check model status")
    print("      - /docs - API documentation")
    print("\n   🗄️  Supabase API: http://localhost:8001")
    print("      - /employees - Get all employees")
    print("      - /add_employee - Add new employee")
    print("      - /docs - API documentation")
    
    print("\n🔄 Servers are running... Press Ctrl+C to stop all servers")
    
    try:
        # Keep the script running and monitor processes
        while True:
            time.sleep(1)
            
            # Check if any process has died
            for name, process in processes:
                if process.poll() is not None:
                    print(f"⚠️  {name} has stopped unexpectedly!")
                    processes.remove((name, process))
            
            if not processes:
                print("❌ All servers have stopped!")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping all servers...")
        
        # Terminate all processes
        for name, process in processes:
            try:
                process.terminate()
                print(f"✅ {name} stopped")
            except:
                pass
        
        # Wait for processes to terminate gracefully
        time.sleep(2)
        
        # Force kill if still running
        for name, process in processes:
            try:
                if process.poll() is None:
                    process.kill()
                    print(f"🔪 {name} force stopped")
            except:
                pass
        
        print("👋 All servers stopped!")

if __name__ == "__main__":
    main()
