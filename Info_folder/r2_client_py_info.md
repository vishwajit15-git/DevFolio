# `backend/r2_client.py`

## Purpose
A new Boto3-powered client module created to securely interact with the Cloudflare R2 API.

## Features
1. Uses S3-compatible `boto3` client to upload objects to Cloudflare R2.
2. Authenticates securely using `.env` secrets (`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`).
3. Returns a public URL string based on the provided custom domain or `.r2.dev` link.
4. Allows DevFolio to scale its 9,000+ screenshots (1,800 portfolios * 5) cheaply with R2's zero-egress fee architecture.
