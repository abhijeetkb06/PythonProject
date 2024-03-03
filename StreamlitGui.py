import streamlit as st
import pandas as pd
import numpy as np

# Set page title
st.set_page_config(page_title="Fancy Streamlit App")

# Set background color and padding
st.markdown(
    """
    <style>
        .reportview-container {
            background: linear-gradient(to bottom, #33ccff 0%, #ff99cc 100%);
            padding: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Fancy Streamlit App")
st.write("Welcome to the fancy Streamlit app! This app showcases various Streamlit elements and widgets.")

# Sidebar
st.sidebar.title("Sidebar Options")
st.sidebar.write("Use the sidebar to explore different options.")

# Checkbox
option1 = st.sidebar.checkbox("Enable Option 1")
if option1:
    st.write("Option 1 is enabled!")
else:
    st.write("Option 1 is disabled.")

# Selectbox
option2 = st.sidebar.selectbox("Select an Option", ["Option A", "Option B", "Option C"])
st.write("Selected Option:", option2)

# Slider
option3 = st.sidebar.slider("Select a Value", min_value=0, max_value=100, value=50)
st.write("Selected Value:", option3)

# Button
if st.sidebar.button("Click Me!"):
    st.write("Button clicked!")

# Text input
user_input = st.text_input("Enter your text here:", "")
st.write("You entered:", user_input)

# Dataframe display
st.subheader("Sample Dataframe")
df = pd.DataFrame(np.random.randn(10, 5), columns=["A", "B", "C", "D", "E"])
st.dataframe(df)

# Plot
st.subheader("Sample Plot")
st.line_chart(df)

# Markdown
st.subheader("Additional Information")
st.markdown("This is a **fancy** Streamlit app designed to showcase various Streamlit elements and widgets.")

# Footer
st.write("---")
st.write("Thank you for using the fancy Streamlit app!")
