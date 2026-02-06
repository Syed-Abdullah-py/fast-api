from fastapi import FastAPI, HTTPException
from starlette import status

app = FastAPI()

text_posts = {
    1: {
        "title": "Welcome",
        "content": "Welcome to the platform"
    },
    2: {
        "title": "Announcement",
        "content": "We are excited to share an update"
    },
    3: {
        "title": "Getting Started",
        "content": "Here is how you can begin using the app"
    },
    4: {
        "title": "Feature Highlight",
        "content": "This feature helps improve productivity"
    },
    5: {
        "title": "Tips and Tricks",
        "content": "Use shortcuts to save time"
    },
    6: {
        "title": "Maintenance Update",
        "content": "The system will be under maintenance tonight"
    },
    7: {
        "title": "Bug Fixes",
        "content": "Several issues have been resolved"
    },
    8: {
        "title": "Performance Update",
        "content": "Application performance has been improved"
    },
    9: {
        "title": "Community Post",
        "content": "Thanks for being part of our community"
    },
    10: {
        "title": "Closing Note",
        "content": "Stay tuned for more updates"
    }
}

# MAIN / (ROOT)
app.get("/")

# QUERY PARAMETER
@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

# PATH PARAMETER
@app.get("/posts/{post_id}")
def get_post(post_id: int=None):
    if 0 < post_id < len(text_posts):
        return text_posts.get(post_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")