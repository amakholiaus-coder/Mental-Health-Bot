import openai
import streamlit as st

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app UI setup
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠")
st.title("🧠 Mental Health Chatbot")
st.write("Hi, I’m here to support you. You can talk to me about anything.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Get user input
if prompt := st.chat_input("How are you feeling today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Generate assistant reply using GPT-4
    with st.spinner("Thinking..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a warm, empathetic mental health support bot. Respond with emotional intelligence. Be supportive, non-judgmental, and deeply human. Never give medical or emergency advice."},
                    *st.session_state.messages
                ]
            )
            reply = response.choices[0].message["content"]
        except Exception as e:
            reply = "I'm sorry, something went wrong. Please try again later."
            print("Error:", e)

        # Show and save assistant reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)
