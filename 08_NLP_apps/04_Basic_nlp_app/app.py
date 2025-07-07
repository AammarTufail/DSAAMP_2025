import streamlit as st
from openai import OpenAI
import os

st.title('🦜🔗 Quickstart App')

# Use environment variable or sidebar input for API key (more secure)
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password') or os.getenv('OPENAI_API_KEY')

def generate_response(input_text):
  try:
    client = OpenAI(api_key=openai_api_key)
    response = client.completions.create(
      model="gpt-3.5-turbo-instruct",
      prompt=input_text,
      max_tokens=500,
      temperature=0.7
    )
    st.info(response.choices[0].text.strip())
  except Exception as e:
    st.error(f"Error: {str(e)}")

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key or not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key and openai_api_key.startswith('sk-'):
    generate_response(text)