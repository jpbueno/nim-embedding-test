#!/usr/bin/env python3
"""
NIM Embedding Test Workload
Generates random text data and calls the NeMo Retriever Text Embedding API
to test observability metrics and traces.
"""

import requests
import json
import time
import random
import logging
import os
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
NIM_ENDPOINT = os.getenv('NIM_ENDPOINT', 'http://nemo-embedder-nvidia-nim-llama-32-nv-embedqa-1b-v2.embedding-nim.svc.cluster.local:8000')
REQUEST_INTERVAL = int(os.getenv('REQUEST_INTERVAL', '10'))  # seconds
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '3'))
MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', '200'))

# Sample text templates for generating random content
TEXT_TEMPLATES = [
    "The quick brown fox jumps over the lazy dog in the forest during {time}.",
    "Machine learning models require large datasets and computational resources for training {topic}.",
    "Climate change affects weather patterns across different regions, causing {effect}.",
    "Modern software development practices include continuous integration and deployment in {domain}.",
    "Artificial intelligence applications are transforming industries like {industry} and healthcare.",
    "Database optimization techniques help improve query performance for {database_type} systems.",
    "Cloud computing platforms provide scalable infrastructure for {workload_type} applications.",
    "Natural language processing enables computers to understand and generate human {language_aspect}.",
    "Cybersecurity measures protect sensitive data from various types of {threat_type} attacks.",
    "Renewable energy sources like solar and wind power contribute to {environmental_benefit}.",
    "E-commerce platforms utilize recommendation systems to suggest relevant {product_category} to users.",
    "Scientific research in {field} requires collaboration between multiple institutions and experts.",
    "Mobile applications must be optimized for different screen sizes and {device_feature}.",
    "Financial markets are influenced by economic indicators and {market_factor}.",
    "Educational technology transforms traditional learning methods through {innovation}."
]

# Variables for text generation
TIMES = ["morning", "afternoon", "evening", "midnight", "dawn", "dusk"]
TOPICS = ["techniques", "algorithms", "methodologies", "frameworks", "approaches"]
EFFECTS = ["droughts", "floods", "temperature variations", "seasonal shifts", "extreme weather"]
DOMAINS = ["microservices", "containerization", "cloud environments", "distributed systems"]
INDUSTRIES = ["finance", "retail", "manufacturing", "transportation", "education"]
DATABASE_TYPES = ["relational", "NoSQL", "graph", "time-series", "columnar"]
WORKLOAD_TYPES = ["web", "mobile", "analytics", "streaming", "batch processing"]
LANGUAGE_ASPECTS = ["text", "speech", "communication", "dialogue", "content"]
THREAT_TYPES = ["malware", "phishing", "ransomware", "social engineering", "insider"]
ENVIRONMENTAL_BENEFITS = ["sustainability", "carbon reduction", "clean air", "energy independence"]
PRODUCT_CATEGORIES = ["books", "electronics", "clothing", "home goods", "software"]
FIELDS = ["biology", "physics", "chemistry", "psychology", "astronomy"]
DEVICE_FEATURES = ["performance", "battery life", "connectivity", "storage", "processing power"]
MARKET_FACTORS = ["geopolitical events", "inflation rates", "technological disruptions", "consumer behavior"]
INNOVATIONS = ["virtual reality", "interactive whiteboards", "online collaboration", "adaptive learning"]

