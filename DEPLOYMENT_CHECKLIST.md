# 📄 CropAI Production Deployment Checklist

**Project**: AI-Based Crop Recommendation Using NPK Values  
**Stack**: React/Vite (Vercel) + Flask/Groq (Render) + scikit-learn  
**Status**: Ready for deployment  
**Date**: 2026-05-15

---

## ✅ PRE-DEPLOYMENT CHECKLIST

### Backend (Flask/Render)

- [ ] **Code**
  - [ ] `app/app.py` has CORS configured with `ALLOWED_ORIGINS`
  - [ ] `app/Procfile` = `web: gunicorn app:app`
  - [ ] `app/requirements.txt` includes: Flask, flask-cors, groq, gunicorn, scikit-learn
  - [ ] `app/ml_training/models/crop_model_best.pkl` exists & is tracked in Git
  - [ ] No hardcoded API keys in code
  - [ ] Error handling for Groq failures (fallback to rule-based AI)

- [ ] **Environment**
  - [ ] `.env` file is Git-ignored
  - [ ] Env template created: `.env.example`
  - [ ] Vars needed: `GROQ_API_KEY`, `FLASK_ENV`, `ALLOWED_ORIGINS`, `FLASK_SECRET_KEY`

- [ ] **Render Setup**
  - [ ] Render account created (free tier OK)
  - [ ] GitHub repo connected to Render
  - [ ] Service created: name = `cropai-api`
  - [ ] Build command: `pip install -r requirements.txt`
  - [ ] Start command: `gunicorn app:app`
  - [ ] Root directory: `app`
  - [ ] Environment variables added (see table below)
  - [ ] Deployment successful (status = ✅)
  - [ ] Backend URL copied: `https://cropai-api.onrender.com` (or yours)

### Frontend (React/Vite/Vercel)

- [ ] **Code**
  - [ ] `frontend/package.json` has `"build": "tsc -b && vite build"`
  - [ ] `frontend/vite.config.ts` exists
  - [ ] `frontend/vercel.json` exists with correct config
  - [ ] `frontend/.env.production` has `VITE_API_URL`
  - [ ] `.gitignore` includes `.env.local`, `.vercel/`
  - [ ] API calls use `import.meta.env.VITE_API_URL`
  - [ ] No `fetch()` to hardcoded `http://localhost` in prod code

- [ ] **Vercel Setup**
  - [ ] Vercel account created (free tier OK)
  - [ ] GitHub repo connected to Vercel
  - [ ] Framework: Vite
  - [ ] Build command: `npm run build`
  - [ ] Output directory: `dist`
  - [ ] Root directory: `frontend`
  - [ ] Environment variable: `VITE_API_URL=https://cropai-api.onrender.com`
  - [ ] Deployment successful (status = ✅)
  - [ ] Frontend URL copied: `https://cropai-xxxx.vercel.app` (or yours)

### Integration

- [ ] **CORS**
  - [ ] Render env: `ALLOWED_ORIGINS=https://cropai-xxxx.vercel.app`
  - [ ] Test CORS headers with curl (see commands below)
  - [ ] Frontend API calls return 200, not 403

- [ ] **API Connectivity**
  - [ ] Frontend → Backend calls work end-to-end
  - [ ] `/api/predict` returns crop prediction + AI insight
  - [ ] `/health` endpoint returns `{"status": "ok"}`
  - [ ] Error responses are handled gracefully

---

## 🚀 DEPLOYMENT COMMANDS

### Step 1: Render Backend Deployment

```bash
# 1. Push code to GitHub
git add .
git commit -m "chore: production ready deployment"
git push origin main

# 2. Render auto-deploys from GitHub
# Go to https://render.com → create Web Service
# Select repo, set:
#   - Root Dir: app
#   - Build: pip install -r requirements.txt
#   - Start: gunicorn app:app
#   - Environment vars (see table below)

# 3. Wait for ✅ status, then test:
curl https://cropai-api.onrender.com/health
# Expected: {"status": "ok"}
```

### Step 2: Frontend Vercel Deployment

```bash
# 1. Update frontend env
echo 'VITE_API_URL=https://cropai-api.onrender.com' > frontend/.env.production

# 2. Commit & push
git add frontend/.env.production frontend/vercel.json
git commit -m "chore: Vercel production config"
git push origin main

# 3. Vercel auto-deploys from GitHub
# Go to https://vercel.com → import repo
# Settings:
#   - Root Dir: frontend
#   - Build: npm run build
#   - Output: dist
#   - Framework: Vite
#   - Env var: VITE_API_URL

# 4. Test frontend loads:
curl https://cropai-xxxx.vercel.app
# Expected: HTML response
```

