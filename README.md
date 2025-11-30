# Weather Forecasting API

A microservices-based weather forecasting system built with FastAPI, containerized with Docker, and deployed on Kubernetes using Helm charts.

## 📋 Overview

This project implements a weather forecasting pipeline consisting of four independent microservices that work together to ingest, process, predict, and notify about weather conditions.

## 🏗️ Architecture

The system is composed of four microservices:

### 1. **Ingestion Service** (Port: 8000)
- Fetches real-time weather data from Open-Meteo API
- Endpoint: `GET /ingest`
- Returns current weather conditions including temperature, wind speed, and humidity

### 2. **Data Processing Service** (Port: 8001)
- Processes and transforms raw weather data
- Endpoint: `POST /process`
- Converts units (e.g., wind speed from m/s to km/h)
- Validates and structures data for downstream services

### 3. **Prediction Service** (Port: 8000)
- Generates weather forecasts based on processed data
- Endpoint: `POST /predict`
- Simple rule-based prediction logic:
  - Temperature > 30°C → Sunny
  - Humidity > 70% → Rainy
  - Otherwise → Cloudy

### 4. **Notification Service** (Port: 8000)
- Sends notifications about weather predictions
- Endpoint: `POST /notify`
- Accepts custom messages for weather alerts

## 📁 Project Structure

```
forecasting-api/
├── backend/
│   ├── ingestion/           # Weather data ingestion service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       └── app.py
│   ├── data-processing/     # Data transformation service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       └── app.py
│   ├── prediction/          # Weather prediction service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       └── app.py
│   └── notification/        # Notification service
│       ├── Dockerfile
│       ├── requirements.txt
│       └── src/
│           └── app.py
└── deployments/
    ├── ingestion-chart/     # Helm chart for ingestion service
    ├── dataprocessing-chart/# Helm chart for data-processing service
    ├── prediction-chart/    # Helm chart for prediction service
    └── notification-chart/  # Helm chart for notification service
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker
- Kubernetes cluster (for deployment)
- Helm 3.x
- Azure Container Registry access (or configure your own registry)

### Local Development

#### Running Individual Services

Each service can be run locally for development:

**1. Ingestion Service:**
```bash
cd backend/ingestion
pip install -r requirements.txt
python src/app.py
```

**2. Data Processing Service:**
```bash
cd backend/data-processing
pip install -r requirements.txt
python src/app.py
```

**3. Prediction Service:**
```bash
cd backend/prediction
pip install -r requirements.txt
python src/app.py
```

**4. Notification Service:**
```bash
cd backend/notification
pip install -r requirements.txt
python src/app.py
```

### Docker Deployment

#### Build Docker Images

```bash
# Ingestion Service
cd backend/ingestion
docker build -t forecasting-ingestion:latest .

# Data Processing Service
cd ../data-processing
docker build -t forecasting-processing:latest .

# Prediction Service
cd ../prediction
docker build -t forecasting-prediction:latest .

# Notification Service
cd ../notification
docker build -t forecasting-notification:latest .
```

#### Run with Docker

```bash
# Ingestion Service
docker run -p 8000:8000 forecasting-ingestion:latest

# Data Processing Service
docker run -p 8001:8000 forecasting-processing:latest

# Prediction Service
docker run -p 8002:8000 forecasting-prediction:latest

# Notification Service
docker run -p 8003:8000 forecasting-notification:latest
```

### Kubernetes Deployment

#### Prerequisites

1. Configure your container registry credentials:
```bash
kubectl create secret docker-registry docker-registry-credentials \
  --docker-server=<your-registry-server> \
  --docker-username=<your-username> \
  --docker-password=<your-password> \
  --namespace=backend
```

2. Create the backend namespace:
```bash
kubectl create namespace backend
```

#### Deploy with Helm

```bash
# Ingestion Service
helm install ingestion ./deployments/ingestion-chart -n backend

# Data Processing Service
helm install dataprocessing ./deployments/dataprocessing-chart -n backend

