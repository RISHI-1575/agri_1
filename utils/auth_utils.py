import pandas as pd
import os

USER_FILE = "data/users.csv"

def load_users():
    if not os.path.exists(USER_FILE):
        users_df = pd.DataFrame(columns=["username", "password", "role"])
        users_df.to_csv(USER_FILE, index=False)
    else:
        users_df = pd.read_csv(USER_FILE)
    return users_df

def save_users(users_df):
    users_df.to_csv(USER_FILE, index=False)

def validate_login(username, password, role):
    users = load_users()
    user_match = users[
        (users["username"] == username) &
        (users["password"] == password) &
        (users["role"] == role)
    ]
    return not user_match.empty

def register_user(username, password, role):
    users = load_users()
    if username in users["username"].values:
        return "⚠️ Username already exists."
    elif not username or not password:
        return "⚠️ Please fill in all fields."
    else:
        new_entry = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])
        users = pd.concat([users, new_entry], ignore_index=True)
        save_users(users)
        return "🎉 Account created!"
