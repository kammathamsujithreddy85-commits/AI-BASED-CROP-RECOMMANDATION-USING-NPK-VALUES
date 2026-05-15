"""
AI Chat Response Generator
You can integrate with:
- OpenAI GPT
- Google Gemini
- Ollama (local)
- Custom rule-based system
"""

import random
from datetime import datetime

# Simple rule-based AI (Replace with actual AI integration)
CROP_KNOWLEDGE_BASE = {
    'rice': {
        'keywords': ['rice', 'paddy', 'dhaan'],
        'response': """🌾 **Rice Cultivation Guide:**

**Sowing:** June-July with monsoon onset
**Varieties:** Use high-yielding varieties like Pusa Basmati, Swarna, or IR64
**Seed Rate:** 20-25 kg/acre for transplanting
**Spacing:** 20cm x 15cm for optimal growth

**Nutrient Management:**
- N:P:K = 80:40:40 kg/ha
- Apply neem-coated urea in 3 splits
- Basal dose at transplanting
- Top dressing at tillering and panicle initiation

**Water Management:**
- Maintain 5cm standing water during vegetative stage
- Drain 7-10 days before harvesting

**Common Issues:**
- Stem borer: Use Carbofuran 3G @ 10 kg/ha
- Brown planthopper: Spray Imidacloprid
- Blast disease: Use Tricyclazole fungicide

**Expected Yield:** 40-60 quintals/ha
**MSP 2024:** ₹2,183/quintal

💡 **Pro Tip:** Try System of Rice Intensification (SRI) for 20-30% higher yield with less water!"""
    },
    'wheat': {
        'keywords': ['wheat', 'gehun', 'gandum'],
        'response': """🌾 **Wheat Cultivation Guide:**

**Sowing:** November-December (Timely sowing crucial!)
**Varieties:** HD-2967, PBW-343, DBW-187
**Seed Rate:** 40-50 kg/acre
**Seed Treatment:** Treat with Thiram or Carbendazim

**Fertilizer Schedule:**
- N:P:K = 120:60:40 kg/ha
- Full P & K at sowing
- N in 3 splits: Basal, 1st irrigation, 2nd irrigation

**Irrigation Schedule (Critical Stages):**
1. Crown Root Initiation (21 days after sowing)
2. Tillering (40-45 days)
3. Jointing (60-65 days)
4. Flowering (80-85 days)
5. Milk stage (100-105 days)

**Weed Control:**
- Pre-emergence: Pendimethalin @ 1 L/ha
- Post-emergence: 2,4-D @ 500 ml/ha at 30-35 days

**Expected Yield:** 45-55 quintals/ha
**MSP 2024:** ₹2,275/quintal

💡 **Pro Tip:** Zero-till sowing saves water and gives 5-7% higher yield!"""
    },
    'npk': {
        'keywords': ['npk', 'fertilizer', 'nutrient', 'urea', 'dap'],
        'response': """🧪 **NPK Fertilizer Guide:**

**NPK Ratio by Crop:**

🌾 **Rice:** 80:40:40 (N:P₂O₅:K₂O kg/ha)
🌾 **Wheat:** 120:60:40
🌽 **Maize:** 120:60:40
🌱 **Cotton:** 120:60:60
🥔 **Potato:** 150:100:120
🍅 **Tomato:** 120:80:100

**Nitrogen (N) Sources:**
- Urea (46% N) - Most common
- Ammonium Sulphate (21% N)
- CAN (26% N)

**Phosphorus (P) Sources:**
- DAP (18% N + 46% P₂O₅)
- SSP (16% P₂O₅)
- TSP (46% P₂O₅)

**Potassium (K) Sources:**
- MOP (60% K₂O)
- SOP (50% K₂O + 18% S)

**Application Tips:**
✅ Apply N in splits (3-4 applications)
✅ Apply full P & K at basal dose
✅ Use neem-coated urea for slow release
✅ Soil test before fertilizer application

💡 **Pro Tip:** Use soil health card recommendations for precise fertilizer application!"""
    },
    'pest': {
        'keywords': ['pest', 'insect', 'disease', 'blast', 'borer', 'aphid'],
        'response': """🐛 **Integrated Pest Management (IPM):**

**Preventive Measures:**
1. Use resistant/tolerant varieties
2. Seed treatment with fungicides
3. Crop rotation
4. Maintain field sanitation
5. Optimal plant spacing

**Common Pests & Solutions:**

🌾 **Rice:**
- Stem borer: Carbofuran 3G @ 10 kg/ha
- Brown planthopper: Imidacloprid 17.8% SL @ 100 ml/ha
- Blast: Tricyclazole 75% WP @ 400g/ha

🌾 **Wheat:**
- Aphids: Dimethoate 30% EC @ 500 ml/ha
- Rust: Propiconazole 25% EC @ 500 ml/ha
- Termite: Chlorpyriphos 20% EC @ 2.5 L/ha

🌽 **Maize:**
- Fall armyworm: Emamectin benzoate 5% SG @ 220g/ha
- Stem borer: Cartap hydrochloride 50% SP @ 500g/ha

🌱 **Cotton:**
- Bollworm: Spinosad 45% SC @ 150 ml/ha
- Whitefly: Acetamiprid 20% SP @ 50g/ha

**Organic Options:**
🌿 Neem oil 3% spray
🌿 BT (Bacillus thuringiensis) for caterpillars
🌿 Pheromone traps for monitoring

💡 **Pro Tip:** Scout your field weekly and act at economic threshold levels!"""
    },
    'irrigation': {
        'keywords': ['irrigation', 'water', 'drip', 'sprinkler'],
        'response': """💧 **Irrigation Management:**

**Water Requirements by Crop:**

🌾 **Rice:** 1200-1500 mm (Flood irrigation)
🌾 **Wheat:** 450-650 mm (4-5 irrigations)
🌽 **Maize:** 500-800 mm (6-7 irrigations)
🌱 **Cotton:** 800-1000 mm (8-10 irrigations)
🥔 **Potato:** 600-800 mm (10-12 irrigations)

**Critical Irrigation Stages:**

🌾 **Wheat:**
1. Crown root initiation (21 DAS) - MOST CRITICAL
2. Tillering (40-45 DAS)
3. Jointing (60-65 DAS)
4. Flowering (80-85 DAS)
5. Milk stage (100-105 DAS)

🌽 **Maize:**
- Tasseling stage
- Silking stage
- Grain filling stage

**Water-Saving Techniques:**

💧 **Drip Irrigation:**
- Saves 40-60% water
- Increases yield 20-30%
- Best for: Vegetables, Cotton, Sugarcane
- Subsidy: 55-90% under PMKSY

💧 **Sprinkler Irrigation:**
- Saves 30-40% water
- Best for: Wheat, Close-growing crops
- Subsidy: 55-90% under PMKSY

💧 **Alternate Wetting & Drying (AWD) for Rice:**
- Saves 25-30% water
- No yield reduction
- Reduces methane emissions

💡 **Pro Tip:** Install soil moisture sensors for precision irrigation scheduling!"""
    },
    'organic': {
        'keywords': ['organic', 'natural', 'bio', 'vermicompost', 'jivamrut'],
        'response': """🌿 **Organic Farming Guide:**

**Organic Inputs:**

🌱 **Vermicompost:**
- Application: 2-5 tonnes/ha
- Benefits: Improves soil structure, water retention
- Cost: ₹3,000-5,000/tonne

🌱 **Jeevamrut:**
- Recipe: 10L cow urine + 10kg cow dung + 2kg jaggery + 2kg pulse flour + soil
- Ferment for 48 hours
- Apply @ 200L/acre every 15 days

🌱 **Bijamrut (Seed Treatment):**
- Mix: 5kg cow dung + 5L cow urine + 50g lime + water
- Treat seeds before sowing
- Protects from soil-borne diseases

🌱 **Ghanjeevamrut:**
- Solid form of Jeevamrut
- Apply @ 500 kg/ha as basal dose

**Organic Pest Control:**

🌿 **Neem-based:**
- Neem oil 3% spray
- Neem seed kernel extract 5%
- Acts as antifeedant & growth regulator

🌿 **Agniastra:**
- Boil 10kg neem leaves in 10L water
- Filter and spray
- Effective against sucking pests

🌿 **Dashparni Ark:**
- Fermented extract of 10 leaves
- Multi-purpose pest repellent

**Certification:**
- NPOP (National Programme for Organic Production)
- PGS-India (Participatory Guarantee System)
- Premium price: 15-25% higher

💡 **Pro Tip:** Start with 1 acre conversion. Full conversion takes 2-3 years!"""
    }
}

