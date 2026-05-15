# app.py - PRODUCTION READY WITH LLAMA 3
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import joblib
import os
import pandas as pd
import requests
import random
import logging
from datetime import datetime, timedelta
import ollama  # Required: pip install ollama

# ==================== CONFIGURATION ====================
class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-production')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'ml_training', 'models', 'crop_model_best.pkl')
    OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama3')
    OLLAMA_TIMEOUT = int(os.environ.get('OLLAMA_TIMEOUT', '60'))
    AGMARKNET_API_URL = os.environ.get('AGMARKNET_API_URL', 'https://agmarknet.gov.in/Api1.0/prices')
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '10'))
    CACHE_TIMEOUT = timedelta(minutes=15)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    VALIDATION_RANGES = {
        'N': (0, 200), 'P': (0, 150), 'K': (0, 250),
        'temperature': (-10, 50), 'humidity': (0, 100),
        'ph': (0, 14), 'rainfall': (0, 3000)
    }

# ==================== LOGGING SETUP ====================
def setup_logging():
    log_level = logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG
    log_dir = os.path.join(Config.BASE_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log'), encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    if os.environ.get('FLASK_ENV') == 'production':
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
    return logging.getLogger(__name__)

logger = setup_logging()

# ==================== FLASK APP FACTORY ====================
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/api/*": {"origins": os.environ.get('ALLOWED_ORIGINS', '*')}})
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    
    # Load model once at startup
    try:
        model = joblib.load(Config.MODEL_PATH)
        logger.info(f"✅ Model loaded successfully from {Config.MODEL_PATH}")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        model = None
        
    with app.app_context():
        validate_app_startup(model)
        
    register_routes(app, limiter, model)
    register_error_handlers(app)
    return app

# ==================== STARTUP VALIDATION ====================
def validate_app_startup(model):
    logger.info("🔍 Validating application startup...")
    
    if model is None:
        logger.warning("⚠️  Model not loaded. Prediction features will be disabled.")
    
    # Check Ollama connection
    try:
        response = requests.get(Config.OLLAMA_HOST, timeout=5)
        logger.info(f"✅ Ollama server reachable: {response.status_code}")
        
        # Check if llama3 model is available
        try:
            models = ollama.list()
            model_names = [m['name'] for m in models['models']]
            if Config.OLLAMA_MODEL in model_names or any(Config.OLLAMA_MODEL in m for m in model_names):
                logger.info(f"✅ Llama3 model found: {Config.OLLAMA_MODEL}")
            else:
                logger.warning(f"⚠️  Llama3 model not found. Run: ollama pull {Config.OLLAMA_MODEL}")
        except Exception as e:
            logger.warning(f"⚠️  Could not list Ollama models: {e}")
            
    except requests.RequestException as e:
        logger.error(f"❌ Ollama server not reachable: {e}")
        logger.error("📝 To fix: 1) Install Ollama from https://ollama.com")
        logger.error("           2) Run: ollama pull llama3")
        logger.error("           3) Run: ollama serve")

# ==================== ROUTE REGISTRATION ====================
def register_routes(app, limiter, model):
    
    @app.context_processor
    def inject_agri_year():
        now = datetime.now()
        year = now.year if now.month >= 4 else now.year - 1
        return {'agri_year': f"{year}-{year + 1}"}
    
    # ==================== HELPER FUNCTIONS ====================
    IMAGE_CACHE = {}
    
    CROP_SEARCH_TERMS = {
        'rice': 'rice paddy field', 'wheat': 'wheat field ready for harvest', 
        'maize': 'corn field maize', 'chickpea': 'chickpea crop', 
        'kidneybeans': 'kidney beans plant', 'pigeonpea': 'pigeon pea crop',
        'moong': 'mung bean plant', 'mothbeans': 'moth bean crop', 
        'urad': 'black gram crop', 'cotton': 'cotton field', 
        'oilseeds': 'oilseed crop', 'sugarcane': 'sugarcane field',
        'potato': 'potato farm', 'onion': 'onion farm', 
        'tomato': 'tomato plant ripe', 'groundnut': 'groundnut peanut field', 
        'soybean': 'soybean crop', 'mustard': 'mustard field yellow',
        'jowar': 'sorghum jowar field', 'bajra': 'pearl millet bajra', 
        'barley': 'barley field', 'ragi': 'finger millet ragi'
    }
    
    def get_crop_image_url(crop_name):
        crop_name = crop_name.lower().strip()
        if crop_name in IMAGE_CACHE:
            return IMAGE_CACHE[crop_name]
            
        for ext in ['jpg', 'jpeg', 'png', 'webp']:
            local_path = os.path.join(app.root_path, 'static', 'images', 'crop', f'{crop_name}.{ext}')
            if os.path.exists(local_path):
                url = f'/static/images/crop/{crop_name}.{ext}'
                IMAGE_CACHE[crop_name] = url
                return url
                
        search_term = CROP_SEARCH_TERMS.get(crop_name, f'{crop_name} crop farming')
        url = f'https://source.unsplash.com/800x600/?{search_term.replace(" ", ",")}'
        IMAGE_CACHE[crop_name] = url
        return url
    
    def validate_input_values(N, P, K, temperature, humidity, ph, rainfall):
        warnings = []
        recommendations = []
        ranges = Config.VALIDATION_RANGES
        
        checks = [
            ('N', N, 'Nitrogen'), ('P', P, 'Phosphorus'), ('K', K, 'Potassium'),
            ('temperature', temperature, 'Temperature'), ('humidity', humidity, 'Humidity'),
            ('ph', ph, 'pH'), ('rainfall', rainfall, 'Rainfall')
        ]
        
        for key, val, name in checks:
            min_v, max_v = ranges[key]
            if not (min_v <= val <= max_v):
                warnings.append(f"{name} out of optimal range ({min_v}-{max_v})")
                recommendations.append(f"Verify {name.lower()} sensor/test values")
                
        if ph < 4.0 or ph > 9.0:
            warnings.append(f"Soil pH {ph} is extreme (optimal: 6.0-7.5)")
            recommendations.append("Consult agricultural expert for pH correction")
        if temperature < 10 or temperature > 40:
            warnings.append(f"Temperature {temperature}°C may limit crop growth")
            recommendations.append("Consider season-appropriate crops")
            
        return warnings, recommendations
    
    def get_agriculture_chatbot_response(user_message, context_data):
        """
        REAL LLAMA 3 AI CHATBOT - Uses Ollama for actual AI responses
        """
        try:
            # Build contextual system prompt
            crop = context_data.get('crop', 'Unknown')
            n = context_data.get('N', 0)
            p = context_data.get('P', 0)
            k = context_data.get('K', 0)
            ph = context_data.get('ph', 7)
            temp = context_data.get('temperature', 25)
            humidity = context_data.get('humidity', 60)
            rainfall = context_data.get('rainfall', 100)
            
            system_prompt = f"""You are an expert AI Agricultural Consultant for Indian farmers and agriculture students.

CONTEXT FROM USER'S SOIL TEST:
- Recommended Crop: {crop}
- Soil Nutrients: N={n} mg/kg, P={p} mg/kg, K={k} mg/kg, pH={ph}
- Climate: Temperature={temp}°C, Humidity={humidity}%, Rainfall={rainfall}mm

YOUR ROLE:
1. Provide accurate, practical farming advice based on the soil data
2. Explain WHY the recommended crop suits these conditions
3. Give specific fertilizer, irrigation, and pest management tips
4. Use simple language that farmers can understand
5. Never guarantee profits or specific yields
6. Recommend consulting local Krishi Vigyan Kendra (KVK) for severe issues

RESPONSE GUIDELINES:
- Be concise but informative (3-5 sentences)
- Include specific NPK recommendations
- Mention water requirements
- Add one important warning or tip
- Use metric units (kg, mm, °C)
"""
            
            logger.info(f"🤖 Sending to Llama3: {user_message[:50]}...")
            
            # Call Ollama Llama3 API
            response = ollama.chat(
                model=Config.OLLAMA_MODEL,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_message}
                ],
                options={
                    'temperature': 0.3,  # Lower = more focused
                    'top_p': 0.9,
                    'num_predict': 500,  # Max tokens in response
                    'timeout': Config.OLLAMA_TIMEOUT
                }
            )
            
            ai_response = response['message']['content'].strip()
            logger.info(f"✅ Llama3 response received ({len(ai_response)} chars)")
            
            return ai_response
            
        except ollama.ResponseError as e:
            logger.error(f"❌ Ollama Response Error: {e}")
            return f"⚠️ AI service temporarily unavailable (Ollama error: {str(e)[:100]}). Please consult a local agricultural expert or try again in a moment."
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ Cannot connect to Ollama server: {e}")
            return "⚠️ Cannot connect to AI server. Please ensure Ollama is running: `ollama serve`. In the meantime, consult local agricultural experts."
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in chatbot: {type(e).__name__} - {e}")
            return f"⚠️ Error: {str(e)[:150]}. Please try again or consult an agricultural expert."
    
    # ==================== ROUTES ====================
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/predict', methods=['POST'])
    @limiter.limit("100 per hour")
    def predict():
        try:
            data = request.get_json() if request.is_json else request.form
            N = float(data['N'])
            P = float(data['P'])
            K = float(data['K'])
            temperature = float(data['temperature'])
            humidity = float(data['humidity'])
            ph = float(data['ph'])
            rainfall = float(data['rainfall'])
            
            warnings, recs = validate_input_values(N, P, K, temperature, humidity, ph, rainfall)
            input_df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                                    columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
            
            prediction = model.predict(input_df)[0]
            confidence = float(max(model.predict_proba(input_df)[0])) * 100
            
            # Store context for chatbot
            session['prediction_context'] = {
                'crop': prediction, 'N': N, 'P': P, 'K': K, 'ph': ph,
                'temperature': temperature, 'humidity': humidity, 'rainfall': rainfall
            }
            
            crop_img = get_crop_image_url(prediction.lower())
            
            if request.is_json:
                return jsonify({
                    'success': True, 'crop': prediction, 'confidence': round(confidence, 2),
                    'warnings': warnings, 'recommendations': recs, 'image_url': crop_img
                })
            else:
                return render_template('index.html',
                                       prediction_text=f'Recommended Crop: {prediction.upper()}',
                                       confidence_text=f'{confidence:.1f}%',
                                       crop_image_url=crop_img,
                                       input_data=f'N={N}, P={P}, K={K}, Temp={temperature}°C, Humidity={humidity}%, pH={ph}, Rainfall={rainfall}mm',
                                       warnings=warnings, recommendations=recs,
                                       crop_name=prediction)
        except Exception as e:
            logger.error(f"Prediction error: {e}", exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500 if request.is_json else render_template('index.html', prediction_text=f'Error: {str(e)}')
    
    @app.route('/api/chat', methods=['POST'])
    @limiter.limit("30 per hour")
    def api_chat():
        """REAL AI CHATBOT ENDPOINT - Uses Llama3 via Ollama"""
        try:
            data = request.json
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({'error': 'No message provided', 'response': ''}), 400
            
            if len(user_message) > 1000:
                return jsonify({'error': 'Message too long (max 1000 characters)', 'response': ''}), 400
            
            # Get context from session
            context = session.get('prediction_context', {})
            
            logger.info(f"💬 User query: {user_message[:100]}")
            
            # Call Llama3 AI
            response_text = get_agriculture_chatbot_response(user_message, context)
            
            return jsonify({
                'success': True,
                'response': response_text,
                'model': Config.OLLAMA_MODEL,
                'context_used': bool(context)
            })
            
        except Exception as e:
            logger.error(f"Chat endpoint error: {e}")
            return jsonify({
                'success': False,
                'response': f"Error: {str(e)}",
                'model': 'error'
            }), 500
    
    @app.route('/api/market-price/<crop_name>')
    @limiter.limit("100 per hour")
    def get_market_price(crop_name):
        try:
            cache_key = f"price_{crop_name.lower()}"
            cached = session.get(cache_key)
            if cached and datetime.now() - cached['ts'] < Config.CACHE_TIMEOUT:
                cached['source'] = 'cache'
                return jsonify(cached)
                
            # Try AGMARKNET API
            try:
                url = f"{Config.AGMARKNET_API_URL}?commodity={crop_name.title()}&arrivalDate={datetime.now().strftime('%d-%m-%Y')}"
                resp = requests.get(url, headers={'User-Agent': 'CropAI/1.0'}, timeout=Config.REQUEST_TIMEOUT)
                if resp.status_code == 200 and resp.json():
                    data = resp.json()[0]
                    result = {
                        'success': True, 'price': data.get('modalPrice', 'N/A'),
                        'min': data.get('minPrice', 'N/A'), 'max': data.get('maxPrice', 'N/A'),
                        'market': data.get('market', 'Unknown'), 'state': data.get('stateName', 'Unknown'),
                        'source': 'live', 'ts': datetime.now()
                    }
                    session[cache_key] = result
                    return jsonify(result)
            except Exception:
                pass  # Fallback to mock
                
            # Mock data for all 22 crops
            mocks = {
                'rice': {'price': 2450, 'min': 2300, 'max': 2600, 'market': 'Mumbai', 'state': 'Maharashtra'},
                'wheat': {'price': 2250, 'min': 2150, 'max': 2350, 'market': 'Delhi', 'state': 'Delhi'},
                'maize': {'price': 1850, 'min': 1750, 'max': 1950, 'market': 'Bangalore', 'state': 'Karnataka'},
                'chickpea': {'price': 5500, 'min': 5300, 'max': 5700, 'market': 'Kanpur', 'state': 'Uttar Pradesh'},
                'kidneybeans': {'price': 6800, 'min': 6500, 'max': 7100, 'market': 'Indore', 'state': 'Madhya Pradesh'},
                'pigeonpea': {'price': 6200, 'min': 6000, 'max': 6400, 'market': 'Solapur', 'state': 'Maharashtra'},
                'moong': {'price': 7200, 'min': 7000, 'max': 7400, 'market': 'Kota', 'state': 'Rajasthan'},
                'mothbeans': {'price': 4200, 'min': 4000, 'max': 4400, 'market': 'Bikaner', 'state': 'Rajasthan'},
                'urad': {'price': 6800, 'min': 6600, 'max': 7000, 'market': 'Bhopal', 'state': 'Madhya Pradesh'},
                'cotton': {'price': 6500, 'min': 6200, 'max': 6800, 'market': 'Ahmedabad', 'state': 'Gujarat'},
                'oilseeds': {'price': 4500, 'min': 4300, 'max': 4700, 'market': 'Rajkot', 'state': 'Gujarat'},
                'sugarcane': {'price': 3200, 'min': 3100, 'max': 3300, 'market': 'Kolhapur', 'state': 'Maharashtra'},
                'potato': {'price': 1200, 'min': 1000, 'max': 1400, 'market': 'Agra', 'state': 'Uttar Pradesh'},
                'onion': {'price': 1800, 'min': 1500, 'max': 2100, 'market': 'Nashik', 'state': 'Maharashtra'},
                'tomato': {'price': 1500, 'min': 1200, 'max': 1800, 'market': 'Pune', 'state': 'Maharashtra'},
                'groundnut': {'price': 5200, 'min': 5000, 'max': 5400, 'market': 'Rajkot', 'state': 'Gujarat'},
                'soybean': {'price': 4200, 'min': 4000, 'max': 4400, 'market': 'Indore', 'state': 'Madhya Pradesh'},
                'mustard': {'price': 4800, 'min': 4600, 'max': 5000, 'market': 'Jaipur', 'state': 'Rajasthan'},
                'jowar': {'price': 2800, 'min': 2700, 'max': 2900, 'market': 'Pune', 'state': 'Maharashtra'},
                'bajra': {'price': 2100, 'min': 2000, 'max': 2200, 'market': 'Jodhpur', 'state': 'Rajasthan'},
                'barley': {'price': 1650, 'min': 1550, 'max': 1750, 'market': 'Jaipur', 'state': 'Rajasthan'},
                'ragi': {'price': 3200, 'min': 3100, 'max': 3300, 'market': 'Bangalore', 'state': 'Karnataka'}
            }
            
            if crop_name.lower() in mocks:
                d = mocks[crop_name.lower()]
                result = {'success': True, 'price': d['price'], 'min': d['min'], 'max': d['max'], 'market': d['market'], 'state': d['state'], 'source': 'simulated', 'ts': datetime.now()}
                session[cache_key] = result
                return jsonify(result)
                
            return jsonify({'success': False, 'message': 'No price data available'}), 404
        except Exception as e:
            logger.error(f"Market price error: {e}")
            return jsonify({'success': False, 'error': 'Server error'}), 500
    
    @app.route('/health')
    def health():
        ollama_status = False
        try:
            requests.get(Config.OLLAMA_HOST, timeout=3)
            ollama_status = True
        except:
            pass
            
        return jsonify({
            'status': 'healthy' if model else 'degraded',
            'model_loaded': model is not None,
            'ollama_available': ollama_status,
            'ollama_model': Config.OLLAMA_MODEL,
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/quick-tip')
    def quick_tip():
        tips = [
            "Maintain soil pH between 6.0-7.5 for optimal nutrient absorption",
            "Test your soil every 6 months to monitor NPK levels",
            "Most crops need 6-8 hours of sunlight daily",
            "Drip irrigation saves 30-50% water compared to flood irrigation",
            "Practice crop rotation to maintain soil fertility"
        ]
        return jsonify({'tip': random.choice(tips)})
    
    @app.route('/chat')
    def chat_page(): return render_template('chat.html')
    @app.route('/crop-calendar')
    def crop_calendar(): return render_template('crop-calendar.html')
    @app.route('/market-prices')
    def market_prices_page(): return render_template('market-prices.html')

# ==================== ERROR HANDLERS ====================
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e): return jsonify({'error': 'Resource not found'}), 404
    @app.errorhandler(500)
    def server_error(e): 
        logger.error(f"Internal error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    @app.errorhandler(429)
    def rate_limit(e): return jsonify({'error': 'Rate limit exceeded. Try again later.'}), 429

# ==================== ENTRY POINT ====================
if __name__ == '__main__':
    app = create_app()
    env = os.environ.get('FLASK_ENV', 'development')
    logger.info(f"🚀 Starting Crop AI System in {env} mode on http://0.0.0.0:5000")
    logger.info(f"🤖 Using Llama3 model: {Config.OLLAMA_MODEL}")
    app.run(debug=(env == 'development'), port=5000, host='0.0.0.0')