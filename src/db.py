import os
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
from datetime import datetime
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

    # def create_post(self, content: str, image_url: str = ""):
    #     if not self.current_user:
    #         return {"error": "User not logged in"}

    #     result = self.sb.table("posts").insert({
    #         "user_id": self.current_user["id"],
    #         "content": content,
    #         "image_url": image_url
    #     }).execute()
    #     return result.data
    # def upload_image(self, image_url: str) -> str:
    #     """Upload image from URL to Supabase storage and return public URL"""
    #     try:
    #         # Fetch the image content from given URL
    #         response = requests.get(image_url)
    #         if response.status_code != 200:
    #             raise Exception("Failed to download image")

    #         # Generate a unique filename
    #         filename = f"{self.current_user['id']}_{int(datetime.utcnow().timestamp())}.jpg"

    #         # Upload to Supabase storage bucket
    #         self.sb.storage.from_("images").upload(filename, response.content)

    #         # Get the public URL
    #         public_url = self.sb.storage.from_("images").get_public_url(filename)

    #         return public_url

    #     except Exception as e:
    #         print("❌ Error uploading image:", e)
    #         return None
    def upload_image(self, image_url: str) -> str:
        """Upload image from URL to Supabase storage and return public URL"""
        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                raise Exception("Failed to download image")

            filename = f"{self.current_user['id']}_{int(datetime.utcnow().timestamp())}.jpg"

            self.sb.storage.from_("images").upload(
                path=filename,
                file=response.content,
                file_options={"content-type": "image/jpeg"}
            )

            # ✅ Extract only the URL string
            public_url = self.sb.storage.from_("images").get_public_url(filename)


            return public_url

        except Exception as e:
            print("❌ Error uploading image:", e)
            return None


    def create_post(self, content: str, image_url: str = ""):
        """Create a new post with optional image upload"""
        if not self.current_user:
            return {"error": "User not logged in"}

        final_image_url = None
        if image_url:
            final_image_url = self.upload_image(image_url)

        data = {
            "content": content,
            "user_id": self.current_user["id"],
            "image_url": final_image_url
        }

        self.sb.table("posts").insert(data).execute()
        return {"success": True, "message": "Post created"}

    # def like_post(self, post_id: int):
    #     if not self.current_user:
    #         return {"error": "User not logged in"}

    #     existing_like = self.sb.table("likes").select("*") \
    #         .eq("user_id", self.current_user["id"]) \
    #         .eq("post_id", post_id).execute()

    #     if existing_like.data:
    #         return {"error": "Post already liked"}

    #     result = self.sb.table("likes").insert({
    #         "user_id": self.current_user["id"],
    #         "post_id": post_id
    #     }).execute()
    #     return result.data

    # def unlike_post(self, post_id: int):
    #     if not self.current_user:
    #         return {"error": "User not logged in"}

    #     self.sb.table("likes").delete().match({
    #         "user_id": self.current_user["id"],
    #         "post_id": post_id
    #     }).execute()

    #     return {"message": "Unliked successfully"}
    def count_likes(self, post_id: int) -> int:
        """Count number of likes for a post"""
        result = self.sb.table("likes").select("id", count="exact").eq("post_id", post_id).execute()
        return result.count or 0

    # def update_like_count(self, post_id: int) -> int:
    #     """Update the like_count column in posts table"""
    #     likes = self.count_likes(post_id)
    #     self.sb.table("posts").update({"like_count": likes}).eq("post_id", post_id).execute()
    #     return likes
    def update_like_count(self, post_id: int) -> int:
        """Update the like_count column in posts table"""
        likes = self.count_likes(post_id)
        # Use the correct column name (id instead of post_id)
        self.sb.table("posts").update({"like_count": likes}).eq("id", post_id).execute()
        return likes


    # def like_post(self, post_id: int):
    #     """Add a like and update like_count"""
    #     user_id=self.current_user["id"]
    #     exists = self.sb.table("likes").select("id").eq("id", post_id).eq("user_id", user_id).execute()
    #     if exists.data:
    #         return {"error": "Already liked"}
        
    #     self.sb.table("likes").insert({"post_id": post_id, "user_id": user_id}).execute()
    #     like_count = self.update_like_count(post_id)
    #     return {"success": True, "like_count": like_count}

    def like_post(self, post_id: int):
        if not self.current_user:
            return {"error": "User not logged in"}
        
        user_id = self.current_user["id"]

        # Check if the user already liked the post
        existing = self.sb.table("likes").select("id").eq("post_id", post_id).eq("user_id", user_id).execute()
        if existing.data:
            return {"message": "Already liked", "like_count": self.count_likes(post_id)}

        # Insert new like
        self.sb.table("likes").insert({"post_id": post_id, "user_id": user_id}).execute()

        # Update like_count
        like_count = self.update_like_count(post_id)
        return {"success": True, "like_count": like_count}

    def unlike_post(self, post_id: int):
        """Remove a like and update like_count"""
        if not self.current_user:
            return {"error": "User not logged in"}

        user_id = self.current_user["id"]

        # Check if the user has liked this post
        existing = self.sb.table("likes").select("id").eq("post_id", post_id).eq("user_id", user_id).execute()
        if not existing.data:
            # User hasn't liked this post
            return {"message": "You have not liked this post", "like_count": self.count_likes(post_id)}

        # Delete the like
        self.sb.table("likes").delete().eq("post_id", post_id).eq("user_id", user_id).execute()

        # Update the like_count column
        like_count = self.update_like_count(post_id)

        return {"success": True, "like_count": like_count}

    

    def comment_post(self, post_id: int, content: str):
        if not self.current_user:
            return {"error": "User not logged in"}

        result = self.sb.table("comments").insert({
            "user_id": self.current_user["id"],
            "post_id": post_id,
            "content": content
        }).execute()
        return result.data

    # def get_posts(self):
    #     result = self.sb.table("posts").select("*").execute()
    #     return result.data
    def get_posts(self):
        try:
            response = sb.table("posts").select("*").execute()
            posts = response.data
            print("📢 Processed posts:", posts)           # DEBUG
            return posts
        except Exception as e:
            print("❌ Error fetching posts:", e)
            return []

    def get_post_by_id(self, post_id: int):
        result = self.sb.table("posts").select("*").eq("id", post_id).execute()
        return result.data
# s=DatabaseManager()
# print(s.login("admin","artham432779"))
# print(s.create_post("image upload","ht108009A3A73D6A8E916D6E5388BE096CA8&selectedIndex=20&itb=0"))
