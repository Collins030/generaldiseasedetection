import streamlit as st
import mysql.connector
import datetime
import io
import base64
import time


# Database connection
def get_database_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Default XAMPP password is blank
        database="farmers_forum"
    )
    return conn


# Initialize database if it doesn't exist
def init_db():
    # Connect to MySQL server without specifying database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS farmers_forum")
    conn.commit()
    conn.close()

    # Connect to the created database
    conn = get_database_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        profile_pic LONGBLOB,
        bio TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_online DATETIME,
        is_online BOOLEAN DEFAULT FALSE
    )
    """)

    # Create posts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        post_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        image LONGBLOB,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """)

    # Create comments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        comment_id INT AUTO_INCREMENT PRIMARY KEY,
        post_id INT NOT NULL,
        user_id INT NOT NULL,
        parent_id INT DEFAULT NULL,
        content TEXT NOT NULL,
        image LONGBLOB,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (parent_id) REFERENCES comments(comment_id) ON DELETE CASCADE
    )
    """)

    # Create votes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        vote_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        post_id INT DEFAULT NULL,
        comment_id INT DEFAULT NULL,
        vote_type ENUM('upvote', 'downvote') NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE,
        CONSTRAINT unique_post_vote UNIQUE(user_id, post_id),
        CONSTRAINT unique_comment_vote UNIQUE(user_id, comment_id)
    )
    """)

    conn.commit()
    conn.close()


# Initialize session state variables
def init_session_state():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
    if 'profile_pic' not in st.session_state:
        st.session_state.profile_pic = None
    if 'online_users' not in st.session_state:
        st.session_state.online_users = {}
    if 'show_comments' not in st.session_state:
        st.session_state.show_comments = {}


