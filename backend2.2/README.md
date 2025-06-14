# Crud Application

This repository contains a simple full-stack authentication application built with React (frontend) and FastAPI (backend).

### deploy

http://165.227.152.212:5173/home
http://165.227.152.212:8000/docs

## Project Structure

```
.
├── README.md
├── docker-compose.yml
├── fastapi
│   ├── Dockerfile
│   ├── README.md3
│   ├── requirements.txt
│   └── src
│       ├── __pycache__
│       │   ├── celery_app.cpython-312.pyc
│       │   ├── config.cpython-312.pyc
│       │   ├── crud.cpython-312.pyc
│       │   ├── database.cpython-312.pyc
│       │   ├── main.cpython-312.pyc
│       │   ├── models.cpython-312.pyc
│       │   ├── schemas.cpython-312.pyc
│       │   └── tasks.cpython-312.pyc
│       ├── assistant
│       │   ├── __pycache__
│       │   │   └── assistant.cpython-312.pyc
│       │   └── assistant.py
│       ├── celery_app.py
│       ├── config.py
│       ├── crud.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── routers
│       │   ├── __pycache__
│       │   │   ├── auth.cpython-312.pyc
│       │   │   └── chat.cpython-312.pyc
│       │   ├── auth.py
│       │   └── chat.py
│       ├── schemas.py
│       └── tasks.py
└── react-app
    ├── Dockerfile
    ├── README.md
    ├── eslint.config.js
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── public
    ├── src
    │   ├── App.css
    │   ├── App.tsx
    │   ├── api
    │   │   └── client.ts
    │   ├── assets
    │   ├── components
    │   │   ├── Auth
    │   │   │   ├── Login.tsx
    │   │   │   └── login.css
    │   │   ├── Chat
    │   │   │   ├── Chat.tsx
    │   │   │   └── chat.css
    │   │   ├── Home.module.css
    │   │   └── Home.tsx
    │   ├── index.css
    │   ├── main.tsx
    │   └── pages
    │       ├── AuthPage.tsx
    │       ├── ChatPage.tsx
    │       ├── HomePage.tsx
    │       └── chatPage.css
    ├── tsconfig.json
    ├── vite-env.d.ts
    ├── vite.config.js
    └── vite.config.ts

17 directories, 52 files

```

## API Endpoints

### Authentication (`/auth`)

* **POST** `/auth/register`: User registration
* **POST** `/auth/login`: User login
* **PATCH** `/auth/user`: Update user profile
* **POST** `/auth/logout`: User logout
* **DELETE** `/auth/user`: deletes user
* **PATCH** `/auth/user`: updates user


* **GET** `/chat/`: List Sessions
* **POST** `/chat/`: Create Session
* **GET** `/chat/{session_id}/messages`: Read  messages
* **POST** `/chat/{session_id}/message`: Post message

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
