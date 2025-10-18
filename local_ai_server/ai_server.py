#!/usr/bin/env python3
"""
Local AI Model Server with Ngrok Support
Hosts a Hugging Face model locally and exposes it via Ngrok
Enhanced with custom model storage and better performance options
Includes web search capabilities for online research
"""

import os
import logging
import json
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from pyngrok import ngrok
from dotenv import load_dotenv
from pathlib import Path
from ddgs import DDGS
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Web Interface HTML Template
WEB_INTERFACE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local AI Server - Web Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            background: none;
            border: none;
            font-size: 16px;
            color: #666;
            transition: all 0.3s;
        }
        .tab.active {
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }
        .tab:hover {
            color: #667eea;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .input-group {
            margin-bottom: 15px;
        }
        .input-group label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 600;
        }
        .input-group input, .input-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .input-group input:focus, .input-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .input-group textarea {
            min-height: 100px;
            resize: vertical;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn:active {
            transform: translateY(0);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .response-box {
            margin-top: 20px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: none;
        }
        .response-box.show {
            display: block;
        }
        .response-box h3 {
            margin-bottom: 10px;
            color: #667eea;
        }
        .response-box pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .search-result {
            padding: 15px;
            margin-bottom: 10px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .search-result h4 {
            color: #667eea;
            margin-bottom: 5px;
        }
        .search-result a {
            color: #764ba2;
            text-decoration: none;
            font-size: 14px;
        }
        .search-result a:hover {
            text-decoration: underline;
        }
        .search-result p {
            margin-top: 10px;
            color: #666;
            line-height: 1.5;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .info-item {
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            color: white;
        }
        .info-item h3 {
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        .info-item p {
            font-size: 1.5em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Local AI Server</h1>
            <p>Chat with AI, Search the Web, and More!</p>
        </div>

        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('chat')">💬 AI Chat</button>
                <button class="tab" onclick="switchTab('search')">🔍 Web Search</button>
                <button class="tab" onclick="switchTab('research')">🌐 Search & Chat</button>
                <button class="tab" onclick="switchTab('info')">ℹ️ Server Info</button>
            </div>

            <!-- Chat Tab -->
            <div id="chat" class="tab-content active">
                <h2>AI Chat</h2>
                <div class="input-group">
                    <label for="chatMessage">Your Message:</label>
                    <textarea id="chatMessage" placeholder="Type your message here..."></textarea>
                </div>
                <button class="btn" onclick="sendChat()">Send Message</button>
                
                <div id="chatLoading" class="loading">
                    <div class="spinner"></div>
                    <p>AI is thinking...</p>
                </div>
                
                <div id="chatResponse" class="response-box">
                    <h3>AI Response:</h3>
                    <pre id="chatResponseText"></pre>
                </div>
            </div>

            <!-- Search Tab -->
            <div id="search" class="tab-content">
                <h2>Web Search</h2>
                <div class="input-group">
                    <label for="searchQuery">Search Query:</label>
                    <input type="text" id="searchQuery" placeholder="Enter your search query...">
                </div>
                <button class="btn" onclick="performSearch()">Search</button>
                
                <div id="searchLoading" class="loading">
                    <div class="spinner"></div>
                    <p>Searching...</p>
                </div>
                
                <div id="searchResults" class="response-box">
                    <h3>Search Results:</h3>
                    <div id="searchResultsList"></div>
                </div>
            </div>

            <!-- Research Tab -->
            <div id="research" class="tab-content">
                <h2>Search & Chat (AI Research)</h2>
                <p style="margin-bottom: 20px; color: #666;">Ask a question and the AI will search the web and provide an informed answer.</p>
                <div class="input-group">
                    <label for="researchQuery">Your Question:</label>
                    <textarea id="researchQuery" placeholder="Ask anything..."></textarea>
                </div>
                <button class="btn" onclick="searchAndChat()">Research & Answer</button>
                
                <div id="researchLoading" class="loading">
                    <div class="spinner"></div>
                    <p>Researching and generating answer...</p>
                </div>
                
                <div id="researchResponse" class="response-box">
                    <h3>AI Research Response:</h3>
                    <pre id="researchResponseText"></pre>
                </div>
            </div>

            <!-- Info Tab -->
            <div id="info" class="tab-content">
                <h2>Server Information</h2>
                <div id="serverInfo" class="info-grid">
                    <div class="info-item">
                        <h3>Status</h3>
                        <p>Loading...</p>
                    </div>
                </div>
                <button class="btn" onclick="loadServerInfo()" style="margin-top: 20px;">Refresh Info</button>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Load server info when info tab is opened
            if (tabName === 'info') {
                loadServerInfo();
            }
        }

        async function sendChat() {
            const message = document.getElementById('chatMessage').value;
            if (!message.trim()) {
                alert('Please enter a message');
                return;
            }

            const loading = document.getElementById('chatLoading');
            const responseBox = document.getElementById('chatResponse');
            const responseText = document.getElementById('chatResponseText');
            
            loading.classList.add('show');
            responseBox.classList.remove('show');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                if (response.ok) {
                    responseText.textContent = data.response;
                    responseBox.classList.add('show');
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                loading.classList.remove('show');
            }
        }

        async function performSearch() {
            const query = document.getElementById('searchQuery').value;
            if (!query.trim()) {
                alert('Please enter a search query');
                return;
            }

            const loading = document.getElementById('searchLoading');
            const resultsBox = document.getElementById('searchResults');
            const resultsList = document.getElementById('searchResultsList');
            
            loading.classList.add('show');
            resultsBox.classList.remove('show');

            try {
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query, max_results: 5 })
                });

                const data = await response.json();
                
                if (response.ok) {
                    resultsList.innerHTML = '';
                    data.results.forEach(result => {
                        const div = document.createElement('div');
                        div.className = 'search-result';
                        div.innerHTML = `
                            <h4>${result.title}</h4>
                            <a href="${result.link}" target="_blank">${result.link}</a>
                            <p>${result.snippet}</p>
                        `;
                        resultsList.appendChild(div);
                    });
                    resultsBox.classList.add('show');
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                loading.classList.remove('show');
            }
        }

        async function searchAndChat() {
            const query = document.getElementById('researchQuery').value;
            if (!query.trim()) {
                alert('Please enter a question');
                return;
            }

            const loading = document.getElementById('researchLoading');
            const responseBox = document.getElementById('researchResponse');
            const responseText = document.getElementById('researchResponseText');
            
            loading.classList.add('show');
            responseBox.classList.remove('show');

            try {
                const response = await fetch('/search_and_chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();
                
                if (response.ok) {
                    responseText.textContent = data.response;
                    responseBox.classList.add('show');
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                loading.classList.remove('show');
            }
        }

        async function loadServerInfo() {
            const infoGrid = document.getElementById('serverInfo');
            infoGrid.innerHTML = '<div class="info-item"><h3>Loading...</h3><p>Please wait</p></div>';

            try {
                const response = await fetch('/config');
                const data = await response.json();
                
                infoGrid.innerHTML = `
                    <div class="info-item">
                        <h3>🤖 Model</h3>
                        <p>${data.model_name}</p>
                    </div>
                    <div class="info-item">
                        <h3>💻 Device</h3>
                        <p>${data.device}</p>
                    </div>
                    <div class="info-item">
                        <h3>🔋 Status</h3>
                        <p>${data.model_loaded ? 'Ready' : 'Loading'}</p>
                    </div>
                    <div class="info-item">
                        <h3>🌐 Features</h3>
                        <p>AI Chat, Web Search, Research</p>
                    </div>
                `;
            } catch (error) {
                infoGrid.innerHTML = `<div class="info-item"><h3>Error</h3><p>${error.message}</p></div>`;
            }
        }

        // Load server info on page load
        window.addEventListener('DOMContentLoaded', () => {
            // Initial load not needed unless on info tab
        });
    </script>
</body>
</html>
"""

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

def search_web(query, max_results=5):
    """
    Perform web search using DuckDuckGo
    Returns a list of search results with title, link, and snippet
    """
    try:
        logger.info(f"Performing web search for: {query}")
        
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    'title': r.get('title', ''),
                    'link': r.get('href', ''),
                    'snippet': r.get('body', '')
                })
            
            logger.info(f"Found {len(results)} search results")
            return results
            
    except Exception as e:
        logger.error(f"Error performing web search: {e}")
        return []

def search_and_summarize(query, user_question):
    """
    Search the web and use AI to summarize the results
    """
    try:
        # Perform web search
        search_results = search_web(query, max_results=5)
        
        if not search_results:
            return "I couldn't find any information on the web about that topic."
        
        # Format search results for the AI
        context = f"User question: {user_question}\n\nWeb search results:\n\n"
        for i, result in enumerate(search_results, 1):
            context += f"{i}. {result['title']}\n{result['snippet']}\n\n"
        
        # Add instruction for the AI
        prompt = f"{context}\nBased on the search results above, please provide a comprehensive answer to the user's question. Include relevant information from the search results and cite sources when appropriate."
        
        # Generate AI response using the search context
        response = generate_response(prompt, max_length=300, temperature=0.7, top_p=0.9)
        
        # Append sources
        sources = "\n\nSources:\n"
        for i, result in enumerate(search_results[:3], 1):
            sources += f"{i}. {result['title']}: {result['link']}\n"
        
        return response + sources
        
    except Exception as e:
        logger.error(f"Error in search_and_summarize: {e}")
        return f"Error performing web search: {str(e)}"

@app.route('/', methods=['GET'])
def home():
    """Home page endpoint with web interface"""
    # Check if request is from a browser (wants HTML) or API (wants JSON)
    if request.headers.get('Accept', '').find('text/html') != -1:
        # Return web interface
        return render_template_string(WEB_INTERFACE_HTML)
    else:
        # Return API info
        return jsonify({
            'name': 'Local AI Model Server with Web Search',
            'version': '2.0.0',
            'status': 'running',
            'model': os.getenv('MODEL_NAME', 'Unknown'),
            'device': str(device) if device else None,
            'features': [
                'AI Chat',
                'Web Search',
                'Search & Summarize'
            ],
            'endpoints': {
                'health': '/health (GET)',
                'models': '/models (GET)',
                'chat': '/chat (POST)',
                'search': '/search (POST)',
                'search_and_chat': '/search_and_chat (POST)'
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
                },
                'search': {
                    'method': 'POST',
                    'url': '/search',
                    'body': {
                        'query': 'Your search query',
                        'max_results': 5
                    }
                },
                'search_and_chat': {
                    'method': 'POST',
                    'url': '/search_and_chat',
                    'body': {
                        'query': 'Your question',
                        'search_query': 'Optional specific search query'
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

@app.route('/search', methods=['POST'])
def search():
    """
    Web search endpoint
    Expected JSON body:
    {
        "query": "Search query",
        "max_results": 5  // optional
    }
    """
    try:
        data = request.json
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query in request'}), 400
        
        query = data['query']
        max_results = data.get('max_results', 5)
        
        logger.info(f"Search query: {query}")
        
        # Perform web search
        results = search_web(query, max_results=max_results)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/search_and_chat', methods=['POST'])
def search_and_chat():
    """
    Search the web and use AI to answer based on results
    Expected JSON body:
    {
        "query": "User's question",
        "search_query": "Optional specific search query"
    }
    """
    try:
        data = request.json
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query in request'}), 400
        
        user_query = data['query']
        search_query = data.get('search_query', user_query)
        
        logger.info(f"Search and chat query: {user_query}")
        
        # Search and summarize
        response = search_and_summarize(search_query, user_query)
        
        return jsonify({
            'query': user_query,
            'response': response,
            'model': os.getenv('MODEL_NAME', 'Unknown'),
            'device': str(device)
        })
        
    except Exception as e:
        logger.error(f"Error in search_and_chat endpoint: {e}")
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
