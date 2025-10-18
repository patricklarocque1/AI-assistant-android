#!/usr/bin/env python3
"""
Model Management Script
Helps manage AI models in your local cache directory
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import shutil

# Load environment variables
load_dotenv()

def get_cache_dir():
    """Get the configured cache directory"""
    cache_dir = os.getenv('MODEL_CACHE_DIR')
    if cache_dir:
        cache_dir = os.path.expanduser(cache_dir)
        cache_dir = os.path.expandvars(cache_dir)
        return Path(cache_dir)
    else:
        # Default HuggingFace cache
        default_cache = Path.home() / '.cache' / 'huggingface'
        return default_cache

def list_models():
    """List all models in the cache directory"""
    cache_dir = get_cache_dir()
    print(f"\n📁 Model cache directory: {cache_dir}")
    
    if not cache_dir.exists():
        print("❌ Cache directory does not exist yet")
        print("   Models will be downloaded here when you first run the server")
        return
    
    print("\n📦 Models in cache:")
    print("=" * 70)
    
    # Look for model directories
    models_dir = cache_dir / 'hub'
    if models_dir.exists():
        model_dirs = [d for d in models_dir.iterdir() if d.is_dir() and d.name.startswith('models--')]
        
        if not model_dirs:
            print("No models found yet")
        else:
            for model_dir in sorted(model_dirs):
                # Extract model name from directory
                model_name = model_dir.name.replace('models--', '').replace('--', '/')
                
                # Get size
                size = sum(f.stat().st_size for f in model_dir.rglob('*') if f.is_file())
                size_gb = size / (1024**3)
                
                print(f"  • {model_name}")
                print(f"    Size: {size_gb:.2f} GB")
                print(f"    Path: {model_dir}")
                print()
    else:
        print("No models directory found yet")
    
    print("=" * 70)

def clear_cache():
    """Clear the model cache"""
    cache_dir = get_cache_dir()
    
    if not cache_dir.exists():
        print("❌ Cache directory does not exist")
        return
    
    print(f"\n⚠️  WARNING: This will delete all models in:")
    print(f"   {cache_dir}")
    
    response = input("\nAre you sure? (yes/no): ")
    if response.lower() == 'yes':
        try:
            shutil.rmtree(cache_dir)
            print("✅ Cache cleared successfully")
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")
    else:
        print("Cancelled")

def show_config():
    """Show current configuration"""
    print("\n⚙️  Current Configuration")
    print("=" * 70)
    
    cache_dir = get_cache_dir()
    print(f"Model Cache Directory: {cache_dir}")
    print(f"Exists: {'Yes' if cache_dir.exists() else 'No'}")
    
    if cache_dir.exists():
        total_size = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
        print(f"Total Size: {total_size / (1024**3):.2f} GB")
    
    print(f"\nModel Name: {os.getenv('MODEL_NAME', 'Qwen/Qwen3-0.6B')}")
    print(f"HF Token: {'Set' if os.getenv('HF_TOKEN') else 'Not set'}")
    print(f"Use GPU: {os.getenv('USE_GPU', 'true')}")
    print(f"Load in 8-bit: {os.getenv('LOAD_IN_8BIT', 'false')}")
    print(f"Load in 4-bit: {os.getenv('LOAD_IN_4BIT', 'false')}")
    print("=" * 70)

def setup_custom_dir():
    """Interactive setup for custom model directory"""
    print("\n🔧 Setup Custom Model Directory")
    print("=" * 70)
    
    current_cache = os.getenv('MODEL_CACHE_DIR')
    if current_cache:
        print(f"Current: {current_cache}")
    else:
        print("Current: Using default (~/.cache/huggingface)")
    
    print("\nEnter new path (or press Enter to use default):")
    new_path = input("> ").strip()
    
    if not new_path:
        print("Using default HuggingFace cache")
        return
    
    # Expand path
    new_path = os.path.expanduser(new_path)
    new_path = os.path.expandvars(new_path)
    
    # Create directory
    try:
        Path(new_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {new_path}")
        
        # Update .env file
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                lines = f.readlines()
            
            # Update or add MODEL_CACHE_DIR
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('MODEL_CACHE_DIR='):
                    lines[i] = f'MODEL_CACHE_DIR={new_path}\n'
                    updated = True
                    break
            
            if not updated:
                lines.append(f'\nMODEL_CACHE_DIR={new_path}\n')
            
            with open(env_file, 'w') as f:
                f.writelines(lines)
            
            print(f"✅ Updated .env file")
        else:
            print("⚠️  .env file not found. Please create it from .env.example")
            print(f"   Add this line: MODEL_CACHE_DIR={new_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("\n🤖 AI Model Manager")
        print("=" * 70)
        print("\nUsage:")
        print("  python manage_models.py <command>")
        print("\nCommands:")
        print("  list      - List all models in cache")
        print("  config    - Show current configuration")
        print("  setup     - Setup custom model directory")
        print("  clear     - Clear model cache (WARNING: deletes all models)")
        print("\nExamples:")
        print("  python manage_models.py list")
        print("  python manage_models.py setup")
        print("=" * 70)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_models()
    elif command == 'config':
        show_config()
    elif command == 'setup':
        setup_custom_dir()
    elif command == 'clear':
        clear_cache()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Run without arguments to see help")

if __name__ == '__main__':
    main()
