import openai
import streamlit as st

# Set OpenAI API key reading from a file and set default model

openai.api_key = "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"
openai_model = "gpt-3.5-turbo"

st.title("OpenAI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat historyp
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=openai_model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})