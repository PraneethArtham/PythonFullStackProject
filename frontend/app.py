import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

# --------------------------
# Backend API helpers
# --------------------------
def signup(username, password, role="user"):
    return requests.post(f"{BASE_URL}/signup", json={
        "username": username,
        "password": password,
        "role": role
    }).json()

def login(username, password):
    return requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    }).json()

def create_post(content, image_url=""):
    return requests.post(f"{BASE_URL}/posts", json={
        "content": content,
        "image_url": image_url
    }).json()

def get_posts():
    return requests.get(f"{BASE_URL}/posts").json()

def like_post(post_id):
    return requests.post(f"{BASE_URL}/posts/like", json={"post_id": post_id}).json()

def unlike_post(post_id):
    return requests.post(f"{BASE_URL}/posts/unlike", json={"post_id": post_id}).json()

def comment_post(post_id, content):
    return requests.post(f"{BASE_URL}/posts/comment", json={
        "post_id": post_id,
        "content": content
    }).json()

# -------------------------------
# Streamlit UI Config
# -------------------------------
st.set_page_config(page_title="Social Media App", page_icon="🌐", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .google-box {
        width: 400px;
        margin: auto;
        margin-top: 50px;
        background: white;
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    .signup-link {
        margin-top: 20px;
        font-size: 14px;
    }
    .signup-link a {
        color: #4285F4;
        font-weight: bold;
        text-decoration: none;
        cursor: pointer;
    }
    .top-right-nav {
        position: absolute;
        top: 20px;
        right: 30px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "Login"  # default = Login page

# -------------------------------
# Navigation (only visible after login)
# -------------------------------
if st.session_state.username:
    nav_placeholder = st.empty()
    with nav_placeholder.container():
        st.markdown('<div class="top-right-nav">', unsafe_allow_html=True)
        if st.button("📢 Home"):
            st.session_state.page = "Home"
        if st.button("📝 Signup"):
            st.session_state.page = "Signup"
        if st.button("🔒 Logout"):
            st.session_state.username = None
            st.session_state.page = "Login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Pages
# -------------------------------

# Login Page
if st.session_state.page == "Login" and not st.session_state.username:
    st.markdown('<div class="main-title">🌐 Social Media Platform</div>', unsafe_allow_html=True)
    #st.markdown('<div class="google-box">', unsafe_allow_html=True)
    st.subheader("Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            result = login(username, password)
            if "message" in result:
                st.session_state.username = username
                st.session_state.page = "Home"   # directly go home
                st.rerun()
            else:
                st.error(result.get("detail", "Login failed"))
        else:
            st.error("Please enter both username and password")
    if st.button("New user? Signup"):
        st.session_state.page = "Signup"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Signup Page
elif st.session_state.page == "Signup" and not st.session_state.username:
  #  st.markdown('<div class="google-box">', unsafe_allow_html=True)
    st.subheader("Create an Account")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    if st.button("Signup"):
        if username and password:
            result = signup(username, password)
            st.success(result.get("message", result))
        else:
            st.error("Please fill all fields")
    if st.button("Back to Login"):
        st.session_state.page = "Login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Home Page
elif st.session_state.page == "Home":
    if not st.session_state.username:
        st.warning("You must login first")
    else:
        st.markdown(f"<h2>Welcome {st.session_state.username} 🎉</h2>", unsafe_allow_html=True)

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
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"**{post['content']}**")
                    if post.get("image_url"):
                        st.image(post["image_url"], width=300, caption="Post Image")
                    st.write(f"👍 {post.get('like_count', 0)} Likes")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Like {post['id']}", key=f"like_{post['id']}"):
                            like_post(post["id"])
                            st.rerun()
                    with col2:
                        if st.button(f"Unlike {post['id']}", key=f"unlike_{post['id']}"):
                            unlike_post(post["id"])
                            st.rerun()

                    with st.expander("💬 Comments"):
                        for c in post.get("comments", []):
                            st.write(f"- {c['content']}")
                        comment_text = st.text_input("Add a comment", key=f"comment_{post['id']}")
                        if st.button("Comment", key=f"comment_btn_{post['id']}"):
                            if comment_text:
                                comment_post(post["id"], comment_text)
                                st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No posts yet. Be the first one!")
