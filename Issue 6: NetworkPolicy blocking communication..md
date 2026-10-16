
## Issue 6: NetworkPolicy Blocking Communication

### Symptom
Requests to the frontend `/orders` endpoint returned HTTP 500 Internal Server Error.

### Investigation
Created a NetworkPolicy named `block-backend-ingress` targeting Pods with the label `app: backend` and denying all ingress traffic.

### Observations
- The baseline frontend-to-backend request succeeded before applying the policy.
- The policy selected backend Pods and isolated them for ingress connectivity.
- After applying the policy, requests through the frontend returned HTTP 500.

### Root Cause
The NetworkPolicy denied incoming traffic to the backend Pods, preventing the frontend from reaching the backend.

### Resolution
Deleted the intentional blocking policy:

```bash
kubectl delete networkpolicy block-backend-ingress
```

### Verification
Retested the frontend `/orders` endpoint after removing the policy. The request returned the expected successful backend response.

**Result:** Resolved.
<img width="1895" height="449" alt="image" src="https://github.com/user-attachments/assets/423cf8fa-af1a-41fc-ba3e-2182e8c413b2" />
<img width="1901" height="657" alt="image" src="https://github.com/user-attachments/assets/c4f14d28-1050-4919-a159-86b346bbf739" />
<img width="1901" height="486" alt="image" src="https://github.com/user-attachments/assets/2f20fcce-19a5-4c1d-8399-9b99645ebde9" />


