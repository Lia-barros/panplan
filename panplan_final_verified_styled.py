
import streamlit as st

st.set_page_config(page_title="PanPlan", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap');

:root {
  color-scheme: light !important;
}
html, body, [class*="css"] {
  font-family: 'Fredoka', sans-serif;
  background-color: #CDE5FA !important;
  color: #2E4053;
}

h1, h2, h3 {
  color: #3B5998;
  text-align: center;
}

.stButton>button {
  background-color: #6B8ED6 !important;
  color: white !important;
  border-radius: 12px;
  padding: 0.5em 1em;
  font-weight: 600;
  border: none;
}

.stTextInput>div>input, .stPasswordInput>div>input {
  border-radius: 8px;
  padding: 0.5em;
  border: 1px solid #6B8ED6;
}

.stRadio>div {
  background: white;
  border-radius: 12px;
  padding: 1em;
  border: 1px solid #B0C4DE;
}

.stExpanderHeader {
  font-weight: 600;
  color: #3B5998;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center"><img src="PanPlan.png" width="120"/></div>', unsafe_allow_html=True)

st.title("Welcome to PanPlan!")
st.write("🌱 Recipe substitutions and dietary tools for everyone.")
