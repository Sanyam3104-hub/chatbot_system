import streamlit as st
import requests

st.title("Mini Chatbot")

# Backend endpoint
backend_url = "http://127.0.0.1:8000/chat"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input.strip():
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Send request to backend
        try:
            response = requests.post(backend_url, json={"messages": st.session_state["messages"]})
            if response.status_code == 200:
                data = response.json()
                # Extract text
                if "choices" in data:
                    reply = data["choices"][0]["message"]["content"]
                    st.session_state["messages"].append({"role": "assistant", "content": reply})
                else:
                    st.error(data.get("error", "Unknown error"))
            else:
                st.error(f"Backend error: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")

# Display chat
for msg in st.session_state["messages"]:
    st.write(f"**{msg['role']}**: {msg['content']}")
