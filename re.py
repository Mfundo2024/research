import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI Client
client = OpenAI(api_key=api_key)

# Pre-saved prompt for the comprehensive analysis
PRE_SAVED_PROMPT = """
As a world-class Analyst, please analyze the brand {{brand}} by looking at the Company, Consumer, Category, and Culture. Include real-time data around market share and demographics, along with creative outputs around positioning and cultural impact. Apply this analysis to each of the following areas:

**Company**
1. Origin Story
2. Recent News
3. Market Share
4. Employee/Consumer Satisfaction
5. Expert Opinion
6. Reasons to Believe

**Category**
1. Advertising Cliches in {{category}}
2. Positioning Among Peers
3. Category Issues & Opportunities
4. Category Evolution

**Consumer**
1. Consumer Demographics
2. Consumer Problem & Goal
3. Consumer Mindset

**Culture**
1. Audience Focus
2. Macro Forces
3. Muses
4. Subcultures

Please provide a full detailed analysis with all the hyperlinks to the source for each topic area with actionable insights and recommendations.
"""

def analyze_brand_and_category(brand, category):
    """
    Function to perform comprehensive analysis using GPT-4.
    """
    # Format the pre-saved prompt with dynamic inputs
    prompt = PRE_SAVED_PROMPT.replace("{{brand}}", brand).replace("{{category}}", category)

    # Call GPT-4 API to process the prompt
    gpt_response = client.chat.completions.create(model="gpt-4",
    messages=[{"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": prompt}])

    # Extract GPT-4's response
    analysis = gpt_response.choices[0].message.content
    return analysis

# Streamlit App
def main():
    st.title("Comprehensive Brand & Category Analysis")
    st.markdown(
        """
        This app performs an in-depth analysis of a brand and its category, covering:
        - Company aspects (e.g., origin story, market share, satisfaction levels)
        - Category trends and positioning
        - Consumer insights and demographics
        - Cultural relevance and subcultural impact

        Enter the brand and category below to get started.
        """
    )

    # Input fields
    brand = st.text_input("Enter the brand name", placeholder="e.g., Nike, Apple")
    category = st.text_input("Enter the category", placeholder="e.g., Sportswear, Technology")

    # Button to perform analysis
    if st.button("Analyze Brand and Category"):
        if not brand or not category:
            st.error("Please fill in both fields before running the analysis.")
        else:
            # Perform analysis
            with st.spinner("Analyzing the brand and category..."):
                try:
                    analysis = analyze_brand_and_category(brand, category)
                    st.success("Analysis complete!")
                    st.markdown("### Detailed Analysis")

                    # Display analysis
                    st.text_area(label="Full Analysis", value=analysis, height=400)

                    # Download button for the analysis
                    st.download_button(
                        label="Download Analysis as Text File",
                        data=analysis,
                        file_name=f"{brand}_analysis.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
