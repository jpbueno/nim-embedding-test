# NIM Embedding Observability Test - Summary

## ✅ Test Workload Successfully Deployed!

Your NIM Embedding test workload is now running and generating traffic to test observability features.

### Current Status
- **Deployment**: `nim-embedding-test` in namespace `nim-test-workload` 
- **Status**: ✅ Running successfully with 100% success rate
- **Request Pattern**: Making embedding requests every 15 seconds with batches of 3 texts
- **Model**: `nvidia/llama-3.2-nv-embedqa-1b-v2`
- **Embedding Dimensions**: 2048

### What's Being Generated
The test workload is:
1. **Generating diverse random text** using templates covering various domains (ML, climate, tech, etc.)
2. **Making embedding API calls** to your NIM service with proper `input_type` parameter for asymmetric models
3. **Producing metrics and traces** that flow through your observability stack
4. **Logging detailed information** for monitoring and debugging

### Observability Data Being Captured

#### 📊 Metrics Available
- **NIM Service Metrics** (port 8000): `/v1/metrics`
  - Request counts, response times, success rates
  - Python runtime metrics, memory usage
- **Triton Inference Metrics** (port 8002): `/metrics`
  - Inference request success/failure counts
  - Model execution metrics
  - Backend performance metrics

#### 🔍 Traces Generated
- Full request lifecycle from API call to model inference
- Cross-service communication traces
- Performance bottleneck identification

#### 📈 Where to Monitor
Based on your observability stack, you can view the data in:
- **Prometheus**: `http://your-prometheus:9090` (metrics queries)
- **Grafana**: `http://your-grafana` (dashboards and visualizations)  
- **Jaeger**: `http://your-jaeger:16686` (distributed traces)
- **Zipkin**: `http://your-zipkin:9411` (trace visualization)

### Commands for Monitoring

```bash
# View logs
kubectl logs -n nim-test-workload deployment/nim-embedding-test -f

# Check deployment status
kubectl get pods -n nim-test-workload

# View recent successful requests
kubectl logs -n nim-test-workload deployment/nim-embedding-test --tail=50 | grep "✅"

# Check metrics directly
kubectl run temp-curl --rm -i --tty --image=curlimages/curl --restart=Never -- \
  curl -s http://nemo-embedder-nvidia-nim-llama-32-nv-embedqa-1b-v2.embedding-nim.svc.cluster.local:8000/v1/metrics

# Check Triton metrics
kubectl run temp-curl --rm -i --tty --image=curlimages/curl --restart=Never -- \
  curl -s http://nemo-embedder-triton-metrics.embedding-nim.svc.cluster.local:8002/metrics
```

### Configuration
You can modify the workload behavior by updating the ConfigMap:

```bash
# Increase request frequency (reduce interval to 5 seconds)
kubectl patch configmap -n nim-test-workload nim-embedding-test-config \
  --patch '{"data":{"REQUEST_INTERVAL":"5"}}'

# Increase batch size (more texts per request)
kubectl patch configmap -n nim-test-workload nim-embedding-test-config \
  --patch '{"data":{"BATCH_SIZE":"5"}}'

# Restart deployment to pick up changes
kubectl rollout restart deployment -n nim-test-workload nim-embedding-test
```

### Cleanup
When you're done testing observability:

```bash
kubectl delete namespace nim-test-workload
```

## Next Steps for Observability Testing

1. **Check Prometheus** - Query for `nv_inference_request_success` and other NIM metrics
2. **Create Grafana Dashboards** - Visualize embedding request rates, latencies, and success rates  
3. **Explore Jaeger Traces** - Look for traces from the embedding service showing full request flows
4. **Set up Alerts** - Configure alerts for high error rates or slow response times
5. **Load Testing** - Scale up the deployment replicas to generate more load if needed

The workload will continue running and generating realistic embedding traffic to help you validate and tune your observability setup!

Here’s a clean **Markdown** version ready for a README file:

````markdown
# Viewing Test Data in Grafana

Follow the steps below to access and explore your test data in Grafana.

---

## 1) Access Grafana

- **If you have NodePort exposed:**
  - URL: `http://<any-cluster-node-ip>:32222`

- **Or via the kube-prom stack service port-forward:**
  ```bash
  kubectl -n monitoring port-forward svc/kube-prometheus-stack-1741309824-grafana 3000:80
````

Then open [http://localhost:3000](http://localhost:3000)

---

## 2) Add Prometheus as a Data Source (if not already configured)

* In Grafana:
  `Settings (gear)` → `Data sources` → `Add data source` → `Prometheus`
* URL:
  `http://prometheus-operated.monitoring.svc.cluster.local:9090`
* Click **Save & test**

---

## 3) Import the Ready-Made Dashboard

* In Grafana:
  `Dashboards` → `New` → `Import`
* Upload:
  `grafana-dashboards/nim_embedding_observability.json`
  *(from this machine)* or paste its JSON content.
* Select your **Prometheus data source** when prompted.

---

## 4) Explore Useful Prometheus Queries in Grafana’s Explore Tab

* Triton requests success over time:

  ```promql
  sum by (model) (rate(nv_inference_request_success[5m]))
  ```
* Triton failures over time:

  ```promql
  sum by (model) (rate(nv_inference_request_failure[5m]))
  ```
* Inference count rate:

  ```promql
  sum by (model) (rate(nv_inference_count[5m]))
  ```
* Request duration (convert µs to s if needed):

  ```promql
  rate(nv_inference_request_duration_us[5m]) / 1e6
  ```
* GPU utilization:

  ```promql
  avg by (device_id) (gpu_utilization)
  ```
* GPU power (watts):

  ```promql
  avg by (device_id) (gpu_power_usage_watts) / 1000
  ```

---

## 5) Correlate with NIM Service Metrics

The NIM service also exposes metrics (Python process/runtime, GPU metrics). Some handy examples:

* Process CPU seconds total:

  ```promql
  rate(process_cpu_seconds_total[5m])
  ```
* Memory RSS:

  ```promql
  process_resident_memory_bytes
  ```
* GPU total energy:

  ```promql
  rate(gpu_total_energy_consumption_joules[5m])
  ```

---

## 6) Optional: Filter to Your Specific Model or Namespace

You can add Grafana variables to filter by model label. For example:

* Variable query:

  ```promql
  label_values(nv_inference_request_success, model)
  ```
* Use it in panel queries:

  ```promql
  sum by (model) (rate(nv_inference_request_success{model=~"$model"}[5m]))
  ```

---

## 7) Validate Data is Flowing

You should see:

* Success counters increasing
* Non-zero rates for `nv_inference_count` and `nv_inference_exec_count`
* GPU utilization and power changing during requests

If rates are flat, wait a minute for rate windows to populate or reduce your request interval:

```bash
kubectl patch configmap -n nim-test-workload nim-embedding-test-config --patch '{"data":{"REQUEST_INTERVAL":"5"}}'
kubectl rollout restart deployment -n nim-test-workload nim-embedding-test
```

---

✅ At this point, your Grafana should be ready to explore test data.
*(Optionally, you can also port-forward Grafana from this terminal and confirm the dashboard import.)*

```

Do you want me to also **add screenshots placeholders** (e.g., `![Grafana Dashboard](./images/grafana-dashboard.png)`) to make the README more visual?
```