# Prediction Service
helm install prediction ./deployments/prediction-chart -n backend

# Notification Service
helm install notification ./deployments/notification-chart -n backend
```

#### Verify Deployment

```bash
kubectl get pods -n backend
kubectl get services -n backend
```

## 🔌 API Documentation

Once services are running, access the interactive API documentation:

- Ingestion: `http://localhost:8000/docs`
- Data Processing: `http://localhost:8001/docs`
- Prediction: `http://localhost:8002/docs`
- Notification: `http://localhost:8003/docs`

### Sample API Calls

**Ingest Weather Data:**
```bash
curl -X GET http://localhost:8000/ingest
```

**Process Weather Data:**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25.5,
    "wind_speed": 5.2,
    "humidity": 65
  }'
```

**Get Weather Prediction:**
```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 32.0,
    "wind_speed": 10.5,
    "humidity": 45
  }'
```

**Send Notification:**
```bash
curl -X POST http://localhost:8003/notify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Weather alert: High temperature expected"
  }'
```

## 🛠️ Technology Stack

- **Framework:** FastAPI
- **Language:** Python 3.10
- **Server:** Uvicorn
- **Containerization:** Docker
- **Orchestration:** Kubernetes
- **Package Management:** Helm
- **Container Registry:** Azure Container Registry
- **External API:** Open-Meteo Weather API

## 📦 Dependencies

Each service uses the following Python packages:
- `fastapi` - Modern web framework for building APIs
- `uvicorn` - ASGI server implementation
- `pydantic` - Data validation using Python type hints
- `requests` - HTTP library for API calls

## ⚙️ Configuration

### Helm Chart Configuration

Each service has its own Helm chart with configurable values:

```yaml
image:
  repository: githubrunnertestregistry.azurecr.io/forecasting
  tag: "v1"
  pullPolicy: IfNotPresent

namespace: backend
replicaCount: 2

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: "500m"
    memory: "512Mi"
  requests:
    cpu: "250m"
    memory: "256Mi"
```

To customize, modify the `values.yaml` file in each chart or override values during installation:

```bash
helm install ingestion ./deployments/ingestion-chart \
  --set replicaCount=3 \
  --set image.tag=v2 \
  -n backend
```

## 🔄 Workflow

1. **Ingestion** → Fetch weather data from external API
2. **Processing** → Transform and validate the data
3. **Prediction** → Generate weather forecasts
4. **Notification** → Send alerts based on predictions

## 🧪 Testing

Test the complete workflow:

```bash
# 1. Ingest data
DATA=$(curl -s http://localhost:8000/ingest)

# 2. Process data (extract values and send to processing)
PROCESSED=$(curl -s -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25, "wind_speed": 5, "humidity": 65}')

# 3. Get prediction
PREDICTION=$(curl -s -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25, "wind_speed": 5, "humidity": 65}')

# 4. Send notification
curl -X POST http://localhost:8003/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Weather forecast ready"}'
```

## 📈 Scaling

Scale individual services based on load:

```bash
# Scale ingestion service to 5 replicas
helm upgrade ingestion ./deployments/ingestion-chart \
  --set replicaCount=5 \
  -n backend

# Or use kubectl
kubectl scale deployment ingestion --replicas=5 -n backend
```

## 🔐 Security Considerations

- API endpoints are currently open; consider adding authentication
- Use HTTPS in production environments
- Rotate container registry credentials regularly
- Implement rate limiting for public endpoints
- Add API key validation for external API calls

## 🚧 Future Enhancements

- [ ] Add machine learning models for better predictions
- [ ] Implement authentication and authorization
- [ ] Add database for historical data storage
- [ ] Create inter-service communication using message queues
- [ ] Implement monitoring and logging (Prometheus, Grafana)
- [ ] Add CI/CD pipeline for automated deployments
- [ ] Implement caching for API responses
- [ ] Add comprehensive unit and integration tests
- [ ] Support multiple location forecasts
- [ ] Add WebSocket support for real-time updates

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue in the repository.