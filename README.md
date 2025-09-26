# 🌐 **SOCIAL CONNECT** 🤝  

## 📝 **Project Description**  

Social Connect is a full-stack social media platform that lets users create profiles, post updates, follow friends, and interact through likes, comments, and private messaging. It’s built to demonstrate how modern web frameworks, APIs, and databases can be combined to deliver an engaging, scalable social experience.  

---

## ✨ **Features**  

- **User Authentication & Profiles** 🔑: Secure sign-up, login, and profile management with profile pictures & bios.  
- **Post Creation & Feeds** 📝: Users can create posts (text, images, or videos) and view a personalized timeline.  
- **Likes & Comments** ❤️💬: Real-time interactions on posts.  
- **Follow/Unfollow System** 👥: Users can follow each other to customize their feed.  
- **Direct Messaging** 📩: Private chat between users.  
- **Notifications** 🔔: Instant alerts for likes, comments, and new followers.  
- **RESTful API Endpoints** 🌐: Backend endpoints for all operations (authentication, posts, interactions, messaging).  
- **Validation & Error Handling** ✅: Ensures clean input and informative error messages.  
- **Responsive Frontend** 📱: Works seamlessly on desktop and mobile.  

---

## 📂 **Project Structure**  

```
SOCIAL CONNECT/
|
|---src/                 # Core application logic
|    |---db.py/         # Database models (Users, Posts, Comments)
|    |---logic.py/       # Business logic 
|
|---api/                 # Backend API
|    |---main.py         # FastAPI/Express endpoints
|
|---frontend/            # Frontend application
|    |---app.py/          # Main pages (feed, profile, messaging)
|
|---requirements.txt     # Python dependencies
|---README.md            # Project Documentation
|---.env                 # Environment variables
```

---

## 🚀 **Quick Start**  

### **Prerequisites**  
- Python 3.9+ (if backend in FastAPI) 🐍  
- PostgreSQL / Supabase 
- Git for cloning 🪴  

### **1. Clone the Project**  
```bash
git clone <repo-url>
cd social-connect
```

### **2. Install Dependencies**  

Python backend:  
```bash
pip install -r requirements.txt
```  


### **3. Setup Database**  

Create the required tables/collections in your database (users, posts, comments, messages). Run included migration/SQL scripts if provided.  

### **4. Configure Environment Variables**  

Create a `.env` file in the root directory and add your credentials:  

```ini
DATABASE_URL=YOUR_DATABASE_URL
SECRET_KEY=YOUR_SECRET_KEY
API_BASE_URL=http://localhost:8000
```

### **5. Run the Application**  

Frontend:  
```bash
cd frontend
streamlit run app.py
```  

Backend:  
```bash
cd api
uvicorn main:app --reload   # (if FastAPI)


---

## 💡 **How to Use**  

1. Sign up for an account.  
2. Set up your profile (photo, bio).  
3. Post updates and follow friends.  
4. Like, comment, and send messages.  

---

## 💻 **Technologies Used**  

- **Frontend**: Streamlit ✨  
- **Backend**: FastAPI (Python) ⚡  
- **Database**: PostgreSQL 
- **Authentication**: JWT / OAuth2 🔒  

### **Key Components**  

- `src/db.py/`: Database schemas.  
- `src/logic.py/`: Core logic (feed generation, notifications).  
- `api/main.py`: REST API endpoints.  

---

## ⚠️ **Troubleshooting**  

### **1. Backend Issues**  

- **`500 Internal Server Error`** 💥  
  - **Reason:** Misconfigured database connection.  
  - **Solution:** Check your `.env` credentials and verify the database is running.  

- **CORS Errors** 🌐  
  - **Reason:** Frontend and backend on different ports.  
  - **Solution:** Enable CORS in your backend.  

### **2. Frontend Issues**  

- **`ConnectionError`** 🔌  
  - **Reason:** Backend not running.  
  - **Solution:** Start the backend server first.  

---

## 📈 **Future Enhancements**  

- **Stories Feature** 📸: Temporary photo/video updates.  
- **Group Chats** 👨‍👩‍👧‍👦: Multi-user messaging.  
- **Advanced Search** 🔍: Find users, posts, and hashtags.  
- **Push Notifications** 📲: Real-time mobile/web notifications.  
- **Media Uploads to Cloud Storage** ☁️: AWS S3 or Cloudinary integration.  
- **Analytics Dashboard** 📊: Insights into user activity.  

---

## 🤝 **Support**  

If you encounter any issues or have questions, please feel free to reach out:  

- Email: `arthampraneeth977@example.com` 📧  
