# Deployment Guide

Complete guide for deploying the BI Dashboard Backend API to various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [Production Checklist](#production-checklist)

---

## Local Development

### Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run server
python main.py
```

The API will be available at `http://localhost:8000`

### Auto-reload Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Docker Deployment

### Prerequisites

- Docker installed
- Docker Compose (optional, for multi-container setup)

### Build Docker Image

```bash
docker build -t bi-dashboard-backend:latest .
```

### Run with SQLite

```bash
docker run -it \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_api_key \
  -e DATABASE_TYPE=sqlite \
  -e DATABASE_URL=sqlite:///./bi_dashboard.db \
  -v $(pwd)/data:/app/data \
  bi-dashboard-backend:latest
```

### Run with Docker Compose (PostgreSQL)

```bash
# Set environment variables
export GEMINI_API_KEY=your_api_key

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Docker Compose with existing database

```bash
# Modify docker-compose.yml to point to existing database
# Update DATABASE_URL in environment

docker-compose up -d
```

### Production Docker Run

```bash
docker run -d \
  --name bi-dashboard \
  --restart unless-stopped \
  -p 80:8000 \
  -e GEMINI_API_KEY=${GEMINI_API_KEY} \
  -e DEBUG=False \
  -e DATABASE_TYPE=postgresql \
  -e DATABASE_URL=postgresql://user:pass@postgres.example.com:5432/bi_dashboard \
  bi-dashboard-backend:latest
```

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster
- kubectl installed
- Docker image pushed to registry

### Create Configmap for Configuration

```yaml
# k8s-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: bi-dashboard-config
data:
  DEBUG: "false"
  DATABASE_TYPE: postgresql
  HOST: 0.0.0.0
  PORT: "8000"
```

### Create Secret for API Key

```bash
kubectl create secret generic bi-dashboard-secrets \
  --from-literal=GEMINI_API_KEY=your_api_key
```

### Create Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bi-dashboard-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bi-dashboard-backend
  template:
    metadata:
      labels:
        app: bi-dashboard-backend
    spec:
      containers:
      - name: backend
        image: your-registry/bi-dashboard-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: bi-dashboard-config
        - secretRef:
            name: bi-dashboard-secrets
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: bi-dashboard-db
              key: url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

### Create Service

```yaml
# k8s-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: bi-dashboard-backend
spec:
  selector:
    app: bi-dashboard-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Deploy

```bash
kubectl apply -f k8s-configmap.yaml
kubectl create secret generic bi-dashboard-db --from-literal=url=postgresql://...
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

# Check deployment
kubectl get deployments
kubectl get pods
kubectl get services
```

---

## Cloud Platforms

### AWS (Elastic Beanstalk)

1. **Install EB CLI**

```bash
pip install awsebcli
```

2. **Initialize EB Application**

```bash
eb init -p python-3.11 bi-dashboard-backend
```

3. **Create Environment**

```bash
eb create bi-dashboard-prod
```

4. **Set Environment Variables**

```bash
eb setenv GEMINI_API_KEY=your_api_key
eb setenv DATABASE_TYPE=postgresql
eb setenv DATABASE_URL=postgresql://...
```

5. **Deploy**

```bash
eb deploy
```

6. **Monitor**

```bash
eb open  # Opens app in browser
eb logs  # View logs
```

### Google Cloud Platform (Cloud Run)

1. **Build and Push Image**

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/bi-dashboard-backend
```

2. **Deploy to Cloud Run**

```bash
gcloud run deploy bi-dashboard-backend \
  --image gcr.io/PROJECT_ID/bi-dashboard-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_api_key,DATABASE_TYPE=postgresql \
  --memory 512Mi \
  --cpu 1
```

### Heroku

1. **Create Procfile**

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Create runtime.txt**

```
python-3.11.4
```

3. **Create app**

```bash
heroku create bi-dashboard-backend
```

4. **Set config variables**

```bash
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set DATABASE_TYPE=postgresql
heroku config:set DATABASE_URL=postgresql://...
```

5. **Deploy**

```bash
git push heroku main
```

6. **View logs**

```bash
heroku logs --tail
```

### PythonAnywhere

1. Go to pythonanywhere.com
2. Create account
3. Upload code
4. Configure WSGI file
5. Set environment variables in web app settings
6. Reload app

---

## Production Checklist

### Security

- [ ] DEBUG mode disabled (`DEBUG=False`)
- [ ] HTTPS/SSL certificate configured
- [ ] CORS origins restricted to specific domains
- [ ] API key authentication implemented
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] SQL injection prevention verified
- [ ] Secret keys stored in environment variables
- [ ] Database credentials not in code
- [ ] Regular security updates

### Performance

- [ ] Database indexes created
- [ ] Connection pooling configured
- [ ] Caching strategy implemented
- [ ] Load balancer configured
- [ ] CDN for static content
- [ ] Database backup strategy
- [ ] Monitoring and logging configured
- [ ] Response times under 5 seconds
- [ ] Error handling and recovery

### Infrastructure

- [ ] PostgreSQL database setup
- [ ] Database backups automated (daily)
- [ ] Log aggregation configured
- [ ] Metrics/monitoring enabled
- [ ] Uptime monitoring set up
- [ ] Disaster recovery plan
- [ ] Auto-scaling configured
- [ ] Health checks implemented

### DevOps

- [ ] CI/CD pipeline configured
- [ ] Automated testing enabled
- [ ] Code quality checks enabled
- [ ] Version control configured
- [ ] Container registry setup
- [ ] Deployment process documented
- [ ] Rollback procedure tested
- [ ] Zero-downtime deployments supported

### Data

- [ ] Sample data removed from production
- [ ] Data validation rules enforced
- [ ] GDPR/privacy compliance verified
- [ ] Data retention policy established
- [ ] Audit logging enabled
- [ ] Regular data quality checks

---

## Monitoring & Maintenance

### Health Monitoring

```bash
# Check health endpoint regularly
curl http://your-api.com/health

# Set up monitoring (optional)
# Datadog, New Relic, CloudWatch, etc.
```

### Logs Management

```bash
# View logs
docker-compose logs backend

# or with Kubernetes
kubectl logs deployment/bi-dashboard-backend

# Aggregate logs with ELK stack, Datadog, etc.
```

### Database Maintenance

```bash
# Backup database
python manage.py backup

# Verify integrity
python manage.py check

# Optimize tables
python manage.py optimize
```

### Performance Tuning

1. Monitor response times
2. Optimize slow queries
3. Add database indexes
4. Implement caching
5. Scale horizontally if needed

---

## Troubleshooting Deployments

### Container won't start

```bash
# Check logs
docker logs container_id

# Test locally first
docker run -it bi-dashboard-backend:latest

# Verify all environment variables
```

### API returns 500 errors

```bash
# Check logs
# Verify API key is set
# Test database connection
python manage.py test

# Verify schema
python manage.py schema
```

### Slow performance

```bash
# Check CPU/memory usage
docker stats

# Monitor query performance
# Add database indexes
# Increase cache size

# Kubernetes:
kubectl top pods
kubectl logs deployment/bi-dashboard-backend
```

### Database connection issues

```bash
# Test connection
python manage.py test

# Check credentials
echo $DATABASE_URL

# Verify database is running
ping database.example.com

# Check firewall rules
```

---

## Scaling

### Horizontal Scaling

```bash
# Docker Compose - run multiple instances
docker-compose up --scale backend=3

# Kubernetes - scale replicas
kubectl scale deployment bi-dashboard-backend --replicas=5
```

### Vertical Scaling

```bash
# Increase resource limits in Docker/Kubernetes
# Docker: Add --memory and --cpus flags
# Kubernetes: Update resources in deployment spec
```

### Database Scaling

```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_sales_region ON sales(region);
CREATE INDEX idx_sales_date ON sales(date);

-- Archive old data
ARCHIVE TABLE sales WHERE date < '2024-01-01';

-- Partitioning (PostgreSQL)
PARTITION BY RANGE (date);
```

---

## Migration Strategies

### Blue-Green Deployment

1. Deploy new version to separate infrastructure
2. Test thoroughly
3. Switch traffic to new version
4. Keep old version as rollback

### Canary Deployment

1. Deploy to small percentage of users
2. Monitor metrics
3. Gradually increase traffic
4. Full rollout if successful

### Rolling Deployment

1. Stop a few instances
2. Deploy new version
3. Start instances
4. Repeat for all instances

---

## Rollback Procedures

```bash
# Docker
docker ps -a
docker run -d image_tag:old_version

# Kubernetes
kubectl rollout history deployment/bi-dashboard-backend
kubectl rollout undo deployment/bi-dashboard-backend

# Heroku
heroku releases
heroku rollback v42

# Elastic Beanstalk
eb abort
```

---

**For more information** refer to individual platform documentation or contact DevOps team.
