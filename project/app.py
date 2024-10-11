import streamlit as st
from openai_client import get_gpt4o_mini_response
from industries import industries

# Streamlit app
def main():
    st.title("Idea Crafter - AI-Powered Idea Generator")

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.update({
            'step': 0,
            'user_topics': [],
            'idea': "",
            'prompt': ""
        })

    # Optional: Display progress in sidebar
    steps = ["Select Industries", "Provide Details", "Generate Idea"]
    st.sidebar.header("Progress")
    for i, step in enumerate(steps):
        if st.session_state.step > i:
            st.sidebar.success(f"✓ {step}")
        elif st.session_state.step == i:
            st.sidebar.info(f"→ {step}")
        else:
            st.sidebar.text(step)

    # Step 0: Select Industries
    if st.session_state.step == 0:
        st.header("Select Industries You're Interested In")
        st.write("Choose one or more industries from the options below.")

        # Number of columns per row
        cols_per_row = 3

        # Calculate the number of rows needed
        num_rows = (len(industries) + cols_per_row - 1) // cols_per_row

        # Create grid layout
        for row in range(num_rows):
            cols = st.columns(cols_per_row)
            for col_index in range(cols_per_row):
                industry_index = row * cols_per_row + col_index
                if industry_index < len(industries):
                    industry = industries[industry_index]
                    with cols[col_index]:
                        st.image(industry["image"], width=150)
                        selected = st.checkbox(industry["name"], key=f"industry_{industry_index}")

        # Submit button
        if st.button("Next"):
            # Collect selected industries
            selected = [industry["name"] for industry in industries if st.session_state.get(f"industry_{industries.index(industry)}", False)]
            if not selected:
                st.warning("Please select at least one industry.")
            else:
                st.session_state.user_topics = selected
                st.session_state.step = 1

    # Step 1: Ask for more detailed inputs
    elif st.session_state.step == 1:
        with st.form(key='detailed_form'):
            st.header("Provide More Details About Your Selected Industry")
            # Display selected industries
            st.subheader(f"Selected Industry: {', '.join(st.session_state.user_topics)}")
            problem = st.text_area("1. Can you describe the specific challenges or main points you want to address?")
            impact = st.text_area("2. What positive changes or outcomes do you hope to achieve?")
            target_audience = st.text_input("3. Who is the primary audience or beneficiaries of your idea?")
            constraints = st.text_input("4. Are there any constraints (e.g., budget, time, resources)?")
            inspirations = st.text_input("5. Are there any existing products, services, or ideas that inspire you or align with your vision?")

            submit_detailed = st.form_submit_button("Generate Idea")
        
        if submit_detailed:
            # Validate required fields
            required_fields = [problem, impact, target_audience, constraints, inspirations]
            if any(field.strip() == "" for field in required_fields):
                st.warning("Please fill in all required fields.")
            else:
                # Construct the prompt
                selected_industries = ", ".join(st.session_state.user_topics)
                prompt = (
                    f"I am interested in the following industries: {selected_industries}. "
                    f"I want to solve the problem of {problem}, aiming to create an impact by {impact}. "
                    f"The primary audience for this idea is {target_audience}. "
                    f"My constraints include {constraints}. "
                    f"I am inspired by {inspirations}. "
                    f"Please provide a unique, creative and innovative idea by utilizing deep thinking that addresses these points."
                )
                # Store the prompt for the next step
                st.session_state.prompt = prompt
                st.session_state.step = 2

    # Step 2: Generate and display the idea
    elif st.session_state.step == 2:
        if st.session_state.idea == "":
            with st.spinner("Generating your unique idea..."):
                idea = get_gpt4o_mini_response(st.session_state.prompt)
                st.session_state.idea = idea

        st.success("**Your Unique Ideas:**")
        st.write(st.session_state.idea)

        # Option to download the idea
        st.download_button(
            label="Download Idea",
            data=st.session_state.idea,
            file_name="unique_idea.txt",
            mime="text/plain"
        )

        # Option to restart the process and generate another idea
        if st.button("Generate Another Idea"):
            st.session_state.step = 0
            st.session_state.user_topics = []
            st.session_state.idea = ""
            st.session_state.prompt = ""

if __name__ == "__main__":
    main()
