import streamlit as st
import PyPDF2
from PyPDF2 import PdfReader
import google.generativeai as genai

def retrieve_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""  # Safely handle None return
        return text
    except FileNotFoundError:
        st.error("The specified PDF file was not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred while reading the PDF: {e}")
        return None

def main():
    # CSS for styling
    custom_css = """
    <style>
        .title { color: #ff6347; }  /* Red */
        .text { color: #4682b4; }   /* Steel Blue */
        .button { background-color: #98fb98; color: black; }  /* Pale Green background with Black text for button */
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # PDF Path
    pdf = "Rag.pdf"
    model = "gemini-1.5-pro-latest"

    try:
        with open("api_key.txt", "r") as file:
            key = file.read().strip()
        genai.configure(api_key=key)
    except FileNotFoundError:
        st.error("API key file not found.")
        return
    except Exception as e:
        st.error(f"An error occurred while configuring the AI model: {e}")
        return

    st.markdown('<h1 class="title">💻A RAG System on “Leave No Context Behind” Paper📰</h1>', unsafe_allow_html=True)
    question = st.text_input("What would you like to know?", key='1')  # Added key for uniqueness

    if st.button("Generate", key='2'):  # Added key for uniqueness
        if question:
            text = retrieve_text_from_pdf(pdf)
            if text is not None:  # Ensure text was successfully retrieved
                context = text + "\n\n" + question
                try:
                    ai = genai.GenerativeModel(model_name=model)
                    response = ai.generate_content(context)
                    st.markdown(f'<h2 class="text">Question:</h2>', unsafe_allow_html=True)
                    st.markdown(f'<p class="text">{question}</p>', unsafe_allow_html=True)
                    st.markdown('<h2 class="text">Answer:</h2>', unsafe_allow_html=True)
                    st.markdown(f'<p class="text">{response.text}</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Failed to generate content: {e}")
        else:
            st.warning("Please enter your question.")

if __name__ == "__main__":
    main()
