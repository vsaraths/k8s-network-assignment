## Issue 2: Incorrect Service targetPort

### Symptom
Requests to `http://backend-service:8080/orders` failed with a connection error.

### Investigation
The backend Service's `targetPort` was intentionally changed from `8080` to `8088`.

Command used:

```bash
kubectl patch service backend-service -p '{"spec":{"ports":[{"port":8080,"targetPort":8088}]}}'
```

The endpoint and connectivity were checked:

```bash
kubectl get endpoints backend-service
kubectl run network-test-2 --rm -i --restart=Never --image=curlimages/curl:latest -- curl --connect-timeout 3 --max-time 5 -sS http://backend-service:8080/orders
```

### Observations
The endpoint showed:

```text
10.244.0.5:8088
```

The test returned a connection error:

```text
curl: (7) Failed to connect to backend-service:8080
```

The backend application was still listening on port `8080`.

### Root Cause
The Service forwarded traffic to port `8088`, where the backend application was not listening.

### Resolution
Restored the correct `targetPort`:

```bash
kubectl patch service backend-service -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

### Verification
Ran a new request:

```bash
kubectl run network-test-2-fixed --rm -i --restart=Never --image=curlimages/curl:latest -- curl -sS http://backend-service:8080/orders
```

Successful response:

```json
{
  "message": "Orders retrieved successfully",
  "service": "backend"
}
```

**Result:** Resolved. The Service forwards traffic to the correct backend port.

---

## Summary

| Issue | Root Cause | Status |
|---|---|---|
| Incorrect Service selector | Service selector did not match Pod labels | Resolved |
| Incorrect `targetPort` | Service forwarded traffic to the wrong port | Resolved |

<img width="1900" height="359" alt="image" src="https://github.com/user-attachments/assets/60edc575-b747-416b-92d5-e1bced58c69f" />


## Lessons Learned

- Kubernetes Service selectors must match the labels on the intended Pods.
- A Service can have endpoints but still fail to connect if its `targetPort` is incorrect.
- Endpoint inspection and connectivity tests help identify networking failures.
- Always verify that application connectivity works after applying a fix.

*Additional networking troubleshooting scenarios will be documented here as they are tested and verified.*
