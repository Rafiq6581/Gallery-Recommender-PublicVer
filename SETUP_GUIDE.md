# 🚀 Quick Setup Guide - Art Gallery Recommender Demo

## Prerequisites

1. **Python 3.11+** - Use pyenv for version management
2. **Poetry** - For dependency management
3. **Docker** (optional) - For local database services
4. **OpenAI API Key** - For LLM functionality

## Step-by-Step Setup

### 1. Install Dependencies

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the example (you'll need to create this file manually since .env.example is git-ignored)
touch .env

# Add the following to your .env file:
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_ID=gpt-4o-mini
DATABASE_HOST=localhost
DATABASE_NAME=gallery_demo
QDRANT_DATABASE_HOST=localhost
QDRANT_DATABASE_PORT=6333
DEMO_MODE=true
```

### 3. Start Local Services

#### Option A: Using Docker Compose
```bash
poetry run poe local-infrastructure-up
```

#### Option B: Manual Setup
```bash
# Start MongoDB
docker run -d --name mongodb -p 27017:27017 mongo:6.0

# Start Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant:latest
```

### 4. Run Demo Data Pipeline

```bash
# Generate and load demo data
poetry run python -m gallery_recommender.application.demo_data

# Run the ETL pipeline with demo data
poetry run poe run-demo-pipeline
```

### 5. Start the API Service

```bash
# Start the ML inference service
poetry run poe run-inference-ml-service
```

The API will be available at: `http://localhost:8000`

### 6. Test the System

```bash
# Test the recommendation endpoint
poetry run poe call-rag-retrieval-module

# Or test via curl:
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "level": "beginner",
      "duration": "2 hours", 
      "reason": "relaxation",
      "mood": "contemplative"
    },
    "filters": {"area": "DOWNTOWN"}
  }'
```

## Available Commands

```bash
# Development
poetry run poe run-inference-ml-service     # Start API server
poetry run poe run-data-service            # Start data service
poetry run poe local-infrastructure-up     # Start local services
poetry run poe local-infrastructure-down   # Stop local services

# Data Pipeline
poetry run poe run-demo-pipeline           # Run with demo data
poetry run poe run-feature-engineering-pipeline  # Feature engineering
poetry run poe run-digital-data-etl-demo   # ETL pipeline

# Testing
poetry run poe call-rag-retrieval-module   # Test RAG module
poetry run poe test                        # Run tests
```

## Monitoring & Observability

### ZenML Dashboard
```bash
# Access ZenML dashboard
poetry run zenml up
# Open: http://localhost:8080
```

### Opik Monitoring (Optional)
If you have Comet ML/Opik credentials:
```bash
export COMET_API_KEY=your_comet_key
export OPIK_PROJECT_NAME=art-gallery-demo
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're using Poetry's virtual environment
   ```bash
   poetry shell
   ```

2. **Database Connection**: Ensure MongoDB and Qdrant are running
   ```bash
   docker ps  # Check running containers
   ```

3. **API Key Issues**: Verify your OpenAI API key is correctly set
   ```bash
   echo $OPENAI_API_KEY
   ```

4. **Port Conflicts**: Check if ports 8000, 6333, 27017 are available
   ```bash
   lsof -i :8000
   ```

### Demo Limitations

This demo version:
- Uses simplified mock data instead of real gallery information
- Has generalized recommendation algorithms  
- Includes placeholder infrastructure configurations
- May have limited error handling for edge cases

For questions or issues, refer to the main README.md and DEMO_NOTICE.md files.
