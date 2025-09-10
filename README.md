# NIM Embedding Test Workload

This workload generates random text data and makes requests to your NeMo Retriever Text Embedding NIM to test observability features.

## What it does

- Generates diverse random text using templates and variables
- Makes embedding requests every 15 seconds (configurable)
- Processes 3 texts per request (configurable)
- Logs detailed information for troubleshooting
- Tracks success rates and performance metrics

## Configuration

The workload can be configured via environment variables in the ConfigMap:

- `NIM_ENDPOINT`: The NIM service endpoint (auto-configured for your cluster)
- `REQUEST_INTERVAL`: Seconds between requests (default: 15)
- `BATCH_SIZE`: Number of texts per request (default: 3)  
- `MAX_TEXT_LENGTH`: Maximum length of generated text (default: 200)

## Deployment

```bash
kubectl apply -f deployment.yaml
```

## Monitoring

View logs:
```bash
kubectl logs -n nim-test-workload deployment/nim-embedding-test -f
```

Check status:
```bash
kubectl get pods -n nim-test-workload
```

## Observability Testing

This workload will generate traffic that should be visible in:
- OpenTelemetry Collector metrics and traces
- Prometheus metrics at the NIM endpoints
- Grafana dashboards
- Jaeger traces
- Zipkin traces

The embedding requests will create traces showing the full request lifecycle and metrics for:
- Request latency
- Success/error rates
- Throughput
- Resource utilization
