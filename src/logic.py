from src.db import DatabaseManager

class SocialMediaPlatform:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None  # track logged-in user

    # ----------------------
    # User Authentication
    # ----------------------
    def signup(self, username: str, password: str, role: str = "user"):
        result = self.db.signup(username, password, role)
        return result

    def login(self, username: str, password: str):
        result = self.db.login(username, password)
        if "error" not in result:
            self.current_user = self.db.current_user  # track logged-in user
        return result

    def get_current_user(self):
        return self.current_user
    def create_post(self, content: str, image_url: str = ""):
        if not self.current_user:
            return {"error": "User not logged in"}
        return self.db.create_post(content, image_url)

    def like_post(self, post_id: int):
        if not self.current_user:
            return {"error": "User not logged in"}
        return self.db.like_post(post_id)

    def unlike_post(self, post_id: int):
        if not self.current_user:
            return {"error": "User not logged in"}
        return self.db.unlike_post(post_id)

    def comment_post(self, post_id: int, content: str):
        if not self.current_user:
            return {"error": "User not logged in"}
        return self.db.comment_post(post_id, content)
