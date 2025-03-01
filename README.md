# LLM Chatbot with Database Logging and Kubernetes Deployment

## Overview
This project demonstrates an LLM-powered chatbot that:
- Serves an LLM via a FastAPI REST API.
- Logs conversation history to a PostgreSQL database.
- Is containerized with Docker.
- Provides Kubernetes manifests for production deployment.

For demonstration purposes, the chatbot uses a Hugging Face text-generation pipeline (e.g., GPT-2). You can easily replace this integration with Ollama or any other LLM serving solution.

## Features
- **LLM Chatbot Endpoint:** A REST API (built with FastAPI) that accepts user messages and returns LLM-generated responses.
- **Database Logging:** Conversation logs are saved to a PostgreSQL database (using SQLAlchemy). You can also switch to another database by updating the connection string.
- **Containerization:** A Dockerfile is provided to build a container image.
- **Kubernetes Deployment:** YAML manifests are provided to deploy both the chatbot and a PostgreSQL database in a Kubernetes cluster.
- **Interactive Notebook:** An interactive Jupyter Notebook for testing and exploration.

## Project Structure
```
llm-chatbot/
├── README.md                 # Overview, installation, usage, and deployment instructions.
├── requirements.txt          # Python package dependencies.
├── Dockerfile                # Container configuration.
├── app.py                    # FastAPI app serving the chatbot and logging to the database.
├── database.py               # Database connection and models (using SQLAlchemy).
├── k8s/
│   ├── deployment.yaml       # Kubernetes Deployment manifest for the FastAPI app.
│   ├── service.yaml          # Kubernetes Service manifest for the FastAPI app.
│   └── postgres.yaml         # Kubernetes manifest for a PostgreSQL instance.
└── notebooks/
    └── Chatbot_Development.ipynb  # Notebook for interactive testing and exploration.
```

## Installation

**Clone the Repository:**
```
   git clone https://github.com/mda84/llm-chatbot.git
   cd llm-chatbot
```

Create and Activate a Virtual Environment:
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install Dependencies:
```
pip install -r requirements.txt
```

Running Locally
Set Environment Variables:

DATABASE_URL: Connection string for the database (e.g., postgresql://user:password@localhost:5432/chatbot_db).
If not provided, the app defaults to a local SQLite database.
(Optional) Configure other settings as needed.
Run the App:
```
uvicorn app:app --host 0.0.0.0 --port 8000
```

The chatbot endpoint will be available at http://localhost:8000/chat.

## Docker Deployment
Build the Docker Image:
```
docker build -t llm-chatbot .
```

## Run the Container:
```
docker run -it -p 8000:8000 llm-chatbot
```

## Kubernetes Deployment
In the k8s/ directory, you'll find:

deployment.yaml: Deployment manifest for the FastAPI chatbot.
service.yaml: Service manifest to expose the chatbot.
postgres.yaml: Manifest to deploy PostgreSQL.

To deploy on your Kubernetes cluster:
```
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Interactive Notebook
Open the interactive notebook:
```
jupyter notebook notebooks/Chatbot_Development.ipynb
```

## License
This project is licensed under the MIT License.

## Contact
For questions or contributions, please contact dorkhah9@gmail.com