### Step 3: Integration Test

```bash
# Test backend → Groq connectivity
curl https://cropai-api.onrender.com/api/chat \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"What crop for high N?"}'

# Test CORS (from frontend origin)
curl -H "Origin: https://cropai-xxxx.vercel.app" \
  https://cropai-api.onrender.com/api/predict \
  -v 2>&1 | grep -i "access-control-allow-origin"
# Expected: Access-Control-Allow-Origin: https://cropai-xxxx.vercel.app

# Test prediction (from browser console or curl with JSON)
curl https://cropai-api.onrender.com/api/predict \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "N": 50, "P": 30, "K": 40,
    "temperature": 25, "humidity": 60,
    "ph": 7, "rainfall": 800
  }' | jq .
```

---

## 📄 ENVIRONMENT VARIABLES TABLE

### Render Backend Environment

| Variable | Example Value | Source |
|----------|---------------|--------|
| `FLASK_ENV` | `production` | Hardcode in Render |
| `GROQ_API_KEY` | `gsk_xxxx...` | https://console.groq.com |
| `ALLOWED_ORIGINS` | `https://cropai-xxxx.vercel.app` | Your Vercel URL |
| `FLASK_SECRET_KEY` | (32-char random) | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `AGMARKNET_API_URL` | `https://agmarknet.gov.in/Api1.0/prices` | Official API (optional) |

### Vercel Frontend Environment

| Variable | Example Value | Source |
|----------|---------------|--------|
| `VITE_API_URL` | `https://cropai-api.onrender.com` | Your Render URL |

---

## 🔍 VALIDATION SCRIPT

Run before deployment:

```bash
python validate_deployment.py
```

This checks:
- ✅ Env vars are set
- ✅ Model file exists
- ✅ Groq API connection works
- ✅ CORS configuration is correct
- ✅ Local API responds (dev only)

---

## 🐛 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| **CORS Error (403)** | Update `ALLOWED_ORIGINS` in Render to match your Vercel domain exactly |
| **Groq 401** | Re-generate API key at https://console.groq.com, check credits |
| **Model Not Found (500)** | Ensure `crop_model_best.pkl` is committed: `git add app/ml_training/models/crop_model_best.pkl` |
| **Cold Start >10s** | Normal on free tier. Upgrade to paid or accept delay |
| **Frontend Build Fails** | Run `npm run build` locally, fix TypeScript/ESLint errors |
| **Health Endpoint 404** | Check backend deployed to Render successfully (check logs) |

---

## 📈 MONITORING POST-DEPLOYMENT

### Weekly Checks

```bash
# Backend health
curl -s https://cropai-api.onrender.com/health | jq .

# Frontend accessible
curl -s https://cropai-xxxx.vercel.app | head -c 200

# Groq API status
curl -s https://status.groq.com  # Check if any incidents
```

### Logs

- **Render Logs**: https://dashboard.render.com → cropai-api → Logs
- **Vercel Logs**: https://vercel.com → Deployments → select → Logs

### Metrics to Monitor

- **Render**: Cold start time, error rate, request count
- **Vercel**: Build time, page load, error budget

---

## 📄 ROLLBACK PROCEDURE

If deployment breaks:

```bash
# Option 1: Render Rollback
# Dashboard → cropai-api → Deployments → select previous ✅ → Rollback

# Option 2: Vercel Rollback
# Dashboard → Deployments → select previous ✅ → Redeploy

# Option 3: Git Rollback (if code issue)
git revert HEAD  # Revert last commit
git push origin main  # Render/Vercel auto-redeploy
```

---

## 🌟 NEXT PHASE: Database

Once frontend + backend are stable:

1. **Create Supabase/Neon PostgreSQL project**
2. **Add SQLAlchemy to Flask**:
   ```python
   from flask_sqlalchemy import SQLAlchemy
   db = SQLAlchemy(app)
   ```
3. **Add env var**: `DATABASE_URL=postgres://user:pass@host/db`
4. **Create models**: User, CropPrediction, UserSession
5. **Implement auth**: JWT + Session management

---

## 🏁 SUCCESS CRITERIA

✅ Deployment is successful when:

1. Frontend loads on Vercel without errors
2. API calls from frontend to Render succeed (200 status)
3. `/api/predict` returns crop prediction + AI insight
4. CORS headers are correct (no 403 errors)
5. Groq API responds within 5 seconds
6. Model predictions are accurate
7. Logs show no 5xx errors
8. Cold start <15s on free tier

---

**Created**: 2026-05-15  
**Last Updated**: 2026-05-15  
**Maintained By**: CropAI DevOps Team  
**Support**: See README.md for contact info
