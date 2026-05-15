# ⚡ DEPLOYMENT QUICK START (5 MINS)

**For**: CropAI Vercel + Render deployment  
**Time**: ~5 minutes of active work + ~15 mins deploy time

---

## 1️⃣ BACKEND DEPLOYMENT (Render) — ~10 mins

```bash
# 1. Push code (all files auto-committed)
git push origin main

# 2. Go to https://render.com
# - Click: New → Web Service
# - GitHub: Select your repo
# - Root Directory: app
# - Build: pip install -r requirements.txt
# - Start: gunicorn app:app
# - Add Environment Variables (see below)

# 3. Click Deploy & wait ~5 mins
# Copy URL: https://cropai-api.onrender.com (yours will differ)
```

**Environment Variables (Render Dashboard)**:
```
FLASK_ENV=production
GROQ_API_KEY=<get from https://console.groq.com>
ALLOWED_ORIGINS=<leave blank for now, update after Vercel deploy>
FLASK_SECRET_KEY=<run: python -c "import secrets; print(secrets.token_hex(32))">
```

**Test**:
```bash
curl https://cropai-api.onrender.com/health
```

---

## 2️⃣ FRONTEND DEPLOYMENT (Vercel) — ~5 mins

```bash
# 1. Update env (use Render URL from step 1)
echo 'VITE_API_URL=https://cropai-api.onrender.com' > frontend/.env.production

# 2. Commit
git add frontend/.env.production
git commit -m "chore: Vercel config"
git push origin main

# 3. Go to https://vercel.com
# - Click: New → Import Git Repository
# - Select your repo
# - Root Directory: frontend
# - Framework: Vite
# - Click Deploy & wait ~2 mins

# Copy URL: https://cropai-xxxx.vercel.app
```

---

## 3️⃣ FINALIZE CORS (2 mins)

```bash
# 1. Go back to Render → cropai-api → Settings → Environment
# 2. Update: ALLOWED_ORIGINS=https://cropai-xxxx.vercel.app
# 3. Save (auto-redeploys in ~30 secs)
```

---

## 4️⃣ TEST (2 mins)

```bash
# Open browser console on https://cropai-xxxx.vercel.app and run:

fetch('https://cropai-api.onrender.com/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    N: 50, P: 30, K: 40,
    temperature: 25, humidity: 60, ph: 7, rainfall: 800
  })
})
  .then(r => r.json())
  .then(d => console.log('✅', d))
  .catch(e => console.error('❌', e))

# Expected: {"prediction": "Rice", "confidence": 0.92, ...}
```

---

## ✅ DONE! 

Your app is live at: `https://cropai-xxxx.vercel.app`

---

## 🆘 IF SOMETHING BREAKS

| Issue | Fix |
|-------|-----|
| **CORS Error** | Update `ALLOWED_ORIGINS` in Render to your Vercel URL |
| **Groq 401** | Check API key at https://console.groq.com |
| **Build Fails** | Run `cd frontend && npm run build` locally, fix errors |
| **Cold Start Slow** | Normal on free tier (up to 30 secs) |

---

## 📖 FULL DOCS

- **Detailed Guide**: `DEPLOYMENT.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **Validation**: `python validate_deployment.py`

---

**Next**: Add database (Supabase) for user auth + crop history  
**Support**: Check GitHub Issues or DEPLOYMENT.md troubleshooting
