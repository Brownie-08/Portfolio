# 🔧 Railway Deployment Troubleshooting

## 🚨 **Common Build Errors and Fixes**

### **Issue: "plp: command not found" Error**
**Error Message**: `/bin/bash: line 1: plp: command not found`

**Root Cause**: Typo in build configuration where `plp` is used instead of `pip`

**✅ Resolution Applied:**
1. ✅ Updated `nixpacks.toml` with explicit `python -m pip` commands
2. ✅ Enhanced `railway.json` with explicit build commands
3. ✅ Added `runtime.txt` to specify Python version
4. ✅ Created backup build script (`build.sh`)

---

## 🔧 **Updated Configuration Files**

### **nixpacks.toml** (Primary Build Config)
```toml
[phases.setup]
nixPkgs = ["python311", "pkg-config", "mysql80"]

[phases.install]
cmds = [
  "python -m pip install --upgrade pip",
  "python -m pip install -r requirements.txt"
]

[phases.build]
cmds = ["python manage.py collectstatic --noinput"]

[start]
cmd = "python manage.py migrate && gunicorn portfolio_project.wsgi --bind 0.0.0.0:$PORT"
```

### **railway.json** (Railway Platform Config)
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "python -m pip install --upgrade pip && python -m pip install -r requirements.txt && python manage.py collectstatic --noinput"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn portfolio_project.wsgi --bind 0.0.0.0:$PORT"
  }
}
```

### **runtime.txt** (Python Version)
```
python-3.11
```

---

## 🚀 **Deployment Process**

### **Automatic Build Steps (Railway):**
1. **Setup Phase**: Install Python 3.11, pkg-config, MySQL client
2. **Install Phase**: Upgrade pip, install requirements
3. **Build Phase**: Collect static files
4. **Deploy Phase**: Run migrations, start gunicorn

### **Expected Build Log Output:**
```
✅ Setting up Python 3.11
✅ Upgrading pip
✅ Installing requirements from requirements.txt
✅ Collecting static files
✅ Running database migrations
✅ Starting gunicorn server
```

---

## 🛠️ **If Build Still Fails**

### **Option 1: Clear Railway Cache**
1. Go to Railway project settings
2. Click **"Reset Build Cache"**
3. Trigger new deployment

### **Option 2: Manual Environment Override**
In Railway Variables, add:
```env
NIXPACKS_PYTHON_VERSION=3.11
NIXPACKS_BUILD_CMD=python -m pip install --upgrade pip && python -m pip install -r requirements.txt
```

### **Option 3: Use Dockerfile (Fallback)**
If Nixpacks continues to fail, we can create a Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

CMD python manage.py migrate && gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:$PORT
```

---

## ✅ **Verification Checklist**

After deployment, verify:
- [ ] Build completes without "plp" error
- [ ] All Python packages install correctly
- [ ] Static files are collected
- [ ] Database migrations run successfully
- [ ] Application starts on Railway URL
- [ ] Contact form works with email notifications

---

## 🔍 **Debug Commands**

### **Check Requirements File:**
```bash
cat requirements.txt
```

### **Verify Python/Pip:**
```bash
python --version
python -m pip --version
```

### **Test Local Installation:**
```bash
python -m pip install -r requirements.txt
python manage.py check --deploy
```

---

## 📞 **Railway Support**

### **If Issues Persist:**
1. **Railway Discord**: https://discord.gg/railway
2. **Railway Docs**: https://docs.railway.app/troubleshoot
3. **Django on Railway**: https://docs.railway.app/guides/django

### **Log Analysis:**
- Check "Build Logs" for installation errors
- Check "Deploy Logs" for runtime errors
- Monitor "Application Logs" for Django errors

---

## 🎯 **Success Indicators**

### **Build Success:**
- ✅ No "command not found" errors
- ✅ All requirements installed
- ✅ Static files collected
- ✅ No Python/Django errors

### **Deploy Success:**
- ✅ Migrations completed
- ✅ Server starts on Railway URL
- ✅ All pages load correctly
- ✅ Database connections work
- ✅ Email system functional

---

**🚂 Your Railway deployment should now proceed without the "plp" error! 🎉**
