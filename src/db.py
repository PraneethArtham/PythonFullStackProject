import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if  not SUPABASE_KEY:
    raise ValueError(
        "Supabase  Key not found. Please check your .env file."
    )
if not SUPABASE_URL:
    raise ValueError(
        "Supabase URL  not found. Please check your .env file."
    )


print(SUPABASE_KEY,SUPABASE_URL)
sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
current_user=None


def signup(username, password, role: str = "user"):
    existing_user = sb.table("profiles").select("id").eq("username", username).execute()

    if existing_user.data: 
        return {"error": "Username already exists"}

    result = sb.table("profiles").insert({
        "username": username,
        "password": password,
        "role": role
    }).execute()

    return result.data


def login(username: str, password: str):
    global current_user
    result = sb.table("profiles").select("*").eq("username", username).execute()

    if not result.data:
        return {"error": "User not found"}

    user = result.data[0]

    if user["password"] == password: 
        current_user=user
        return {"message": "Login successful", "user": user['username']}
    
    else:
        return {"error": "Invalid password"}

def get_user_by_username(username: str):
    result = sb.table("profiles").select("id","username","created_at","role").eq("username", username).execute()
    return result.data[0] 

def create_post(content: str, image_url: str = ""):
    global current_user

    if not current_user:
        return {"error": "User not logged in"}

    result = sb.table("posts").insert({
        "user_id": current_user["id"],  
        "content": content,
        "image_url": image_url
    }).execute()

    return result.data

# def like_post(post_id: int):
#     global current_user
#     if not current_user:
#         return {"error": "User not logged in"}

#     result = sb.table("likes").insert({
#         "user_id": current_user["id"], 
#         "post_id": post_id
#     }).execute()

#     return result.data

def like_post(post_id: int):
    global current_user
    if not current_user:
        return {"error": "User not logged in"}

    existing_like = sb.table("likes").select("*")\
        .eq("user_id", current_user["id"])\
        .eq("post_id", post_id).execute()

    if existing_like.data:
        return {"error": "Post already liked"}

    result = sb.table("likes").insert({
        "user_id": current_user["id"],
        "post_id": post_id
    }).execute()

    return result.data



def unlike_post(post_id: int):
    global current_user
    if not current_user:
        return {"error": "User not logged in"}

    result = sb.table("likes").delete().match({
        "user_id": current_user["id"], 
        "post_id": post_id
    }).execute()

    return {"message": "Unliked successfully"}

def comment_post(post_id: int, content: str):
    global current_user
    if not current_user:
        return {"error": "User not logged in"}

    result = sb.table("comments").insert({
        "user_id": current_user["id"],  
        "post_id": post_id,
        "content": content
    }).execute()

    return result.data

def get_posts():
    result = sb.table("posts").select("*").execute()
    return result.data

def get_post_by_id(post_id: int):
    result = sb.table("posts").select("*").eq("id", post_id).execute()
    return result.data

