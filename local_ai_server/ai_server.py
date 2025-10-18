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
