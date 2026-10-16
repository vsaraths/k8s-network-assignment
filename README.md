# Kubernetes Networking Troubleshooting Assignment

## 1. Project Overview

This project demonstrates Kubernetes application networking using three components:

- Client: Sends HTTP requests to the frontend.
- Frontend: Receives requests and calls the backend.
- Backend: Returns an orders response.

## 2. Architecture

Client → frontend-service:8081 → Frontend Pod
Frontend Pod → backend-service:8080 → Backend Pod

## 3. Healthy Baseline

The backend and frontend Deployments were running successfully.

Both Kubernetes Services had valid endpoints. A request to
`http://frontend-service:8081/orders` returned the expected JSON response.

## 4. Symptom

After introducing a Service selector mismatch, client requests
failed with HTTP 500 Internal Server Error.

## 5. Investigation

Commands used:

```bash
kubectl get pods -o wide
kubectl get services
kubectl get endpointslices
kubectl logs deployment/client --since=2m
kubectl get endpointslices -l kubernetes.io/service-name=backend-service
```

The backend Service EndpointSlice showed no endpoints.

## 6. Root Cause

The backend Service selector was changed to:

`app: wrong-backend`

The backend Pod had the label:

`app: backend`

Because the labels did not match, Kubernetes could not associate the backend Pod with the Service. Requests from the frontend therefore failed.

## 7. Resolution

Restored the correct Service selector:

```bash
kubectl patch service backend-service -p '{"spec":{"selector":{"app":"backend"}}}'
```

## 8. Verification

The EndpointSlice again showed the backend endpoint at
`10.244.0.5:8080`.

The following test returned a successful orders response:

```bash
kubectl run network-test --rm -i --restart=Never --image=curlimages/curl:latest -- curl -sS http://frontend-service:8081/orders
```

The response confirmed that frontend-to-backend communication was restored.

## 9. Key Learnings

- Kubernetes Services use label selectors to identify backend Pods.
- A running Pod does not guarantee that a Service can route traffic to it.
- EndpointSlices help diagnose missing Service endpoints.
- Kubernetes DNS enables communication using Service names.
- Logs, selectors, and endpoints provide evidence for troubleshooting.
