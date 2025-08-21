#!/usr/bin/env python3
"""
Debug script to identify why SnapClass server crashes on startup
"""

import os
import sys
import traceback
import socket

def test_imports():
    """Test all imports that app.py uses"""
    print("Testing imports...")
    
    try:
        from flask import Flask, render_template, request, redirect, url_for, jsonify
        print("✓ Flask imports successful")
    except Exception as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import logging
        print("✓ logging import successful")
    except Exception as e:
        print(f"✗ logging import failed: {e}")
        return False
    
    try:
        import socket
        print("✓ socket import successful")
    except Exception as e:
        print(f"✗ socket import failed: {e}")
        return False
    
    try:
        from werkzeug.utils import secure_filename
        print("✓ werkzeug import successful")
    except Exception as e:
        print(f"✗ werkzeug import failed: {e}")
        return False
    
    try:
        from trans import process_files
        print("✓ trans import successful")
    except Exception as e:
        print(f"✗ trans import failed: {e}")
        return False
    
    try:
        import question_gen
        print("✓ question_gen import successful")
    except Exception as e:
        print(f"✗ question_gen import failed: {e}")
        return False
    
    try:
        import utils
        print("✓ utils import successful")
    except Exception as e:
        print(f"✗ utils import failed: {e}")
        return False
    
    try:
        import json
        print("✓ json import successful")
    except Exception as e:
        print(f"✗ json import failed: {e}")
        return False
    
    try:
        import slm_analyse
        print("✓ slm_analyse import successful")
    except Exception as e:
        print(f"✗ slm_analyse import failed: {e}")
        return False
    
    try:
        import subprocess
        print("✓ subprocess import successful")
    except Exception as e:
        print(f"✗ subprocess import failed: {e}")
        return False
    
    try:
        import signal
        print("✓ signal import successful")
    except Exception as e:
        print(f"✗ signal import failed: {e}")
        return False
    
    try:
        import threading
        print("✓ threading import successful")
    except Exception as e:
        print(f"✗ threading import failed: {e}")
        return False
    
    try:
        from datetime import datetime
        print("✓ datetime import successful")
    except Exception as e:
        print(f"✗ datetime import failed: {e}")
        return False
    
    return True

def test_port_availability():
    """Test if port 5000 is available"""
    print("\nTesting port availability...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        if result == 0:
            print("✗ Port 5000 is already in use!")
            return False
        else:
            print("✓ Port 5000 is available")
            return True
    except Exception as e:
        print(f"✗ Error testing port: {e}")
        return False

def test_file_permissions():
    """Test if we can create necessary files"""
    print("\nTesting file permissions...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Test uploads directory
    uploads_dir = os.path.join(base_dir, 'uploads')
    try:
        os.makedirs(uploads_dir, exist_ok=True)
        print("✓ Uploads directory created/accessible")
    except Exception as e:
        print(f"✗ Cannot create uploads directory: {e}")
        return False
    
    # Test log file
    log_path = os.path.join(base_dir, 'snapclass.log')
    try:
        with open(log_path, 'a') as f:
            f.write("Test log entry\n")
        print("✓ Log file writable")
    except Exception as e:
        print(f"✗ Cannot write to log file: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\nTesting environment...")
    
    env_var = os.environ.get('SNAPCLASS_LAUNCHED_BY_DESKTOP')
    if env_var == '1':
        print("✓ SNAPCLASS_LAUNCHED_BY_DESKTOP is set correctly")
    else:
        print(f"✗ SNAPCLASS_LAUNCHED_BY_DESKTOP is not set correctly: {env_var}")
        print("  This will cause the server to exit immediately!")
        return False
    
    return True

def test_flask_app_creation():
    """Test if Flask app can be created"""
    print("\nTesting Flask app creation...")
    
    try:
        from flask import Flask
        import os
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        app = Flask(
            __name__,
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static')
        )
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        traceback.print_exc()
        return False

def main():
    print("=== SnapClass Server Debug Tool ===\n")
    
    # Set environment variable for testing
    os.environ['SNAPCLASS_LAUNCHED_BY_DESKTOP'] = '1'
    
    tests = [
        ("Import Tests", test_imports),
        ("Port Availability", test_port_availability),
        ("File Permissions", test_file_permissions),
        ("Environment Variables", test_environment),
        ("Flask App Creation", test_flask_app_creation)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                all_passed = False
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            traceback.print_exc()
            all_passed = False
    
    print("\n=== Summary ===")
    if all_passed:
        print("✓ All tests passed! The server should work.")
        print("\nIf the server still crashes, try running the actual app.py:")
        print("python app.py")
    else:
        print("✗ Some tests failed. Fix the issues above before running the server.")
    
    return all_passed

if __name__ == "__main__":
    main()
