# SmartSpark - AI-Powered Chat Application

## 🚀 Project Overview

SmartSpark is a modern, full-stack AI chat application that provides an intelligent conversational interface powered by OpenAI's GPT-4. The application features a responsive React frontend with dark/light mode support and a robust FastAPI backend with MongoDB integration for conversation persistence.

## ✨ Features

### Frontend Features
- **Modern React UI** with responsive design
- **Dark/Light Mode Toggle** with persistent theme preference
- **Real-time Chat Interface** with smooth scrolling
- **Conversation Management** - start new conversations or continue existing ones
- **Loading States** and error handling
- **Mobile-responsive** design using Tailwind CSS

### Backend Features
- **FastAPI REST API** with automatic OpenAPI documentation
- **OpenAI GPT-4 Integration** for intelligent responses
- **MongoDB Database** for conversation persistence
- **CORS Support** for cross-origin requests
- **Environment-based Configuration** for secure deployment
- **Comprehensive Error Handling** and validation

### Core Functionality
- **AI Chat Interface** - Send messages and receive intelligent responses
- **Conversation History** - All conversations are saved and retrievable
- **Session Management** - Continue conversations across sessions
- **API Endpoints** for chat, conversation management, and data retrieval

## 🛠️ Tech Stack

### Frontend
- **React 19** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **React Router** - Client-side routing
- **CRACO** - Create React App Configuration Override

### Backend
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Emergent Integrations** - OpenAI API integration
- **Python-dotenv** - Environment variable management

### Database
- **MongoDB** - NoSQL database for conversation storage

### Deployment
- **Vercel** - Frontend deployment
- **Environment Variables** - Secure configuration management

## 📁 Project Structure

```
Smartspark/
├── backend/
│   ├── server.py          # FastAPI server with chat endpoints
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styling
│   │   └── index.js       # React entry point
│   ├── package.json       # Node.js dependencies
│   └── vercel.json        # Vercel deployment config
├── tests/
│   └── backend_test.py    # API testing suite
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- MongoDB (local or cloud instance)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd Smartspark/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "MONGO_URL=mongodb://localhost:27017" >> .env
   echo "DB_NAME=smartspark" >> .env
   ```

4. Start the backend server:
   ```bash
   uvicorn server:app --reload --port 8001
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd Smartspark/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Create .env file
   echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
   ```

4. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## 🔧 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send a message and receive AI response
- `GET /api/conversations/{conversation_id}` - Get specific conversation
- `GET /api/conversations` - Get all conversations
- `DELETE /api/conversations/{conversation_id}` - Delete conversation

### Health Check
- `GET /` - API health check

## 🧪 Testing

### Backend Testing
Run the comprehensive API test suite:
```bash
cd Smartspark
python backend_test.py
```

The test suite covers:
- API health checks
- Chat functionality
- Conversation management
- Error handling
- Data persistence

## 🚀 Deployment

### Frontend Deployment (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard:
   - `REACT_APP_BACKEND_URL` - Your backend API URL
3. Deploy automatically on push to main branch

### Backend Deployment
The backend can be deployed to any Python hosting service (Railway, Render, Heroku, etc.) with the following environment variables:
- `OPENAI_API_KEY`
- `MONGO_URL`
- `DB_NAME`

## 🔒 Security Features

- **Environment Variables** - Sensitive data stored securely
- **CORS Configuration** - Proper cross-origin request handling
- **Input Validation** - Pydantic models for data validation
- **Error Handling** - Comprehensive error responses

## 📊 Performance Features

- **Async/Await** - Non-blocking backend operations
- **Optimized Build** - Production-ready React build
- **Database Indexing** - Efficient MongoDB queries
- **Caching** - Browser-level caching for static assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🔗 Live Demo

[Add your deployed application URL here]

---

**Built with ❤️ using React, FastAPI, and OpenAI**
