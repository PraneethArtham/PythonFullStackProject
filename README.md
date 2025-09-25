## Social Media Platform

A social media platform built using Python (Flask) and Supabase to manage authentication, real-time interactions, and data storage. This project allows users to create profiles, post content, interact with posts (comments, likes), and follow other users.

## Features:
User Registration & Authentication: Using Supabase to handle sign-ups, logins, and user management.
Profile Management: Users can create and manage their profiles.
Post Creation: Users can create posts with or without images.
Real-Time Updates: New posts, comments, and likes are updated in real-time.
Follow System: Users can follow and unfollow each other to see posts from followed users in their feed.
Comment & Like System: Users can interact with posts via likes and comments.
Admin Role: Admins can manage the users and moderate content.

## Tech Stack:
Backend: Python, Flask
Database: Supabase (PostgreSQL)
Authentication: Supabase Auth
Real-Time: Supabase Real-Time
Frontend: HTML, CSS, JavaScript


## File Structure:

PYTHONFULLSTACKPROJECT/
|
|--src/
|   |--logic.py  #logic and task
|   |--db.py #database related
|
|--API/  #backend api
|   |--main.py #fastapi
|
|--frontend/  #frontend application
|   |--app.py  #streamlit web interface
|
|__requirements.txt #install python dependicies
|
|__README.md #project documentation
|
|__.env     #python variables    


## Quick Start

### prerequisties

--Python 3.8 or higher
--Supabase Account
--Git(push,cloning)


## 1.Clone or Download Project

# option1 :clone-->git clone <repo-name>

# 2.install dependicies 

# install all requirements --> pip install -r requirements.txt

# 3.set your  supabase database

# 4.Get your credentials

1. create a .env file 

2. add supabase credentials to your .env file:
url="supabase_url"
key="supabase_key"


# Key Components

1. ## 'src/db.py'-->database operations and handle all crud operations
2. ## 'src/logic.py'-->business logic and task validation and processing

## troubleshooting

##  common issues

1. **Module not found error**-->Make sure you installed all dependicies


## support
 if you encounter any issues or have questions :
 Contact details:9059222978
 mail id:arthampraneeth977@gmail.com


 
