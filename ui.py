import streamlit as st
import requests

BASE_URL = "https://harshita1006.pythonanywhere.com"

st.set_page_config(page_title="Task Manager", page_icon="✅")
st.title("✅ Task Manager")


# --- 1. FETCH DATA ---
try:
    response = requests.get(f"{BASE_URL}/tasks")
    tasks = response.json()
except Exception as e:
    st.error("Could not connect to Backend. Make sure your Flask app is running!")
    tasks = []

# --- 2. ADD NEW TASK ---

# --- 1. INITIALIZE STATE ---
if "expander_open" not in st.session_state:
    st.session_state.expander_open = True
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

# --- 2. THE EXPANDER ---
# We use st.session_state.expander_open here
with st.expander("➕ Add New Task", expanded=st.session_state.expander_open):

    input_key = f"task_input_{st.session_state.input_counter}"
    new_task_title = st.text_input("What needs to be done?", key=input_key)

    if st.button("Submit Task", use_container_width=True):
        if new_task_title.strip():
            response = requests.post(f"{BASE_URL}/tasks", json={"title": new_task_title})

            if response.status_code == 201:
                # SUCCESS ACTIONS:
                st.session_state.input_counter += 1 # Clears the text box
                st.session_state.expander_open = False # Closes the box
                st.toast(f"✅ Added: {new_task_title}")
                st.rerun()
            else:
                st.error("Backend error.")
        else:
            st.error("Title cannot be empty!")

# --- 3. THE RESET (CRITICAL FIX) ---
# After the script runs once and closes the expander (via rerun),
# we reset the variable to True so that the NEXT time the user
# clicks the header manually, it doesn't try to force it shut.
if st.session_state.expander_open == False:
    st.session_state.expander_open = True
st.divider()

# --- 3. DISPLAY TASKS ---
st.header("📋 My Tasks")

if not tasks:
    st.info("✨ Your list is empty. Add your first todo above!")
else:
    for task in tasks:
        # Create a unique key for session state to track if we are editing this specific task
        edit_mode_key = f"edit_mode_{task['id']}"
        if edit_mode_key not in st.session_state:
            st.session_state[edit_mode_key] = False

        # --- TASK ROW ---
        with st.container(border=True):
            if st.session_state[edit_mode_key]:
                # EDIT UI
                new_title = st.text_input("Edit Task", value=task['title'], key=f"input_{task['id']}")
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 Save", key=f"save_{task['id']}", use_container_width=True):
                        requests.put(f"{BASE_URL}/tasks/{task['id']}", json={"title": new_title})
                        st.session_state[edit_mode_key] = False
                        st.rerun()
                with col_cancel:
                    if st.button("❌ Cancel", key=f"cancel_{task['id']}", use_container_width=True):
                        st.session_state[edit_mode_key] = False
                        st.rerun()
            else:
                # DISPLAY UI
                col1, col2 = st.columns([5, 3])

                with col1:
                    status_prefix = "✅" if task["done"] else "⏳"
                    # Add strikethrough if done
                    display_text = f"~~{task['title']}~~" if task["done"] else task['title']
                    st.markdown(f"### {status_prefix} {display_text}")

                with col2:
                    btn_done, btn_edit, btn_del = st.columns(3)
                    with btn_done:
                        # Toggle Done/Undo
                        icon = "↩️" if task["done"] else "✔️"
                        if st.button(icon, key=f"done_{task['id']}", help="Mark as Done"):
                            requests.put(f"{BASE_URL}/tasks/{task['id']}", json={"done": not task["done"]})
                            st.rerun()
                    with btn_edit:
                        if st.button("✏️", key=f"btn_edit_{task['id']}", help="Edit Title"):
                            st.session_state[edit_mode_key] = True
                            st.rerun()
                    with btn_del:
                        if st.button("🗑️", key=f"del_{task['id']}", help="Delete Task"):
                            requests.delete(f"{BASE_URL}/tasks/{task['id']}")
                            st.rerun()
