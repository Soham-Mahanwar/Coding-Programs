import os
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
import streamlit as st

# Set up app title
st.set_page_config(page_title="Web Locator Automation Tool", layout="wide")
st.title("Web Locator Automation Tool")

# Create directory for saving locators
LOCATORS_DIR = "Locator-Automation"
os.makedirs(LOCATORS_DIR, exist_ok=True)

# Define locator file path
LOCATOR_FILE_PATH = os.path.join(LOCATORS_DIR, "locator.json")

# Features section
st.sidebar.header("Features")
st.sidebar.markdown(
    """
    - **Extract IDs, Classes, Names, and XPaths**
    - **Responsive Analysis**
    - **Version Tracking**
    - **AI-Supported Locator Ranking**
    """
)

# URL input field
url = st.text_input("Enter a webpage URL to extract locators:", placeholder="https://example.com")

if url:
    if st.button("Extract Locators"):
        try:
            # Fetch webpage
            st.info("Fetching webpage content...")
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad HTTP response
            soup = BeautifulSoup(response.content, "html.parser")
            dom = etree.HTML(str(soup))

            # Extract locators
            st.info("Extracting locators...")
            locators = []
            for tag in soup.find_all(True):
                locator = {"tag": tag.name}
                for attr, value in tag.attrs.items():
                    locator[attr] = value
                try:
                    xpath = dom.getroottree().getpath(dom.xpath(f"//*[name()='{tag.name}']")[0])
                    locator["xpath"] = xpath
                except IndexError:
                    locator["xpath"] = None
                locators.append(locator)

            # Save locators to file
            st.info("Saving locators...")
            with open(LOCATOR_FILE_PATH, "w") as f:
                json.dump(locators, f, indent=4)

            # Display results
            st.success(f"Found {len(locators)} locators!")
            st.json(locators[:10])  # Display first 10 locators
            st.download_button(
                label="Download Locators JSON",
                data=json.dumps(locators, indent=4),
                file_name="locator.json",
                mime="application/json",
            )
            st.info(f"Locators saved to {LOCATOR_FILE_PATH}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Placeholder buttons for future features
st.button("Analyze Responsiveness")
st.button("Track Version")

# Footer
st.markdown("---")
st.markdown("Built by **Soham Mahanwar**, Pune, India.")
