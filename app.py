import streamlit as st
import os
from generate_tests import run_pipeline

# Page config
st.set_page_config(page_title="🧪 C++ Unit Test Generator", layout="centered")
st.title("🧪 AI-Powered C++ Unit Test Generator")
st.markdown("Upload a ZIP file containing your C++ project, and this tool will generate unit tests automatically using a Large Language Model (LLM).")

# File upload
uploaded_file = st.file_uploader("📁 Upload your C++ project (.zip)", type=["zip"])

if uploaded_file:
    # Save uploaded zip to disk
    with open("uploaded.zip", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ File uploaded successfully.")

    # Run pipeline
    with st.spinner("⏳ Generating and refining test cases..."):
        run_pipeline("uploaded.zip")

    st.success("✅ Unit tests generated and refined successfully!")
    st.markdown("---")

    # Show output links
    if os.path.exists("output/test/refined"):
        st.markdown("### 📄 Refined Unit Tests")
        for file in os.listdir("output/test/refined"):
            st.download_button(
                label=f"📥 Download {file}",
                data=open(f"output/test/refined/{file}", "rb").read(),
                file_name=file
            )

    if os.path.exists("output/logs/test_results.log"):
        st.markdown("### 📋 Test Logs")
        st.code(open("output/logs/test_results.log").read(), language="text")

    if os.path.exists("output/coverage/html/index.html"):
        st.markdown("### 📊 Coverage Report")
        st.markdown(
            "[🔍 View HTML Coverage Report (open in browser)](output/coverage/html/index.html)"
        )
