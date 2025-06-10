# Crud Application

This repository contains a simple full-stack authentication application built with React (frontend) and FastAPI (backend).

## Project Structure

```
.
├── docker-compose.yml
├── fastapi
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src
│       ├── main.py
│       ├── routers
│       │   └── auth.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── config.py
│       └── database.py
└── react-app
├── Dockerfile
├── package.json
└── src
├── api
│   └── client.ts
├── components
│   ├── Auth
│   │   └── Login.tsx
│   └── Home.tsx
└── pages
├── AuthPage.tsx
└── HomePage.tsx
```

## API Endpoints

### Authentication (`/auth`)

* **POST** `/auth/register`: User registration
* **POST** `/auth/login`: User login
* **PATCH** `/auth/user`: Update user profile
* **POST** `/auth/logout`: User logout

### Default

* **GET** `/`: Root endpoint

## Schemas

* `UserCreate`
* `UserRead`
* `Token`

## Technologies

* **Frontend**: React, Vite, TypeScript
* **Backend**: FastAPI, SQLAlchemy, JWT
* **Database**: PostgreSQL

## Usage

1. Ensure PostgreSQL is running and properly configured.
2. Start FastAPI backend:

```
cd fastapi
uvicorn src.main\:app --reload
```

3. Start React frontend:

```
cd react-app
npm install
npm run dev
```
