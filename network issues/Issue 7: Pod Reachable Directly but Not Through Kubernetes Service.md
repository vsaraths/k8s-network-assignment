
## Issue 7: Pod Reachable Directly but Not Through Kubernetes Service

### Symptom
Requests to the backend Pod IP succeeded, but requests through `backend-service` failed.

### Investigation
Tested the backend Pod directly at `10.244.0.18:8080/orders`. The request succeeded. Then changed the Service `targetPort` from 8080 to 8088 and tested through `backend-service:8080/orders`.

### Observations
- Direct Pod request returned `Orders retrieved successfully`.
- The Service request failed with a connection error.
- The backend application remained configured to listen on port 8080.

### Root Cause
The Service forwarded traffic to port 8088, while the backend application listened on port 8080.

### Resolution
Restored the Service `targetPort` to 8080.

### Verification
Retested through `backend-service:8080/orders`. The request returned the expected backend JSON response.

**Result:** Resolved.
