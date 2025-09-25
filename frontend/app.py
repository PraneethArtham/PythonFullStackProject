import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

def signup(username, password, role="user"):
    response = requests.post(f"{BASE_URL}/signup", json={
        "username": username,
        "password": password,
        "role": role
    })
    return response.json()

def login(username, password):
    response = requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })
    return response.json()

def create_post(content, image_url=""):
    response = requests.post(f"{BASE_URL}/posts", json={
        "content": content,
        "image_url": image_url
    })
    return response.json()

def get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    return response.json()

def like_post(post_id):
    response = requests.post(f"{BASE_URL}/posts/like", json={"post_id": post_id})
    return response.json()

def unlike_post(post_id):
    response = requests.post(f"{BASE_URL}/posts/unlike", json={"post_id": post_id})
    return response.json()

def comment_post(post_id, content):
    response = requests.post(f"{BASE_URL}/posts/comment", json={
        "post_id": post_id,
        "content": content
    })
    return response.json()

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Social Media App", page_icon="🌐", layout="centered")

st.title("🌐 Social Media Platform")

# Sidebar menu
menu = ["Signup", "Login", "Home"]
choice = st.sidebar.radio("Navigation", menu)

# Track session state (logged in user)
if "username" not in st.session_state:
    st.session_state.username = None

# -------------------------------
# Signup Page
# -------------------------------
if choice == "Signup":
    st.subheader("Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if username and password:
            result = signup(username, password)
            st.success(result.get("message", result))
        else:
            st.error("Please fill all fields")

# -------------------------------
# Login Page
# -------------------------------
elif choice == "Login":
    st.subheader("Login to your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            result = login(username, password)
            if "message" in result:
                st.session_state.username = username
                st.success(f"Welcome {username} 👋")
            else:
                st.error(result.get("detail", "Login failed"))
        else:
            st.error("Please enter both username and password")

# -------------------------------
# Home Page
# -------------------------------
elif choice == "Home":
    if not st.session_state.username:
        st.warning("You must login first")
    else:
        st.subheader(f"Welcome {st.session_state.username} 🎉")

        # Create Post
        with st.expander("➕ Create a Post"):
            content = st.text_area("What's on your mind?")
            image_url = st.text_input("Image URL (optional)")
            if st.button("Post"):
                result = create_post(content, image_url)
                st.success(result.get("message", "Post created"))

        # Display Posts
        st.subheader("📢 All Posts")
        posts_data = get_posts()
        posts = posts_data.get("posts", [])

        if posts:
            for post in posts:
                st.markdown(f"**{post['content']}**")
                if post.get("image_url"):
                    st.image(post["image_url"], width=250)
                st.write(f"👍 {post.get('like_count', 0)} Likes")

                # Like / Unlike
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Like {post['id']}", key=f"like_{post['id']}"):
                        like_post(post["id"])
                        st.experimental_rerun()
                with col2:
                    if st.button(f"Unlike {post['id']}", key=f"unlike_{post['id']}"):
                        unlike_post(post["id"])
                        st.experimental_rerun()

                # Comments
                with st.expander("💬 Comments"):
                    for c in post.get("comments", []):
                        st.write(f"- {c['content']}")
                    comment_text = st.text_input("Add a comment", key=f"comment_{post['id']}")
                    if st.button("Comment", key=f"comment_btn_{post['id']}"):
                        if comment_text:
                            comment_post(post["id"], comment_text)
                            st.experimental_rerun()

                st.markdown("---")
        else:
            st.info("No posts yet. Be the first one!")
