# `backend/gcs_client.py`

## Purpose
A Google Cloud Storage client module created to securely interact with the GCP Storage API for DevFolio image hosting.

## Features
1. Uses `google-cloud-storage` client to upload objects to GCP.
2. Authenticates securely using `.env` secrets (`GOOGLE_APPLICATION_CREDENTIALS`, `GCS_PROJECT_ID`, `GCS_BUCKET_NAME`) via a service account JSON file.
3. Returns a public URL string `https://storage.googleapis.com/...`.
4. Allows DevFolio to scale its 9,000+ screenshots (1,800 portfolios * 5) to enterprise-grade infrastructure.
