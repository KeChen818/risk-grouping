import streamlit as st

st.header("AI Chatbot - Inventory Expert")

summary, chat, prompts = st.tabs(["Inventory Brief", "Chat", "Suggested Questions"])

with summary:
    st.subheader("Inventory Brief")
    st.write(
        "This chatbot is positioned as an inventory expert: it explains top exposure, quantification alignment, QoQ changes, and grouping outputs in business language."
    )

with chat:
    st.subheader("Ask about the inventory")
    question = st.text_input("Example: Which material credit risks increased QoQ?")
    if question:
        st.success(f"Demo response placeholder for: {question}")

with prompts:
    st.subheader("Suggested questions")
    st.write("- Show the top exposure for CUSO credit risks.")
    st.write("- Which risks changed the most QoQ?")
    st.write("- Summarize the non-material risk watchlist.")
    st.write("- Propose common themes across market and credit risks.")
