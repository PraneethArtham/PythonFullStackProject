import sys
import os
# API/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.logic import SocialMediaPlatform   # your own logic
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
#uvicorn API.main:app --reload
# Add parent directory (project root) to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Now you can import from src
from src.logic import SocialMediaPlatform
from src.db import DatabaseManager


# --------------------------
# App setup
# --------------------------
app = FastAPI(title="Social Media Platform API", version="1.0")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize platform
social_platform = SocialMediaPlatform()

# --------------------------
# Pydantic Models
# --------------------------
class UserSchema(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class PostSchema(BaseModel):
    content: str
    image_url: Optional[str] = ""

class LikeSchema(BaseModel):
    post_id: int

class CommentSchema(BaseModel):
    post_id: int
    content: str

# --------------------------
# User Endpoints
# --------------------------
@app.post("/signup")
def signup(user: UserSchema):
    result = social_platform.signup(user.username, user.password, user.role)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": f"User {user.username} created successfully."}

@app.post("/login")
def login(user: UserSchema):
    result = social_platform.login(user.username, user.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": result["message"], "username": user.username}

# --------------------------
# Post Endpoints
# --------------------------
@app.post("/posts")
def create_post(post: PostSchema):
    result = social_platform.create_post(post.content, post.image_url)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Post created successfully", "post": result}

# @app.get("/posts")
# def get_posts():
#     posts = social_platform.get_posts()
#     return {"posts": posts}
@app.get("/posts")
def get_posts():
    try:
        posts = social_platform.get_posts()
        if posts is None:
            posts = []
        return {"posts": posts}
    except Exception as e:
        return {"posts": [], "error": str(e)}

# --------------------------
# Like / Unlike Endpoints
# --------------------------
@app.post("/posts/like")
def like_post(like: LikeSchema):
    result = social_platform.like_post(like.post_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Post liked successfully"}

@app.post("/posts/unlike")
def unlike_post(like: LikeSchema):
    result = social_platform.unlike_post(like.post_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Post unliked successfully"}

# --------------------------
# Comment Endpoint
# --------------------------
@app.post("/posts/comment")
def comment_post(comment: CommentSchema):
    result = social_platform.comment_post(comment.post_id, comment.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Comment added successfully", "comment": result}

# --------------------------
# Run the app
# --------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)