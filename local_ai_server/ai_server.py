#!/usr/bin/env python3
"""
Local AI Model Server with Ngrok Support
Hosts a Hugging Face model locally and exposes it via Ngrok
Enhanced with custom model storage and better performance options
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from pyngrok import ngrok
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Android app

# Global variables for model and tokenizer
model = None
tokenizer = None
device = None
start_time = None

def setup_model_cache():
    """Setup custom model cache directory if specified"""
    cache_dir = os.getenv('MODEL_CACHE_DIR')
    if cache_dir:
        # Expand ~ and environment variables
        cache_dir = os.path.expanduser(cache_dir)
        cache_dir = os.path.expandvars(cache_dir)
        
        # Create directory if it doesn't exist
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        
        # Set HuggingFace cache environment variables
        os.environ['TRANSFORMERS_CACHE'] = cache_dir
        os.environ['HF_HOME'] = cache_dir
        
        logger.info(f"Using custom model cache directory: {cache_dir}")
        return cache_dir
    else:
        logger.info("Using default HuggingFace cache directory")
        return None

def load_model():
    """Load the AI model and tokenizer with performance optimizations"""
    global model, tokenizer, device
    
    # Setup model cache
    cache_dir = setup_model_cache()
    
    model_name = os.getenv('MODEL_NAME', 'Qwen/Qwen3-0.6B')
    hf_token = os.getenv('HF_TOKEN', None)
    use_gpu = os.getenv('USE_GPU', 'true').lower() == 'true'
    load_in_8bit = os.getenv('LOAD_IN_8BIT', 'false').lower() == 'true'
    load_in_4bit = os.getenv('LOAD_IN_4BIT', 'false').lower() == 'true'
    
    logger.info(f"Loading model: {model_name}")
    if cache_dir:
        logger.info(f"Model storage location: {cache_dir}")
    
    # Determine device
    if use_gpu and torch.cuda.is_available():
        device = torch.device('cuda')
        logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device('cpu')
        logger.info("Using CPU")
    
    try:
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=hf_token,
            trust_remote_code=True,
            cache_dir=cache_dir
        )
        
        # Configure quantization if requested
        quantization_config = None
        if load_in_8bit or load_in_4bit:
            try:
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=load_in_8bit,
                    load_in_4bit=load_in_4bit,
                )
                logger.info(f"Using quantization: {'8-bit' if load_in_8bit else '4-bit'}")
            except ImportError:
                logger.warning("bitsandbytes not available, loading in full precision")
                quantization_config = None
        
        # Load model
        model_kwargs = {
            'token': hf_token,
            'trust_remote_code': True,
            'low_cpu_mem_usage': True,
            'cache_dir': cache_dir
        }
        
        if quantization_config:
            model_kwargs['quantization_config'] = quantization_config
        else:
            model_kwargs['torch_dtype'] = torch.float16 if device.type == 'cuda' else torch.float32
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            **model_kwargs
        )
        
        if not quantization_config:
            model.to(device)
        
        model.eval()
        
        logger.info("Model loaded successfully!")
        logger.info(f"Model parameters: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_response(prompt, max_length=None, temperature=None, top_p=None):
    """Generate a response from the model"""
    # Use defaults from environment if not specified
    max_length = max_length or int(os.getenv('DEFAULT_MAX_LENGTH', 100))
    temperature = temperature or float(os.getenv('DEFAULT_TEMPERATURE', 0.8))
    top_p = top_p or float(os.getenv('DEFAULT_TOP_P', 0.9))
    
    try:
        # Encode input
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode output
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt from response if it's included
        if response.startswith(prompt):
            response = response[len(prompt):].strip()
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise

@app.route('/', methods=['GET'])
def home():
    """Home page endpoint"""
    return jsonify({
        'name': 'Local AI Model Server',
        'version': '1.0.0',
        'status': 'running',
        'model': os.getenv('MODEL_NAME', 'Unknown'),
        'device': str(device) if device else None,
        'endpoints': {
            'health': '/health (GET)',
            'models': '/models (GET)',
            'chat': '/chat (POST)'
        },
        'usage': {
            'chat': {
                'method': 'POST',
                'url': '/chat',
                'body': {
                    'message': 'Your message here',
                    'max_length': 512,
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            }
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'device': str(device) if device else None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint compatible with Android app
    Expected JSON body:
    {
        "message": "User's message",
        "max_length": 512,  // optional
        "temperature": 0.7,  // optional
        "top_p": 0.9  // optional
    }
    """
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message in request'}), 400
        
        user_message = data['message']
        max_length = data.get('max_length', 512)
        temperature = data.get('temperature', 0.7)
        top_p = data.get('top_p', 0.9)
        
        logger.info(f"Received message: {user_message}")
        
        # Generate response
        response = generate_response(
            user_message,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p
        )
        
        logger.info(f"Generated response: {response}")
        
        return jsonify({
            'response': response,
            'model': os.getenv('MODEL_NAME', 'Unknown'),
            'device': str(device)
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/models', methods=['GET'])
def get_model_info():
    """Get information about the loaded model"""
    return jsonify({
        'model_name': os.getenv('MODEL_NAME', 'Unknown'),
        'device': str(device) if device else None,
        'model_loaded': model is not None
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Get current server configuration"""
    try:
        cache_dir = os.getenv('MODEL_CACHE_DIR', 'Default (~/.cache/huggingface)')
        if cache_dir != 'Default (~/.cache/huggingface)':
            cache_dir = os.path.expanduser(cache_dir)
            cache_dir = os.path.expandvars(cache_dir)
        
        config = {
            'model_name': os.getenv('MODEL_NAME', 'Qwen/Qwen3-0.6B'),
            'model_cache_dir': cache_dir,
            'port': int(os.getenv('PORT', 5000)),
            'host': os.getenv('HOST', '0.0.0.0'),
            'use_gpu': os.getenv('USE_GPU', 'true').lower() == 'true',
            'load_in_8bit': os.getenv('LOAD_IN_8BIT', 'false').lower() == 'true',
            'load_in_4bit': os.getenv('LOAD_IN_4BIT', 'false').lower() == 'true',
            'default_max_length': int(os.getenv('DEFAULT_MAX_LENGTH', 100)),
            'default_temperature': float(os.getenv('DEFAULT_TEMPERATURE', 0.8)),
            'default_top_p': float(os.getenv('DEFAULT_TOP_P', 0.9)),
            'has_hf_token': bool(os.getenv('HF_TOKEN')),
            'device': str(device) if device else 'Not initialized',
            'model_loaded': model is not None,
            'cuda_available': torch.cuda.is_available(),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        }
        
        return jsonify(config)
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/config', methods=['POST'])
def update_config():
    """
    Update server configuration
    Note: Changes require server restart to take effect
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No configuration data provided'}), 400
        
        # Read current .env file
        env_path = Path(__file__).parent / '.env'
        env_content = {}
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_content[key] = value
        
        # Update with new values
        updated_fields = []
        
        if 'model_name' in data:
            env_content['MODEL_NAME'] = data['model_name']
            updated_fields.append('model_name')
        
        if 'model_cache_dir' in data:
            env_content['MODEL_CACHE_DIR'] = data['model_cache_dir']
            updated_fields.append('model_cache_dir')
        
        if 'use_gpu' in data:
            env_content['USE_GPU'] = str(data['use_gpu']).lower()
            updated_fields.append('use_gpu')
        
        if 'load_in_8bit' in data:
            env_content['LOAD_IN_8BIT'] = str(data['load_in_8bit']).lower()
            updated_fields.append('load_in_8bit')
        
        if 'load_in_4bit' in data:
            env_content['LOAD_IN_4BIT'] = str(data['load_in_4bit']).lower()
            updated_fields.append('load_in_4bit')
        
        if 'default_max_length' in data:
            env_content['DEFAULT_MAX_LENGTH'] = str(data['default_max_length'])
            updated_fields.append('default_max_length')
        
        if 'default_temperature' in data:
            env_content['DEFAULT_TEMPERATURE'] = str(data['default_temperature'])
            updated_fields.append('default_temperature')
        
        if 'default_top_p' in data:
            env_content['DEFAULT_TOP_P'] = str(data['default_top_p'])
            updated_fields.append('default_top_p')
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            f.write("# Server Configuration - Updated via API\n")
            f.write("# Changes require server restart to take effect\n\n")
            
            # Write ngrok config
            if 'NGROK_AUTH_TOKEN' in env_content:
                f.write(f"NGROK_AUTH_TOKEN={env_content['NGROK_AUTH_TOKEN']}\n\n")
            
            # Write model config
            f.write("# Model Configuration\n")
            f.write(f"MODEL_NAME={env_content.get('MODEL_NAME', 'Qwen/Qwen3-0.6B')}\n")
            if 'MODEL_CACHE_DIR' in env_content:
                f.write(f"MODEL_CACHE_DIR={env_content['MODEL_CACHE_DIR']}\n")
            f.write("\n")
            
            # Write server config
            f.write("# Server Configuration\n")
            f.write(f"PORT={env_content.get('PORT', '5000')}\n")
            f.write(f"HOST={env_content.get('HOST', '0.0.0.0')}\n\n")
            
            # Write HF token if exists
            if 'HF_TOKEN' in env_content:
                f.write(f"HF_TOKEN={env_content['HF_TOKEN']}\n\n")
            
            # Write performance config
            f.write("# Performance Optimization\n")
            f.write(f"USE_GPU={env_content.get('USE_GPU', 'true')}\n")
            f.write(f"LOAD_IN_8BIT={env_content.get('LOAD_IN_8BIT', 'false')}\n")
            f.write(f"LOAD_IN_4BIT={env_content.get('LOAD_IN_4BIT', 'false')}\n\n")
            
            # Write generation defaults
            f.write("# Generation Defaults\n")
            f.write(f"DEFAULT_MAX_LENGTH={env_content.get('DEFAULT_MAX_LENGTH', '100')}\n")
            f.write(f"DEFAULT_TEMPERATURE={env_content.get('DEFAULT_TEMPERATURE', '0.8')}\n")
            f.write(f"DEFAULT_TOP_P={env_content.get('DEFAULT_TOP_P', '0.9')}\n")
        
        logger.info(f"Configuration updated: {updated_fields}")
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully',
            'updated_fields': updated_fields,
            'note': 'Restart the server for changes to take effect'
        })
        
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/system', methods=['GET'])
def get_system_info():
    """Get system information and resource usage"""
    try:
        import psutil
        import time
        
        # Get memory info
        memory = psutil.virtual_memory()
        
        # Get model memory usage if available
        model_memory = None
        if model is not None and torch.cuda.is_available() and device.type == 'cuda':
            model_memory = torch.cuda.memory_allocated(device) / 1024**3  # GB
            max_memory = torch.cuda.get_device_properties(device).total_memory / 1024**3
        
        info = {
            'uptime_seconds': time.time() - start_time,
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_total_gb': memory.total / 1024**3,
            'memory_used_gb': memory.used / 1024**3,
            'memory_percent': memory.percent,
            'model_loaded': model is not None,
            'device': str(device) if device else None,
            'cuda_available': torch.cuda.is_available()
        }
        
        if model_memory:
            info['gpu_memory_used_gb'] = model_memory
            info['gpu_memory_total_gb'] = max_memory
        
        return jsonify(info)
        
    except ImportError:
        return jsonify({
            'error': 'psutil not installed',
            'note': 'Install with: pip install psutil'
        }), 500
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/restart', methods=['POST'])
def restart_server():
    """
    Trigger server restart
    Note: This requires external process manager (systemd, supervisor, etc.)
    """
    try:
        logger.info("Restart requested via API")
        
        # Signal that restart is needed
        with open('restart_requested.flag', 'w') as f:
            f.write('1')
        
        return jsonify({
            'success': True,
            'message': 'Restart signal sent',
            'note': 'Server will restart if managed by a process supervisor'
        })
        
    except Exception as e:
        logger.error(f"Error requesting restart: {e}")
        return jsonify({'error': str(e)}), 500

def setup_ngrok():
    """Setup ngrok tunnel"""
    ngrok_token = os.getenv('NGROK_AUTH_TOKEN')
    
    if not ngrok_token:
        logger.warning("No NGROK_AUTH_TOKEN found. Ngrok will run without authentication.")
        logger.warning("Get a free token at: https://dashboard.ngrok.com/signup")
    else:
        ngrok.set_auth_token(ngrok_token)
    
    port = int(os.getenv('PORT', 5000))
    
    # Start ngrok tunnel
    public_url = ngrok.connect(port)
    logger.info('=' * 80)
    logger.info(f"🌐 Ngrok tunnel started!")
    logger.info(f"🔗 Public URL: {public_url}")
    logger.info(f"📱 Use this URL in your Android app: {public_url}")
    logger.info('=' * 80)
    
    return public_url

if __name__ == '__main__':
    import time
    start_time = time.time()
    
    logger.info("Starting AI Model Server...")
    
    # Load the model
    if not load_model():
        logger.error("Failed to load model. Exiting.")
        exit(1)
    
    # Setup ngrok
    try:
        public_url = setup_ngrok()
        
        # Save the URL to a file for easy reference
        with open('ngrok_url.txt', 'w') as f:
            f.write(str(public_url))
        logger.info("Ngrok URL saved to ngrok_url.txt")
        
    except Exception as e:
        logger.error(f"Error setting up ngrok: {e}")
        logger.info("Continuing without ngrok...")
    
    # Start Flask server
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting Flask server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
