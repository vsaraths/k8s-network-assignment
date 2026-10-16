
## Issue 5: Incorrect DNS / Kubernetes Service Name

### Symptom
Requests to the frontend `/orders` endpoint returned HTTP 500 Internal Server Error.

### Investigation
Changed the frontend environment variable `BACKEND_URL` from `http://backend-service:8080` to `http://backend-wrong:8080`.

### Observations
The frontend logs showed:

```text
Failed to resolve 'backend-wrong'
Temporary failure in name resolution
```

The frontend could not resolve the nonexistent Service hostname.

### Root Cause
The frontend was configured with an incorrect backend Service name.

### Resolution
Restored the environment variable to `BACKEND_URL=http://backend-service:8080`.

### Verification
After the frontend Deployment rollout, tested the `/orders` endpoint through `frontend-service`. The request returned the successful backend response.

**Result:** Resolved.
<img width="1892" height="455" alt="image" src="https://github.com/user-attachments/assets/126e2e3f-bfb6-4826-9b5b-347e78af6c7f" />
<img width="1898" height="226" alt="image" src="https://github.com/user-attachments/assets/fa4da7a8-05eb-48b7-a2e9-6dda7d5bf0df" />

