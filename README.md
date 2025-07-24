# Smart Medical Assistant

A comprehensive AI-powered medical assistant application that analyzes patient symptoms, provides medical recommendations, and suggests appropriate healthcare providers. Built with LangGraph, FastAPI, and Streamlit.

## Features

- **Symptom Analysis**: Natural language processing to parse and understand patient symptoms
- **Medical Condition Prediction**: AI-powered prediction of potential medical conditions
- **Action Recommendations**: Personalized healthcare recommendations based on symptoms and history
- **Doctor Suggestions**: Intelligent recommendation of medical specializations
- **Location-based Doctor Search**: Find nearby healthcare providers using location data
- **Patient History Tracking**: MongoDB-powered patient record management
- **Interactive Web Interface**: User-friendly Streamlit frontend

## Architecture

The application uses a **LangGraph-based workflow** with the following nodes:

1. **Symptom Parser** - Extracts key symptoms from user descriptions
2. **History Checker** - Retrieves patient medical history from MongoDB
3. **Condition Predictor** - Uses AI to predict potential medical conditions
4. **Action Recommender** - Provides personalized treatment recommendations
5. **Doctor Suggester** - Recommends appropriate medical specializations
6. **Doctor Search** - Finds nearby healthcare providers using Tavily search
7. **History Updater** - Updates patient records with new consultation data

## Tech Stack

- **Backend**: FastAPI
- **AI/ML**: LangChain, OpenAI GPT, Groq LLaMA
- **Workflow**: LangGraph
- **Database**: MongoDB
- **Search**: Tavily Search API
- **Frontend**: Streamlit
- **Environment**: Python 3.8+

## Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB instance
- OpenAI API key
- Groq API key
- Tavily Search API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your_username>/Smart-Medical-Assistant.git
   cd smart-medical-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI=mongodb://localhost:27017/smart_medical_db
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Database Setup**
   - Ensure MongoDB is running
   - The application will automatically create the required collections

## Usage

### Starting the Backend Server

```bash
python app/main.py
```

The FastAPI server will start on `http://localhost:8000`

### Starting the Frontend

```bash
streamlit run streamlit_app/ui.py
```

The Streamlit app will be available at `http://localhost:8501`

### API Endpoints

#### POST `/api/analyze`

Analyzes patient symptoms and provides comprehensive medical recommendations.

**Request Body:**
```json
{
  "patient_id": "string",
  "symptoms": "string",
  "location": "string"
}
```

**Response:**
```json
{
  "patient_id": "string",
  "symptoms": "string",
  "location": "string",
  "parsed_symptoms": "string",
  "history": {},
  "predicted_condition": "string",
  "recommended_action": "string",
  "recommended_doctor": "string",
  "nearby_doctors": []
}
```

## Project Structure

```
smart-medical-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── core/
│   │   ├── graph.py           # LangGraph workflow definition
│   │   └── state.py           # State management
│   ├── nodes/                 # LangGraph workflow nodes
│   │   ├── symptom_parser.py
│   │   ├── check_history.py
│   │   ├── predict_condition.py
│   │   ├── recommend_action.py
│   │   ├── suggest_doctor.py
│   │   ├── search_doctors_nearby.py
│   │   └── update_history.py
│   ├── routes/
│   │   └── analyze.py         # API route handlers
│   └── services/
│       └── mongodb.py         # Database operations
├── streamlit_app/
│   └── ui.py                  # Streamlit frontend
├── requirements.txt
└── README.md
```

## Key Components

### LangGraph Workflow

The application uses a sequential workflow that processes patient data through multiple specialized nodes, ensuring comprehensive analysis and recommendations.

### AI Models Integration

- **OpenAI GPT**: Primary model for medical analysis and recommendations
- **Groq LLaMA**: Alternative model for action recommendations
- **LangChain**: Framework for building AI-powered applications

### Database Schema

**Patient Collection:**
```json
{
  "patient_id": "string",
  "history": [
    {
      "parsed_symptoms": "string",
      "predicted_condition": "string",
      "recommended_action": "string",
      "recommended_doctor": "string",
      "timestamp": "datetime"
    }
  ]
}
```

## Features in Detail

### Symptom Analysis
- Natural language processing for symptom extraction
- Intelligent parsing of complex medical descriptions
- Context-aware symptom categorization

### Medical Prediction
- AI-powered condition prediction
- Integration of patient history for accurate diagnosis
- Multi-model approach for enhanced reliability

### Doctor Recommendations
- Specialization matching based on predicted conditions
- Location-based healthcare provider search
- Real-time availability and contact information

### Patient History Management
- Comprehensive medical record storage
- Historical pattern analysis
- Trend identification for chronic conditions

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGO_URI` | MongoDB connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `GROQ_API_KEY` | Groq API key | Yes |
| `TAVILY_API_KEY` | Tavily Search API key | Yes |

## Development

### Adding New Nodes

1. Create a new node file in `app/nodes/`
2. Implement the node function following the existing pattern
3. Add the node to the graph in `app/core/graph.py`
4. Update the state schema in `app/core/state.py` if needed

### Extending the API

1. Add new routes in `app/routes/`
2. Include the router in `app/main.py`
3. Update the Streamlit UI if needed

