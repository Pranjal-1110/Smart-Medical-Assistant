# Smart Medical Assistant: Production-Grade AI Agents System

A comprehensive, enterprise-grade medical assistant application that uses a multi-stage AI workflow to analyze patient symptoms, provide personalized medical recommendations, and suggest verified healthcare providers.

This application has been fully refactored for **security, performance, and scalability**, implementing modern backend engineering practices like JWT-based authentication, Role-Based Access Control (RBAC), and Redis caching.

-----

## 🌟 Key Features

The project has been enhanced from an AI demo to a production-ready microservice system.

  * **🔐 Enterprise Authentication**: Implemented OAuth 2.0 Authorization Code flow (via Google) and secure Email/Password registration.
  * **🛡️ Role-Based Access Control (RBAC)**: Supports roles (`patient`, `pending_doctor`, `doctor`) with a secure, multi-step verification process for doctors.
  * **⚡ Performance Caching**: Redis integration for sub-millisecond retrieval of common AI analysis and doctor search results, reducing latency and cost.
  * **🧠 Intelligent Two-Stage AI Analysis**: The LangGraph pipeline is split into a generic, cacheable **Primary Analysis** and a personalized, history-aware **Condition Predictor**.
  * **Location-based Doctor Search**: Find nearby healthcare providers using Tavily search (now cached).
  * **Patient History Tracking**: Asynchronous MongoDB (Motor) powered patient record management.

-----

## 🏛️ Architecture

The application uses a **LangGraph-based workflow** with 8 nodes to ensure comprehensive and secure analysis:

1.  **Symptom Parser**: Extracts canonical, keyword-based symptoms from user descriptions.
2.  **Primary Analysis (New)**: Performs a **general, cacheable** AI prediction based *only* on symptoms. (Cache Hit/Miss Check).
3.  **History Checker**: Retrieves patient medical history from MongoDB (Async Motor).
4.  **Condition Predictor**: Uses AI to predict the final, **personalized** medical condition by combining Primary Analysis with patient history.
5.  **Action Recommender**: Provides personalized treatment recommendations based on the final condition.
6.  **Doctor Suggester**: Recommends the appropriate medical specialization.
7.  **Doctor Search (Cacheable)**: Finds nearby healthcare providers using Tavily search (Cache Hit/Miss Check).
8.  **History Updater**: Updates patient records with new consultation data.

-----

## 💻 Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | FastAPI, Uvicorn | High-performance, asynchronous API framework. |
| **AI/ML** | LangChain, OpenAI GPT, Groq LLaMA | Frameworks for building LLM-powered nodes. |
| **Workflow** | **LangGraph** | State-of-the-art framework for creating stateful, multi-step AI agents. |
| **Security** | **Authlib**, **python-jose** | OAuth 2.0 implementation and JWT token management. |
| **Database** | MongoDB, **Motor** | Asynchronous (Async) driver for patient data persistence. |
| **Cache/Bus** | **Redis**, **redis-py** | In-memory data store for caching AI results and managing application lifespan. |
| **Search** | Tavily Search API | Tool for real-time, location-based doctor lookup. |
| **Frontend** | Streamlit | User-friendly web interface. |

-----

## ⚙️ Installation

### Prerequisites

  - Python 3.8 or higher
  - **MongoDB instance** (local or Atlas)
  - **Redis instance** (local or managed)
  - OpenAI API key
  - Groq API key
  - Tavily Search API key

### Setup

1.  **Clone the repository**

    ```bash
    git clone https://github.com/<your_username>/Smart-Medical-Assistant.git
    cd smart-medical-assistant
    ```

2.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**
    Create a `.env` file in the root directory:

    ```env
    # Database
    MONGO_URI=mongodb://localhost:27017/smart_medical_db
    # Redis (New)
    REDIS_URL=redis://localhost:6379/0

    # Security/Auth
    SECRET_KEY=your_long_secure_jwt_secret # MUST be changed in production
    OPENAI_API_KEY=your_openai_api_key
    GROQ_API_KEY=your_groq_api_key
    TAVILY_API_KEY=your_tavily_api_key

    # Google OAuth 2.0 (For login)
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret
    ```

-----

## 🚀 Usage

### Starting the Backend Server

```bash
python app/main.py
```

The FastAPI server will start on `http://localhost:8000`.

### API Endpoints

| Endpoint | Method | Security | Description |
| :--- | :--- | :--- | :--- |
| `/api/analyze` | `POST` | **Requires JWT** | Analyzes patient symptoms and provides recommendations. |
| `/api/auth/register` | `POST` | Public | Registers a new user with email/password. |
| `/api/auth/login` | `POST` | Public | Authenticates user and returns JWT token. |
| `/api/auth/login/google` | `GET` | Public | Initiates Google OAuth 2.0 login flow. |
| `/api/auth/me` | `GET` | **Requires JWT** | Returns data for the currently authenticated user. |
| `/api/auth/doctor/dashboard` | `GET` | **Requires 'doctor' role** | Example of a role-restricted endpoint. |

-----

## 🗂️ Project Structure

```
smart-medical-assistant/
├── app/
│   ├── auth/                # JWT, OAuth, and Dependency Injection for Security
│   ├── routes/
│   │   ├── analyze.py
│   │   └── auth.py          # Registration, Login, Google OAuth, Verification
│   ├── core/
│   │   ├── graph.py         # Updated 8-Node LangGraph Workflow
│   │   └── state.py         # Updated State Schema
│   ├── nodes/
│   │   ├── primary_analysis.py # NEW: Cacheable AI node
│   │   └── ... (6 original nodes)
│   ├── services/
│   │   ├── mongodb.py       # Asynchronous MongoDB with Motor
│   │   ├── redis_client.py  # NEW: Redis connection/caching utility
│   │   ├── password_hasher.py # NEW: Bcrypt hashing service
│   │   └── models.py        # Pydantic Schemas
├── streamlit_app/
└── README.md
```