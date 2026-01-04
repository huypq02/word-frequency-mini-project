"""
Automated setup and startup script for Word Frequency Mini Project
This script will:
1. Create necessary directories
2. Create required __init__.py files
3. Download NLTK data
4. Start the FastAPI server
"""

import os
import sys
import subprocess
from pathlib import Path

def print_step(step_num, message):
    """Print formatted step message"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {message}")
    print('='*60)

def create_directories():
    """Create necessary directories"""
    print_step(1, "Creating required directories")
    
    directories = ['output', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created/verified directory: {directory}/")

def create_init_files():
    """Create __init__.py files for Python packages"""
    print_step(2, "Creating __init__.py files")
    
    init_files = [
        'src/__init__.py',
        'src/app/__init__.py',
        'src/pipeline/__init__.py'
    ]
    
    for init_file in init_files:
        Path(init_file).touch(exist_ok=True)
        print(f"✓ Created/verified: {init_file}")

def download_nltk_data():
    """Download required NLTK data"""
    print_step(3, "Downloading NLTK data")
    
    try:
        import nltk
        print("Downloading 'punkt' tokenizer...")
        nltk.download('punkt', quiet=True)
        print("✓ Downloaded: punkt")
        
        print("Downloading 'stopwords' corpus...")
        nltk.download('stopwords', quiet=True)
        print("✓ Downloaded: stopwords")
        
        print("\n✓ All NLTK data downloaded successfully!")
    except ImportError:
        print("⚠ Warning: NLTK not installed. Please run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"⚠ Warning: Failed to download NLTK data: {e}")
        return False
    
    return True

def check_dependencies():
    """Check if dependencies are installed"""
    print_step(4, "Checking dependencies")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pandas',
        'nltk',
        'underthesea',
        'matplotlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        print("\nTo install all dependencies, run:")
        print("  pip install -r requirements.txt")
        
        response = input("\nDo you want to install missing packages now? (y/n): ").strip().lower()
        if response == 'y':
            print("\nInstalling dependencies...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                print("✓ Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("✗ Failed to install dependencies")
                return False
        else:
            print("\n⚠ Please install dependencies manually before starting the server.")
            return False
    
    print("\n✓ All dependencies installed!")
    return True

def start_server():
    """Start the FastAPI server"""
    print_step(5, "Starting FastAPI server")
    
    print("\n🚀 Starting server at http://localhost:5000")
    print("📖 API documentation: http://localhost:5000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'src.app.main:app',
            '--reload',
            '--port', '5000',
            '--host', '0.0.0.0'
        ])
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped by user")
    except FileNotFoundError:
        print("\n✗ uvicorn not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'uvicorn[standard]'])
        print("\nPlease run this script again to start the server.")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("Word Frequency Mini Project - Automated Setup & Startup")
    print("="*60)
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Create __init__.py files
    create_init_files()
    
    # Step 3: Check and install dependencies
    if not check_dependencies():
        print("\n⚠ Setup incomplete. Please install dependencies and try again.")
        sys.exit(1)
    
    # Step 4: Download NLTK data
    download_nltk_data()
    
    # Step 5: Start server
    start_server()
    
    print("\n✓ Thank you for using Word Frequency Mini Project!")

if __name__ == "__main__":
    # Ensure we're in the project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    main()
