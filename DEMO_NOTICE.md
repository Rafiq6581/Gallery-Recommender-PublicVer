# 🚨 DEMO VERSION NOTICE

## Important Information

This repository contains a **demonstration version** of a production AI/ML system. It has been specifically prepared for public sharing and educational purposes.

### What's Different in This Version

#### ✅ **What's Included:**
- **Complete technical architecture** showcasing modern ML/AI patterns
- **RAG (Retrieval-Augmented Generation)** implementation with vector search
- **ML Ops pipeline** using ZenML for ETL and feature engineering
- **FastAPI microservices** with async processing capabilities
- **Monitoring integration** with Opik and Comet ML
- **Clean code structure** following domain-driven design principles

#### ⚠️ **What's Been Modified:**
- **Business logic simplified** - Production algorithms and proprietary recommendations logic abstracted
- **Infrastructure sanitized** - Real GCP project IDs, URLs, and production configurations replaced with placeholders
- **Data sources anonymized** - Production data connections replaced with demo/mock data
- **API keys removed** - All production credentials and sensitive configurations abstracted
- **Branding neutralized** - Product-specific names and business details generalized

#### 🎯 **Intended Use:**
- **Learning and education** - Understanding modern ML system architecture
- **Technical evaluation** - Assessing code quality, patterns, and technical approaches
- **Portfolio demonstration** - Showcasing technical capabilities and system design skills
- **Reference implementation** - Examples of ML Ops, RAG, and microservices patterns

### Getting Started with Demo Mode

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Set up demo environment:**
   ```bash
   # Copy environment template (you'll need to create this file)
   cp .env.example .env
   # Add your OpenAI API key for LLM functionality
   ```

3. **Run with demo data:**
   ```bash
   poetry run poe run-demo-pipeline
   ```

### Production Differences

The actual production system includes:
- Sophisticated proprietary recommendation algorithms
- Real-time data ingestion from multiple sources
- Production-grade security and authentication
- Custom business logic and user experience optimizations
- Integrated mobile applications and full-stack implementations
- Advanced monitoring, scaling, and reliability features

### Disclaimer

This demonstration version is provided for educational and evaluation purposes only. It does not represent the complete functionality, performance, or capabilities of the production system it's based on.

---

**For questions about the production system or commercial applications, please contact the maintainer.**
