# 🚀 CropAI Production Deployment Guide

## Overview
- **Frontend**: React/Vite → **Vercel**
- **Backend**: Flask/Groq → **Render**
- **Database**: Supabase/Neon (future)
- **Model**: Scikit-learn ML in `/app/ml_training/models/`

---

## PHASE 1: BACKEND DEPLOYMENT (Render)

### Prerequisites
- GitHub account with repo access
- Render account (free tier)
- Groq API key (https://console.groq.com)

### Step 1: Create Render Service

1. Go to **https://render.com**
2. Click **New +** → **Web Service**
3. Connect GitHub → Select repo `AI-BASED-CROP-RECOMMANDATION-USING-NPK-VALUES`
4. **Service Settings**:
   - **Name**: `cropai-api` (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Root Directory**: `app`
   - **Deployment Plan**: Free (0.5 CPU, 512MB RAM)

### Step 2: Environment Variables on Render

Go to **Settings** → **Environment** and add:

```
FLASK_ENV=production
GROQ_API_KEY=<your-groq-api-key>
ALLOWED_ORIGINS=https://<your-vercel-domain>.vercel.app
FLASK_SECRET_KEY=<generate-random-secret>
AGMARKNET_API_URL=https://agmarknet.gov.in/Api1.0/prices
```

**To generate a random Flask secret**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Deploy & Get URL

1. Click **Deploy** (Render builds automatically from GitHub)
2. Wait for ✅ status (first deploy ~5 mins)
3. Copy live backend URL: `https://cropai-api.onrender.com` (or yours)
4. Save this URL for frontend setup

### Step 4: Test Backend Health

```bash
# Test health endpoint
curl https://cropai-api.onrender.com/health

# Expected: {"status": "ok"}
```

⚠️ **Note**: First request might be slow (cold start ~10s) on free tier.

---

## PHASE 2: FRONTEND DEPLOYMENT (Vercel)

### Prerequisites
- Vercel account (free)
- Backend URL from Phase 1

### Step 1: Update Frontend Env Vars

Edit `frontend/.env.production`:
```
VITE_API_URL=https://cropai-api.onrender.com
```

### Step 2: Commit Changes

```bash
cd frontend
git add .env.production vercel.json
git commit -m "chore: add Vercel production config"
git push origin main  # or your default branch
```

### Step 3: Connect Vercel to GitHub

1. Go to **https://vercel.com/new**
2. Click **Import Git Repository**
3. Select your GitHub repo
4. **Configure**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Root Directory**: `frontend`

### Step 4: Add Environment Variables in Vercel

In Vercel dashboard → **Settings** → **Environment Variables**:

```
VITE_API_URL=https://cropai-api.onrender.com
```

### Step 5: Deploy

1. Click **Deploy**
2. Wait for ✅ (builds in ~2 mins)
3. Copy frontend URL: `https://cropai-xxxx.vercel.app`

### Step 6: Update Render CORS

Go back to **Render** → **cropai-api** → **Settings** → **Environment**:

Update:
```
ALLOWED_ORIGINS=https://cropai-xxxx.vercel.app
```

---

## PHASE 3: INTEGRATION TEST

### Test API Connectivity

From Vercel frontend, open browser console and run:

```javascript
fetch('https://cropai-api.onrender.com/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    N: 50, P: 30, K: 40,
    temperature: 25, humidity: 60, ph: 7, rainfall: 800
  })
})
  .then(r => r.json())
  .then(d => console.log('✅ Success:', d))
  .catch(e => console.error('❌ Error:', e.message))
```

Expected response:
```json
{
  "prediction": "Rice",
  "confidence": 0.92,
  "ai_insight": "Based on NPK values and climate..."
}
```

---

## TROUBLESHOOTING

### ❌ CORS Error: "Access to XMLHttpRequest blocked"
**Fix**: Verify `ALLOWED_ORIGINS` in Render matches your Vercel domain exactly.

```bash
curl -H "Origin: https://cropai-xxxx.vercel.app" \
  https://cropai-api.onrender.com/api/predict -v
```

Check headers include: `Access-Control-Allow-Origin: https://cropai-xxxx.vercel.app`

### ❌ Groq API Error: "401 Unauthorized"
**Fix**: Re-check your `GROQ_API_KEY` in Render environment. Groq keys expire.

```bash
curl https://cropai-api.onrender.com/health
```

Check logs: Render → **Logs** → search for "Groq"

### ❌ Model Not Found: "crop_model_best.pkl not found"
**Fix**: Ensure model is committed to GitHub:

```bash
ls app/ml_training/models/crop_model_best.pkl
git add app/ml_training/models/crop_model_best.pkl
git commit -m "feat: include ML model for production"
git push
```

### ❌ Frontend Build Fails on Vercel
**Fix**: Check TypeScript errors:

```bash
cd frontend
npm run build
```

Common: Missing env vars. Vercel must have `VITE_API_URL` set.

### ❌ Cold Start Too Slow (>10s)
- **Expected**: Free Render tier sleeps after 15 mins of inactivity
- **Solution**: Upgrade to paid tier or accept cold start delay

---

## MONITORING & LOGS

### View Backend Logs (Render)
```
Render Dashboard → cropai-api → Logs
```

### View Frontend Deploy Logs (Vercel)
```
Vercel Dashboard → Deployments → Select deployment → Logs
```

### Check Live Health Status
```bash
curl https://cropai-api.onrender.com/health
curl https://cropai-xxxx.vercel.app  # Should return HTML
```

---

## ROLLBACK STEPS

### If Backend Breaks:
1. Render → **cropai-api** → **Deployment** → select previous ✅
2. Click **Rollback**

### If Frontend Breaks:
1. Vercel → **Deployments** → select previous ✅
2. Click **Redeploy**

---

## Next: Database (Supabase/Neon)

Once frontend + backend are stable, add:
- Supabase PostgreSQL for crop history, user sessions
- Update Flask to use SQLAlchemy + Supabase
- Implement user authentication

---

## Environment Variables Checklist

### Render (Backend)
- [ ] `GROQ_API_KEY` (from console.groq.com)
- [ ] `FLASK_ENV=production`
- [ ] `ALLOWED_ORIGINS=https://your-vercel-url`
- [ ] `FLASK_SECRET_KEY` (random 32 chars)
- [ ] `AGMARKNET_API_URL` (default: official URL)

### Vercel (Frontend)
- [ ] `VITE_API_URL=https://your-render-url`

---

## Support

- **Groq Issues**: https://support.groq.com
- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **This Repo**: Check GitHub Issues
