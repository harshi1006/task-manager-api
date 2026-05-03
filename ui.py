import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

st.title("✅ Task Manager")
st.write("Manage your tasks easily!")


st.header("📋 All Tasks")

response = requests.get(f"{BASE_URL}/tasks")
tasks = response.json()

for task in tasks:
    col1, col2 = st.columns([6, 2])

    with col1:
        if task["done"]:
            st.success(f"✅ {task['title']}")
        else:
            st.warning(f"⏳ {task['title']}")

    with col2:
        btn1, btn2 = st.columns(2)
        with btn1:
            if not task["done"]:
                if st.button("✅ Done", key=f"done_{task['id']}", use_container_width=True):
                    requests.put(
                        f"{BASE_URL}/tasks/{task['id']}",
                        json={"done": True}
                    )
                    st.rerun()
        with btn2:
            if st.button("🗑️ Delete", key=f"delete_{task['id']}", use_container_width=True):
                requests.delete(f"{BASE_URL}/tasks/{task['id']}")
                st.rerun()

st.header("➕ Add New Task")

new_task = st.text_input("Task title")

if st.button("Add Task"):
    if new_task.strip() == "":
        st.error("Please enter a task title!")
    else:
        response = requests.post(
            f"{BASE_URL}/tasks",
            json={"title": new_task}
        )
        if response.status_code == 201:
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.error("Something went wrong!")

