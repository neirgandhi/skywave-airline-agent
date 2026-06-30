import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

with open("faq.md", "r") as f:
    faq_content = f.read()

st.title("SkyWave Airlines Customer Service")
st.caption("Ask me anything about baggage, check-in, flight changes, seats, and more.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"""You are a helpful customer service agent for SkyWave Airlines.
Answer questions using only the information in the FAQ below.
If a question is not covered in the FAQ, respond with:
I don't have information on that. I'm escalating your query to a human agent who will follow up shortly. You can also reach us at support@skywave.com or call 1-800-SKY-WAVE.
If a customer expresses frustration, respond with:
I'm sorry to hear that. I'm escalating your case to a human agent right away. You will be contacted within 24 hours.
Be friendly, concise, and professional.

FAQ:
{faq_content}"""}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