def get_ai_response(user_message):
    """
    Generate AI response based on user query
    Replace this with actual AI integration (OpenAI, Gemini, Ollama, etc.)
    """
    
    message_lower = user_message.lower()
    
    # Check for keywords in knowledge base
    for topic, data in CROP_KNOWLEDGE_BASE.items():
        if any(keyword in message_lower for keyword in data['keywords']):
            return data['response']
    
    # Check for crop-specific queries
    crops = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane', 'potato', 'tomato', 'onion']
    for crop in crops:
        if crop in message_lower:
            if crop in CROP_KNOWLEDGE_BASE:
                return CROP_KNOWLEDGE_BASE[crop]['response']
            else:
                return f"""🌾 **{crop.title()} Information:**

I can provide detailed information about {crop} cultivation. 

Please ask specific questions about:
- Sowing time and methods
- Fertilizer requirements
- Irrigation schedule
- Pest and disease management
- Harvesting and post-harvest

Or type '{crop} cultivation guide' for complete information!"""
    
    # Default responses for common queries
    if any(word in message_lower for word in ['hello', 'hi', 'namaste', 'hey']):
        return """🙏 Namaste! Welcome to CropAI Assistant!

I'm here to help you with:
🌾 Crop cultivation guidance
🧪 Soil health & nutrient management
🐛 Pest & disease control
💧 Irrigation techniques
🌿 Organic farming practices
💰 Government schemes & MSP

How can I assist you today?"""
    
    if any(word in message_lower for word in ['thank', 'thanks', 'dhanyavaad']):
        return """🙏 You're welcome! 

Remember:
✅ Test your soil regularly
✅ Use certified seeds
✅ Follow recommended practices
✅ Keep records of farm activities

Feel free to ask anytime. Happy Farming! 🌾"""
    
    if any(word in message_lower for word in ['scheme', 'subsidy', 'loan', 'pm-kisan']):
        return """💰 **Government Schemes for Farmers:**

**1. PM-KISAN:**
- ₹6,000/year in 3 installments
- Direct benefit transfer
- Eligibility: All landholding farmers

**2. PMFBY (Crop Insurance):**
- Premium: 2% (Kharif), 1.5% (Rabi)
- Covers yield losses
- Quick claim settlement

**3. Kisan Credit Card (KCC):**
- Crop loan up to ₹3 lakh
- Interest subsidy: 7% (on-time repayment)
- Effective interest: 4% p.a.

**4. PMKSY (Irrigation):**
- 55-90% subsidy on drip/sprinkler
- Water conservation focus

**5. Soil Health Card:**
- Free soil testing
- Crop-specific recommendations
- Valid for 3 years

**6. Kisan Samman Nidhi:**
- Same as PM-KISAN
- ₹2,000 per installment

💡 **Pro Tip:** Register on PM-KISAN portal or visit your local CSC/VLE for enrollment!"""
    
    if any(word in message_lower for word in ['weather', 'rain', 'forecast']):
        return """🌤️ **Weather Advisory:**

For accurate weather forecast in your area:

📱 **Download Apps:**
- IMD Weather (Official)
- Skymet Weather
- AccuWeather

📞 **Call:**
- 1800-180-1551 (Kisan Call Centre)
- They provide localized weather updates

🌐 **Website:**
- www.imd.gov.in (India Meteorological Dept)
- Enter your district for 5-day forecast

**General Tips:**
✅ Check forecast before sowing
✅ Avoid irrigation if rain expected
✅ Harvest before heavy rains
✅ Store grains in moisture-proof containers

💡 **Pro Tip:** Sign up for SMS weather alerts from your state agriculture department!"""
    
    # Fallback response
    return f"""🤔 I received your query: "{user_message}"

I can help you with:

🌾 **Crop-specific queries:**
   - "rice cultivation"
   - "wheat fertilizer"
   - "maize pest control"

🧪 **Soil & Nutrients:**
   - "NPK ratio for rice"
   - "soil pH improvement"
   - "organic manure"

💧 **Irrigation:**
   - "drip irrigation subsidy"
   - "water saving techniques"

🐛 **Pest Management:**
   - "stem borer control"
   - "organic pesticides"

💰 **Schemes:**
   - "PM-KISAN"
   - "crop insurance"

Please rephrase your question or ask about specific crops!"""