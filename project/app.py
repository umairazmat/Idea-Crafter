import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # Load the API key from .env
    base_url=os.getenv("OPENAI_API_BASE"),  # Load the base URL from .env
)

# Function to get GPT-4o Mini response
def get_gpt4o_mini_response(prompt, max_tokens=200):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",  # Adjust the model name if necessary
            messages=[
                {"role": "system", "content": "You are an AI assistant who provides brief and innovative ideas."},
                {"role": "user", "content": f"Generate a unique business idea in 1-2 lines for the following: {prompt}"},
            ],
            max_tokens=max_tokens,
        )
        print(f"response:", response)
        return response.choices[0].message.content  # Corrected line
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
def main():
    st.title("Idea Crafter - AI-Powered Idea Generator")

    # Step-based input flow with Streamlit session state
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'user_topic' not in st.session_state:
        st.session_state.user_topic = ""
    if 'idea' not in st.session_state:
        st.session_state.idea = ""

    # Step 0: Get initial input from the user
    if st.session_state.step == 0:
        with st.form(key='initial_form'):
            initial_input = st.text_input("Enter the industry you're interested in or a broad topic:", key="initial_input")
            submit_initial = st.form_submit_button("Next")
        if submit_initial:
            if initial_input.strip() == "":
                st.warning("Please enter a valid topic.")
            else:
                st.session_state.user_topic = initial_input.strip()
                st.session_state.step = 1

    # Step 1: Ask for more details (problem, impact, skills, platform)
    elif st.session_state.step == 1:
        with st.form(key='followup_form'):
            problem = st.text_input(f"What problem do you want to solve in the field of '{st.session_state.user_topic}'?")
            impact = st.text_input("What impact do you want to create?")
            skills = st.text_input("What skills do you need to learn?")
            platform = st.text_input("What platforms/tools do you think you'll need?")

            submit_followup = st.form_submit_button("Generate Idea")
        if submit_followup:
            if any(input_field.strip() == "" for input_field in [problem, impact, skills, platform]):
                st.warning("Please fill in all fields.")
            else:
                prompt = (
                    f"I want to work in {st.session_state.user_topic}, solve the problem of {problem}, "
                    f"create an impact on {impact}, and learn {skills}. I will mainly use {platform}."
                )
                # Store the prompt for the next step
                st.session_state.prompt = prompt
                st.session_state.step = 2

    # Step 2: Generate the business idea
    elif st.session_state.step == 2:
        if st.session_state.idea == "":
            with st.spinner("Generating your unique idea..."):
                idea = get_gpt4o_mini_response(st.session_state.prompt)
                st.session_state.idea = idea.strip()  # Remove any extra whitespace

        st.success("**Your Unique Idea:**")
        st.write(st.session_state.idea)

        # Option to restart the process and generate another idea
        if st.button("Generate Another Idea"):
            st.session_state.step = 0
            st.session_state.user_topic = ""
            st.session_state.idea = ""

if __name__ == "__main__":
    main()

