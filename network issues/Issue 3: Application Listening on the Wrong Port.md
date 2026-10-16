## Issue 3: Application Listening on the Wrong Port

### Symptom
Requests through the backend Service failed, and the frontend returned HTTP 500 Internal Server Error.

### Investigation
The backend application was intentionally changed to listen on port 8088, while the Kubernetes Service continued forwarding traffic to port 8080.

The backend logs showed:

```text
Running on http://127.0.0.1:8088
```

The request to the backend Service failed with a connection error.

### Observations
- The backend Pod was Running and Ready.
- The backend Service targeted port 8080.
- The application was listening on port 8088.
- The source file was subsequently restored to port 8080, and the rebuilt image was deployed.

### Root Cause
The application's listening port did not match the port expected by the Kubernetes Service.

### Resolution
Changed the application back to port 8080, rebuilt the backend image, loaded it into Kind, and updated the Deployment to use the corrected image.

### Verification
The new backend Pod logs confirmed that the application was listening on port 8080. Subsequent requests to `/orders` returned HTTP 200 OK.

**Result:** Resolved.

<img width="1911" height="624" alt="image" src="https://github.com/user-attachments/assets/d32318f9-132d-45be-9d07-1753f27e4557" />
