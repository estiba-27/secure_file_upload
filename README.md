# Secure File Upload System

A secure file upload and processing system with policy enforcement.  
Built with **FastAPI** (Python) backend and **React.js** frontend, supporting **file metadata extraction**, **policy validation**, and **admin review** of uploaded files.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture & Data Flow](#architecture--data-flow)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Trade-offs & Design Decisions](#trade-offs--design-decisions)
- [Folder Structure](#folder-structure)
-

---

## Project Overview

This system allows users to securely upload files, automatically validates them against defined policies, and enables administrators to review the file status (accepted/rejected). Uploaded files are stored in separate directories based on their policy compliance.

---

## Features

- User file uploads (via frontend form)
- Automatic extraction of file metadata (filename, size, hash)
- Policy enforcement on uploaded files
- Admin review of file status (Accepted / Rejected)
- Storage segregation: `accepted` and `rejected` directories
- Dashboard with dynamic file status display

---

## Architecture & Data Flow

```mermaid
flowchart LR
    A[User Upload Form] --> B[Frontend (React)]
    B --> C[Backend API (FastAPI)]
    C --> D[Policy Validation Service]
    D -->|Accepted| E[Accepted Storage Folder]
    D -->|Rejected| F[Rejected Storage Folder]
    C --> G[Database / Metadata Store]
    G --> B[File Table Dashboard]

## Installation & Setup
---
Backend:
# Clone repository
git clone https://github.com/estiba-27/secure-file-upload.git
cd secure-file-upload/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000

fronteend:
cd ../frontend
npm install
npm start
http://localhost:3000
opa
opa run --server --addr :8181 policies/