# User Authentication Functions
def register_user(username, password, email, profile_pic=None):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        # Convert image to binary if provided
        profile_pic_binary = None
        if profile_pic is not None:
            profile_pic_binary = profile_pic.getvalue()

        # Insert user into database
        cursor.execute(
            "INSERT INTO users (username, password, email, profile_pic) VALUES (%s, %s, %s, %s)",
            (username, password, email, profile_pic_binary)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            # Update user's online status
            cursor.execute(
                "UPDATE users SET is_online = TRUE, last_online = NOW() WHERE user_id = %s",
                (user['user_id'],)
            )
            conn.commit()

            # Set session state
            st.session_state.user_id = user['user_id']
            st.session_state.username = user['username']
            st.session_state.is_logged_in = True

            # Set profile picture if exists
            if user['profile_pic']:
                st.session_state.profile_pic = user['profile_pic']

            return True
        else:
            return False
    finally:
        conn.close()


def logout_user():
    if st.session_state.is_logged_in:
        conn = get_database_connection()
        cursor = conn.cursor()

        try:
            # Update user's online status
            cursor.execute(
                "UPDATE users SET is_online = FALSE, last_online = NOW() WHERE user_id = %s",
                (st.session_state.user_id,)
            )
            conn.commit()
        finally:
            conn.close()

    # Clear session state
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_logged_in = False
    st.session_state.profile_pic = None


# Post Functions
def create_post(title, content, image=None):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        # Convert image to binary if provided
        image_binary = None
        if image is not None:
            image_binary = image.getvalue()

        # Insert post into database
        cursor.execute(
            "INSERT INTO posts (user_id, title, content, image) VALUES (%s, %s, %s, %s)",
            (st.session_state.user_id, title, content, image_binary)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return False
    finally:
        conn.close()


def get_posts():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
        SELECT p.*, u.username, u.profile_pic, u.is_online,
               (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.post_id) AS comment_count,
               (SELECT COUNT(*) FROM votes v WHERE v.post_id = p.post_id AND v.vote_type = 'upvote') AS upvotes,
               (SELECT COUNT(*) FROM votes v WHERE v.post_id = p.post_id AND v.vote_type = 'downvote') AS downvotes
        FROM posts p
        JOIN users u ON p.user_id = u.user_id
        ORDER BY p.created_at DESC
        """)
        return cursor.fetchall()
    finally:
        conn.close()


# Comment Functions
def add_comment(post_id, content, parent_id=None, image=None):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        # Convert image to binary if provided
        image_binary = None
        if image is not None:
            image_binary = image.getvalue()

        # Insert comment into database
        cursor.execute(
            "INSERT INTO comments (post_id, user_id, parent_id, content, image) VALUES (%s, %s, %s, %s, %s)",
            (post_id, st.session_state.user_id, parent_id, content, image_binary)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return False
    finally:
        conn.close()


def get_comments(post_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
        SELECT c.*, u.username, u.profile_pic, u.is_online,
               (SELECT COUNT(*) FROM votes v WHERE v.comment_id = c.comment_id AND v.vote_type = 'upvote') AS upvotes,
               (SELECT COUNT(*) FROM votes v WHERE v.comment_id = c.comment_id AND v.vote_type = 'downvote') AS downvotes
        FROM comments c
        JOIN users u ON c.user_id = u.user_id
        WHERE c.post_id = %s
        ORDER BY c.parent_id IS NULL DESC, c.created_at ASC
        """, (post_id,))
        return cursor.fetchall()
    finally:
        conn.close()


# Vote Functions
def vote(post_id=None, comment_id=None, vote_type='upvote'):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        # Check if user has already voted
        if post_id:
            cursor.execute(
                "SELECT * FROM votes WHERE user_id = %s AND post_id = %s",
                (st.session_state.user_id, post_id)
            )
        else:
            cursor.execute(
                "SELECT * FROM votes WHERE user_id = %s AND comment_id = %s",
                (st.session_state.user_id, comment_id)
            )

        existing_vote = cursor.fetchone()

        if existing_vote:
            # Update existing vote
            if post_id:
                cursor.execute(
                    "UPDATE votes SET vote_type = %s WHERE user_id = %s AND post_id = %s",
                    (vote_type, st.session_state.user_id, post_id)
                )
            else:
                cursor.execute(
                    "UPDATE votes SET vote_type = %s WHERE user_id = %s AND comment_id = %s",
                    (vote_type, st.session_state.user_id, comment_id)
                )
        else:
            # Create new vote
            cursor.execute(
                "INSERT INTO votes (user_id, post_id, comment_id, vote_type) VALUES (%s, %s, %s, %s)",
                (st.session_state.user_id, post_id, comment_id, vote_type)
            )

        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return False
    finally:
        conn.close()


def remove_vote(post_id=None, comment_id=None):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        # Delete vote
        if post_id:
            cursor.execute(
                "DELETE FROM votes WHERE user_id = %s AND post_id = %s",
                (st.session_state.user_id, post_id)
            )
        else:
            cursor.execute(
                "DELETE FROM votes WHERE user_id = %s AND comment_id = %s",
                (st.session_state.user_id, comment_id)
            )

        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return False
    finally:
        conn.close()


def get_user_vote(post_id=None, comment_id=None):
    if not st.session_state.is_logged_in:
        return None

    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if post_id:
            cursor.execute(
                "SELECT vote_type FROM votes WHERE user_id = %s AND post_id = %s",
                (st.session_state.user_id, post_id)
            )
        else:
            cursor.execute(
                "SELECT vote_type FROM votes WHERE user_id = %s AND comment_id = %s",
                (st.session_state.user_id, comment_id)
            )

        result = cursor.fetchone()
        return result['vote_type'] if result else None
    finally:
        conn.close()


# Get online users
def get_online_users():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
        SELECT user_id, username, profile_pic
        FROM users
        WHERE is_online = TRUE
        """)
        return cursor.fetchall()
    finally:
        conn.close()


# Convert binary to image
def get_image_base64(binary_data):
    if binary_data:
        return base64.b64encode(binary_data).decode('utf-8')
    return None


# UI Components
def user_avatar(profile_pic, is_online=False, size=40):
    if profile_pic:
        img_base64 = get_image_base64(profile_pic)
        online_indicator = "🟢" if is_online else ""
        return f"""
        <div style="position: relative; display: inline-block; margin-right: 10px;">
            <img src="data:image/png;base64,{img_base64}" style="width: {size}px; height: {size}px; border-radius: 50%; object-fit: cover;">
            <span style="position: absolute; bottom: 0; right: 0;">{online_indicator}</span>
        </div>
        """
    else:
        online_indicator = "🟢" if is_online else ""
        return f"""
        <div style="position: relative; display: inline-block; margin-right: 10px;">
            <div style="width: {size}px; height: {size}px; border-radius: 50%; background-color: #ccc; display: flex; justify-content: center; align-items: center;">
                <span style="font-size: {size // 2}px;">👤</span>
            </div>
            <span style="position: absolute; bottom: 0; right: 0;">{online_indicator}</span>
        </div>
        """


def format_time(dt):
    now = datetime.datetime.now()
    delta = now - dt

    if delta.days == 0:
        if delta.seconds < 60:
            return "just now"
        elif delta.seconds < 3600:
            return f"{delta.seconds // 60} minutes ago"
        else:
            return f"{delta.seconds // 3600} hours ago"
    elif delta.days == 1:
        return "yesterday"
    else:
        return dt.strftime("%b %d, %Y")



def display_post_card(post):
    col1, col2 = st.columns([1, 6])

    with col1:
        st.markdown(user_avatar(post['profile_pic'], post['is_online']), unsafe_allow_html=True)

    with col2:
        st.markdown(f"**{post['username']}** • {format_time(post['created_at'])}")

    st.markdown(f"## {post['title']}")
    st.markdown(post['content'])

    if post['image']:
        img_base64 = get_image_base64(post['image'])
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" style="max-width: 100%; max-height: 400px;">',
                    unsafe_allow_html=True)

    # Vote buttons and comment count
    col1, col2, col3, col4 = st.columns([1, 1, 1, 10])

    user_vote = get_user_vote(post_id=post['post_id'])

    with col1:
        upvote_color = "green" if user_vote == "upvote" else "gray"
        if st.button(f"👍 {post['upvotes']}", key=f"upvote_{post['post_id']}"):
            if st.session_state.is_logged_in:
                if user_vote == "upvote":
                    remove_vote(post_id=post['post_id'])
                else:
                    vote(post_id=post['post_id'], vote_type="upvote")
                st.rerun()
            else:
                st.warning("Please log in to vote")

    with col2:
        downvote_color = "red" if user_vote == "downvote" else "gray"
        if st.button(f"👎 {post['downvotes']}", key=f"downvote_{post['post_id']}"):
            if st.session_state.is_logged_in:
                if user_vote == "downvote":
                    remove_vote(post_id=post['post_id'])
                else:
                    vote(post_id=post['post_id'], vote_type="downvote")
                st.rerun()
            else:
                st.warning("Please log in to vote")

    with col3:
        comment_key = f"show_comments_{post['post_id']}"
        if comment_key not in st.session_state.show_comments:
            st.session_state.show_comments[comment_key] = False

        if st.button(f"💬 {post['comment_count']}", key=f"comment_{post['post_id']}"):
            st.session_state.show_comments[comment_key] = not st.session_state.show_comments[comment_key]
            st.rerun()

    # Show comments
    if st.session_state.show_comments.get(f"show_comments_{post['post_id']}", False):
        comments = get_comments(post['post_id'])

        # Comment form
        if st.session_state.is_logged_in:
            with st.expander("Add Comment", expanded=False):
                comment_form(post['post_id'])

        # Display comments
        for comment in comments:
            display_comment(comment, level=0)


def display_comment(comment, level=0):
    margin_left = level * 20

    with st.container():
        st.markdown(f'<div style="margin-left: {margin_left}px; border-left: 2px solid #ccc; padding-left: 10px;">',
                    unsafe_allow_html=True)

        col1, col2 = st.columns([1, 6])

        with col1:
            st.markdown(user_avatar(comment['profile_pic'], comment['is_online'], size=30), unsafe_allow_html=True)

        with col2:
            st.markdown(f"**{comment['username']}** • {format_time(comment['created_at'])}")

        st.markdown(comment['content'])

        if comment['image']:
            img_base64 = get_image_base64(comment['image'])
            st.markdown(f'<img src="data:image/png;base64,{img_base64}" style="max-width: 100%; max-height: 200px;">',
                        unsafe_allow_html=True)

        # Vote buttons and reply button
        col1, col2, col3, col4 = st.columns([1, 1, 1, 10])

        user_vote = get_user_vote(comment_id=comment['comment_id'])

        with col1:
            upvote_color = "green" if user_vote == "upvote" else "gray"
            if st.button(f"👍 {comment['upvotes']}", key=f"upvote_comment_{comment['comment_id']}"):
                if st.session_state.is_logged_in:
                    if user_vote == "upvote":
                        remove_vote(comment_id=comment['comment_id'])
                    else:
                        vote(comment_id=comment['comment_id'], vote_type="upvote")
                    st.rerun()
                else:
                    st.warning("Please log in to vote")

        with col2:
            downvote_color = "red" if user_vote == "downvote" else "gray"
            if st.button(f"👎 {comment['downvotes']}", key=f"downvote_comment_{comment['comment_id']}"):
                if st.session_state.is_logged_in:
                    if user_vote == "downvote":
                        remove_vote(comment_id=comment['comment_id'])
                    else:
                        vote(comment_id=comment['comment_id'], vote_type="downvote")
                    st.rerun()
                else:
                    st.warning("Please log in to vote")

        with col3:
            reply_key = f"reply_{comment['comment_id']}"
            if reply_key not in st.session_state:
                st.session_state[reply_key] = False

            if st.button("↩️ Reply", key=f"reply_btn_{comment['comment_id']}"):
                if st.session_state.is_logged_in:
                    st.session_state[reply_key] = not st.session_state[reply_key]
                    st.rerun()
                else:
                    st.warning("Please log in to reply")

        # Show reply form
        if st.session_state.is_logged_in and st.session_state.get(f"reply_{comment['comment_id']}", False):
            with st.container():
                st.markdown(
                    f'<div style="margin-left: {margin_left + 20}px; border-left: 2px solid #ccc; padding-left: 10px;">',
                    unsafe_allow_html=True)
                reply_form(comment['post_id'], comment['comment_id'])
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def comment_form(post_id, parent_id=None):
    with st.form(key=f"comment_form_{post_id}_{parent_id}" if parent_id else f"comment_form_{post_id}"):
        comment_text = st.text_area("Comment", height=100)
        uploaded_file = st.file_uploader("Add Image (Optional)", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Post Comment")

        if submitted and comment_text:
            success = add_comment(post_id, comment_text, parent_id, uploaded_file)
            if success:
                st.success("Comment added successfully!")
                time.sleep(1)
                st.rerun()


def reply_form(post_id, parent_id):
    with st.form(key=f"reply_form_{parent_id}"):
        reply_text = st.text_area("Reply", height=100)
        uploaded_file = st.file_uploader("Add Image (Optional)", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Post Reply")

        if submitted and reply_text:
            success = add_comment(post_id, reply_text, parent_id, uploaded_file)
            if success:
                st.success("Reply added successfully!")
                st.session_state[f"reply_{parent_id}"] = False
                time.sleep(1)
                st.rerun()


def post_form():
    with st.form(key="post_form"):
        post_title = st.text_input("Title")
        post_content = st.text_area("Content", height=150)
        uploaded_file = st.file_uploader("Add Image (Optional)", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Create Post")

        if submitted and post_title and post_content:
            success = create_post(post_title, post_content, uploaded_file)
            if success:
                st.success("Post created successfully!")
                time.sleep(1)
                st.rerun()


def login_form():
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted and username and password:
            if login_user(username, password):
                st.success("Logged in successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")


def register_form():
    with st.form(key="register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        profile_pic = st.file_uploader("Profile Picture (Optional)", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Register")

        if submitted and username and password and email:
            if register_user(username, password, email, profile_pic):
                st.success("Registered successfully! Please log in.")
                time.sleep(1)
                st.rerun()


def show_online_users_sidebar():
    st.sidebar.title("Online Users")

    online_users = get_online_users()

    if online_users:
        for user in online_users:
            col1, col2 = st.sidebar.columns([1, 3])

            with col1:
                st.markdown(user_avatar(user['profile_pic'], True, size=30), unsafe_allow_html=True)

            with col2:
                st.markdown(f"**{user['username']}**")
    else:
        st.sidebar.markdown("No users online")


# Main Community Page Function
def community_page():
    # Initialize database and session state
    init_db()
    init_session_state()

    st.header("🌱 Farmers Community Forum")
    st.write("Discuss crop diseases, farming techniques, and connect with other farmers")

    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .post-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Authentication header
    col1, col2 = st.columns([6, 1])

    with col2:
        if st.session_state.is_logged_in:
            if st.button("Logout"):
                logout_user()
                st.rerun()

    # Sidebar - Authentication and Online Users
    if not st.session_state.is_logged_in:
        with st.sidebar:
            tab1, tab2 = st.tabs(["Login", "Register"])

            with tab1:
                login_form()

            with tab2:
                register_form()
    else:
        # Show user profile in sidebar
        with st.sidebar:
            st.markdown(f"### Welcome, {st.session_state.username}!")
            if st.session_state.profile_pic:
                img_base64 = get_image_base64(st.session_state.profile_pic)
                st.markdown(
                    f'<img src="data:image/png;base64,{img_base64}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover;">',
                    unsafe_allow_html=True)

        # Show online users
        show_online_users_sidebar()

    # Main content
    tab1, tab2 = st.tabs(["Feed", "Create Post"])

    with tab1:
        posts = get_posts()

        for post in posts:
            with st.container():
                st.markdown('<div class="post-card">', unsafe_allow_html=True)
                display_post_card(post)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)

    with tab2:
        if st.session_state.is_logged_in:
            post_form()
        else:
            st.warning("Please log in to create a post")


# For testing directly
if __name__ == "__main__":
    community_page()