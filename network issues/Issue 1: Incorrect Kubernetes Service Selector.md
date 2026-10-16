## Issue 1: Incorrect Kubernetes Service Selector

### Symptom
Requests through `backend-service` failed because the Service could not find the backend Pod endpoints.

### Investigation
The backend Service selector was intentionally changed to `app: wrong-backend`.

Commands used:

```bash
kubectl patch service backend-service -p '{"spec":{"selector":{"app":"wrong-backend"}}}'
kubectl get endpoints backend-service
```

### Observations
The Service had no endpoints because its selector did not match the backend Pod label.

The backend Pod uses the label:

```yaml
app: backend
```

### Root Cause
The Service selector `app: wrong-backend` did not match the backend Pod's label `app: backend`.

### Resolution
Restored the correct Service selector:

```bash
kubectl patch service backend-service -p '{"spec":{"selector":{"app":"backend"}}}'
```

### Verification
Confirmed that the backend endpoint was available again and tested the application through the frontend Service.

The request succeeded and returned the backend response:

```json
{
  "message": "Orders retrieved successfully",
  "service": "backend"
}
```

**Result:** Resolved. The Service selector correctly identifies the backend Pod.
<img width="1916" height="415" alt="Screenshot_20" src="https://github.com/user-attachments/assets/4a447522-2548-4ccb-82fa-3a7571630644" />
<img width="1919" height="605" alt="Screenshot_19" src="https://github.com/user-attachments/assets/fcd2a39c-42a6-43e1-b11f-1fdd696d4256" />
<img width="1291" height="341" alt="Screenshot_16" src="https://github.com/user-attachments/assets/2342ac59-abd1-4937-b1e0-51635ab5ff11" />
<img width="946" height="472" alt="Screenshot_17" src="https://github.com/user-attachments/assets/5762f323-affc-4c7d-9780-9ecd45ef7d38" />
---<img width="1909" height="684" alt="Screenshot_18" src="https://github.com/user-attachments/assets/0282c906-edfb-4c63-8610-61d8db2de67f" />
