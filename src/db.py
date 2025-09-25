import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_KEY:
    raise ValueError("Supabase Key not found. Please check your .env file.")
if not SUPABASE_URL:
    raise ValueError("Supabase URL not found. Please check your .env file.")

sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class DatabaseManager:
    def __init__(self):
        self.sb = sb
        self.current_user = None

    def signup(self, username, password, role: str = "user"):
        existing_user = self.sb.table("profiles").select("id").eq("username", username).execute()
        if existing_user.data:
            return {"error": "Username already exists"}

        result = self.sb.table("profiles").insert({
            "username": username,
            "password": password,
            "role": role
        }).execute()
        return result.data

    def login(self, username: str, password: str):
        result = self.sb.table("profiles").select("*").eq("username", username).execute()
        if not result.data:
            return {"error": "User not found"}

        user = result.data[0]
        if user["password"] == password:
            self.current_user = user
            return {"message": "Login successful", "user": user['username']}
        else:
            return {"error": "Invalid password"}

    def get_user_by_username(self, username: str):
        result = self.sb.table("profiles").select("id", "username", "created_at", "role").eq("username", username).execute()
        return result.data[0]

    def create_post(self, content: str, image_url: str = ""):
        if not self.current_user:
            return {"error": "User not logged in"}

        result = self.sb.table("posts").insert({
            "user_id": self.current_user["id"],
            "content": content,
            "image_url": image_url
        }).execute()
        return result.data

    def like_post(self, post_id: int):
        if not self.current_user:
            return {"error": "User not logged in"}

        existing_like = self.sb.table("likes").select("*") \
            .eq("user_id", self.current_user["id"]) \
            .eq("post_id", post_id).execute()

        if existing_like.data:
            return {"error": "Post already liked"}

        result = self.sb.table("likes").insert({
            "user_id": self.current_user["id"],
            "post_id": post_id
        }).execute()
        return result.data

    def unlike_post(self, post_id: int):
        if not self.current_user:
            return {"error": "User not logged in"}

        self.sb.table("likes").delete().match({
            "user_id": self.current_user["id"],
            "post_id": post_id
        }).execute()

        return {"message": "Unliked successfully"}

    def comment_post(self, post_id: int, content: str):
        if not self.current_user:
            return {"error": "User not logged in"}

        result = self.sb.table("comments").insert({
            "user_id": self.current_user["id"],
            "post_id": post_id,
            "content": content
        }).execute()
        return result.data

    def get_posts(self):
        result = self.sb.table("posts").select("*").execute()
        return result.data

    def get_post_by_id(self, post_id: int):
        result = self.sb.table("posts").select("*").eq("id", post_id).execute()
        return result.data
s=DatabaseManager()
print(s.login("praneeth","artham432779"))
print(s.get_post_by_id(2))