def generate_random_text() -> str:
    """Generate random text using templates and variables."""
    template = random.choice(TEXT_TEMPLATES)
    
    # Replace placeholders with random values
    replacements = {
        'time': random.choice(TIMES),
        'topic': random.choice(TOPICS),
        'effect': random.choice(EFFECTS),
        'domain': random.choice(DOMAINS),
        'industry': random.choice(INDUSTRIES),
        'database_type': random.choice(DATABASE_TYPES),
        'workload_type': random.choice(WORKLOAD_TYPES),
        'language_aspect': random.choice(LANGUAGE_ASPECTS),
        'threat_type': random.choice(THREAT_TYPES),
        'environmental_benefit': random.choice(ENVIRONMENTAL_BENEFITS),
        'product_category': random.choice(PRODUCT_CATEGORIES),
        'field': random.choice(FIELDS),
        'device_feature': random.choice(DEVICE_FEATURES),
        'market_factor': random.choice(MARKET_FACTORS),
        'innovation': random.choice(INNOVATIONS)
    }
    
    # Apply replacements
    for key, value in replacements.items():
        template = template.replace(f'{{{key}}}', value)
    
    # Sometimes add extra random content
    if random.random() < 0.3:
        extra_sentences = [
            " This is particularly important for modern applications.",
            " Research shows significant improvements in efficiency.",
            " Industry experts recommend this approach for scalability.",
            " The implementation requires careful planning and execution.",
            " Users report positive experiences with this methodology."
        ]
        template += random.choice(extra_sentences)
    
    # Limit text length
    if len(template) > MAX_TEXT_LENGTH:
        template = template[:MAX_TEXT_LENGTH].rsplit(' ', 1)[0] + "."
    
    return template

def call_embedding_api(texts: List[str]) -> Dict[str, Any]:
    """Call the NIM embedding API with a list of texts."""
    url = f"{NIM_ENDPOINT}/v1/embeddings"
    
    payload = {
        "input": texts,
        "model": "NV-Embed-QA",
        "encoding_format": "float"
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            num_embeddings = len(result.get('data', []))
            embedding_dims = len(result['data'][0]['embedding']) if num_embeddings > 0 else 0
            
            logger.info(
                f"✅ Embedding request successful - "
                f"Texts: {len(texts)}, "
                f"Embeddings: {num_embeddings}, "
                f"Dimensions: {embedding_dims}, "
                f"Response time: {response_time:.2f}s"
            )
            
            return {
                'success': True,
                'response_time': response_time,
                'num_texts': len(texts),
                'num_embeddings': num_embeddings,
                'embedding_dims': embedding_dims,
                'status_code': response.status_code
            }
        else:
            logger.error(f"❌ API request failed - Status: {response.status_code}, Response: {response.text}")
            return {
                'success': False,
                'response_time': response_time,
                'status_code': response.status_code,
                'error': response.text
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main test loop."""
    logger.info(f"🚀 Starting NIM Embedding Test Workload")
    logger.info(f"NIM Endpoint: {NIM_ENDPOINT}")
    logger.info(f"Request Interval: {REQUEST_INTERVAL}s")
    logger.info(f"Batch Size: {BATCH_SIZE}")
    logger.info(f"Max Text Length: {MAX_TEXT_LENGTH}")
    
    # Test connectivity first
    try:
        health_url = f"{NIM_ENDPOINT}/v1/health/ready"
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            logger.info("✅ NIM service is ready")
        else:
            logger.warning(f"⚠️  NIM health check returned status: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Cannot reach NIM service: {str(e)}")
        logger.info("Continuing anyway - the service might still work...")
    
    request_count = 0
    successful_requests = 0
    
    try:
        while True:
            request_count += 1
            
            # Generate random texts
            texts = [generate_random_text() for _ in range(BATCH_SIZE)]
            
            logger.info(f"📝 Request #{request_count} - Generated {len(texts)} random texts:")
            for i, text in enumerate(texts, 1):
                logger.info(f"  {i}. {text}")
            
            # Call embedding API
            result = call_embedding_api(texts)
            
            if result.get('success'):
                successful_requests += 1
            
            success_rate = (successful_requests / request_count) * 100
            logger.info(f"📊 Stats - Total: {request_count}, Successful: {successful_requests}, Success Rate: {success_rate:.1f}%")
            
            # Wait before next request
            logger.info(f"⏰ Waiting {REQUEST_INTERVAL} seconds before next request...")
            time.sleep(REQUEST_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Test workload stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error in main loop: {str(e)}")
    finally:
        logger.info(f"📈 Final Stats - Total Requests: {request_count}, Successful: {successful_requests}")

if __name__ == "__main__":
    main()
