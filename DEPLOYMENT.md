# 🚀 Deployment Guide - Iris ML Classifier

This guide covers deployment to various platforms with step-by-step instructions.

## 1. Local Development

### Quick Start
```bash
# Clone/Download project
cd iris-ml-project

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate environment
source venv/bin/activate

# Run application
python app.py
```

Visit: **http://localhost:5000**

---

## 2. Docker Deployment (Local)

### Prerequisites
- Docker installed
- Docker Compose (optional)

### Option A: Using Docker directly
```bash
# Build image
docker build -t iris-ml .

# Run container
docker run -p 5000:5000 iris-ml
```

### Option B: Using Docker Compose
```bash
# Start application
docker-compose up

# View logs
docker-compose logs -f web

# Stop application
docker-compose down
```

Visit: **http://localhost:5000**

---

## 3. Heroku Deployment

### Prerequisites
- Heroku CLI installed
- GitHub account
- Free Heroku account

### Steps

1. **Create Procfile** (if not present)
```bash
cat > Procfile << EOF
web: gunicorn --bind 0.0.0.0:$PORT app:app
EOF
```

2. **Create runtime.txt**
```bash
cat > runtime.txt << EOF
python-3.9.16
EOF
```

3. **Create Heroku app**
```bash
heroku login
heroku create your-app-name
```

4. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

5. **View logs**
```bash
heroku logs --tail
```

Visit: **https://your-app-name.herokuapp.com**

---

## 4. AWS Deployment (EC2)

### Prerequisites
- AWS account
- EC2 instance (t2.micro)
- Security group configured for ports 80, 443, 5000

### Steps

1. **SSH into instance**
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

2. **Update system**
```bash
sudo yum update -y
sudo yum install python3 python3-pip git -y
```

3. **Clone project**
```bash
git clone your-repo-url
cd iris-ml-project
```

4. **Install dependencies**
```bash
pip3 install -r requirements.txt
```

5. **Run with Gunicorn**
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

6. **Setup systemd service**
```bash
sudo cat > /etc/systemd/system/iris-ml.service << EOF
[Unit]
Description=Iris ML Classifier
After=network.target

[Service]
Type=notify
User=ec2-user
WorkingDirectory=/home/ec2-user/iris-ml-project
Environment="PATH=/usr/local/bin"
ExecStart=/usr/local/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl start iris-ml
sudo systemctl enable iris-ml
```

Visit: **http://your-instance-ip:5000**

---

## 5. PythonAnywhere Deployment

### Steps

1. **Create PythonAnywhere account** (free tier available)
   - Sign up at https://www.pythonanywhere.com

2. **Upload files**
   - Upload app.py and templates folder to Files section

3. **Create Web App**
   - Go to Web tab
   - Add new web app → Flask → Python 3.9

4. **Configure WSGI file**
   - Edit WSGI configuration file:
   ```python
   import sys
   path = '/home/yourusername/mysite'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```

5. **Reload**
   - Click Reload button

Visit: **https://yourusername.pythonanywhere.com**

---

## 6. Google Cloud Platform (Cloud Run)

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Steps

1. **Authenticate**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Deploy**
```bash
gcloud run deploy iris-ml \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

3. **View service**
```bash
gcloud run services list
```

Visit: **Your Cloud Run URL** (provided after deployment)

---

## 7. Azure Deployment

### Prerequisites
- Azure account
- Azure CLI installed

### Steps

1. **Create resource group**
```bash
az group create --name iris-ml --location eastus
```

2. **Create App Service Plan**
```bash
az appservice plan create \
  --name iris-ml-plan \
  --resource-group iris-ml \
  --sku B1 --is-linux
```

3. **Create Web App**
```bash
az webapp create \
  --resource-group iris-ml \
  --plan iris-ml-plan \
  --name iris-ml-app \
  --runtime "PYTHON|3.9"
```

4. **Deploy**
```bash
az webapp deployment source config-zip \
  --resource-group iris-ml \
  --name iris-ml-app \
  --src deployment.zip
```

Visit: **https://iris-ml-app.azurewebsites.net**

---

## 8. DigitalOcean App Platform

### Prerequisites
- DigitalOcean account
- Project connected to GitHub

### Steps

1. **Connect GitHub repo**
   - Link your repository in DigitalOcean

2. **Create app.yaml**
```yaml
name: iris-ml
services:
  - name: web
    github:
      repo: your-username/iris-ml-project
      branch: main
    build_command: pip install -r requirements.txt
    run_command: gunicorn --bind 0.0.0.0:$PORT app:app
    http_port: 5000
```

3. **Deploy**
   - Push to GitHub
   - DigitalOcean automatically deploys

Visit: **Your DigitalOcean App URL**

---

## 9. Production Configuration Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Set `SECURE_SSL_REDIRECT = True`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Set up logging
- [ ] Configure CORS properly
- [ ] Use HTTPS/SSL certificate
- [ ] Set up monitoring and alerts
- [ ] Configure database backups (if applicable)

---

## 10. Monitoring & Maintenance

### Health Check
```bash
curl https://your-app-url/api/model-info
```

### View Logs
- **Heroku**: `heroku logs --tail`
- **AWS**: Check CloudWatch
- **GCP**: Cloud Logging dashboard
- **Azure**: App Service logs

### Update Dependencies
```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

---

## 11. Domain Configuration

### Using Custom Domain

1. **Get domain** (Namecheap, GoDaddy, etc.)

2. **Point to app**
   - Update DNS records to point to your app's IP/URL

3. **SSL Certificate**
   - Most platforms offer free SSL with Let's Encrypt
   - Configure in platform settings

---

## 12. Cost Estimation

| Platform | Free Tier | Paid | Notes |
|----------|-----------|------|-------|
| Heroku | $7/month | $50+/month | Dyno hours limited |
| AWS | 1 year free | $5-20/month | t2.micro eligible |
| GCP | $300 credit | $0.00002/request | Pay-as-you-go |
| Azure | $200 credit | $50-100/month | App Service Plan |
| DigitalOcean | None | $6+/month | Droplets or Apps |
| PythonAnywhere | Free tier available | $5-40/month | Web apps |

---

## Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :5000
# Kill process
kill -9 PID
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Connection Refused
- Check firewall settings
- Verify port is exposed
- Check security group/network rules

### Out of Memory
- Increase instance size
- Reduce model complexity
- Implement caching

---

## Support & Resources

- **Flask Documentation**: https://flask.palletsprojects.com
- **Scikit-learn Docs**: https://scikit-learn.org
- **Docker Docs**: https://docs.docker.com
- **Platform-specific docs**: See links above

---

**Happy deploying! 🚀🌸**
