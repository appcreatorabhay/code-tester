🧪 AI-Powered Unit Test Generator for C++ Projects
This tool automatically generates, refines, and validates Google Test unit tests for any C++ project using a self-hosted Large Language Model (LLM) like Ollama (Gemma 2B).

Upload your C++ project as a .zip and get high-quality, refined unit test files — plus build logs and code coverage.

📁 Project Structure
<img width="350" alt="image" src="https://github.com/user-attachments/assets/14e1f9c4-876f-467f-ac27-97912bc81631" />

⚙️ Features
✅ Upload C++ projects as .zip
✅ Extracts source files from nested folders
✅ Uses LLM to generate Google Test unit tests
✅ Refines test cases (deduplicates, fixes includes, adds missing logic)
✅ Automatically builds with CMake + GTest
✅ Shows test logs and generates HTML coverage reports with gcov + lcov

🧪 Technologies Used
Streamlit – UI frontend

Ollama + Gemma 2B – LLM for code understanding & generation

Google Test – C++ testing framework

CMake – Build automation

lcov + genhtml – Code coverage tools

🚀 How to Run
1. Prerequisites
Ensure the following are installed:

bash
Copy
Edit
sudo apt update
sudo apt install cmake g++ lcov git
pip install streamlit pyyaml
Install Ollama and pull the Gemma model:

bash
Copy
Edit
ollama run gemma:2b
2. Run the App
bash
Copy
Edit
streamlit run app.py
📥 Input Format
Upload a .zip file that contains a C++ project. Your folder should include .cpp, .cc, .cxx, .h, .hpp, .c++ files.

💡 No need for a CMakeLists.txt — it will be auto-generated.

📤 Output
After uploading and processing:

🧪 Refined Unit Tests: output/test/refined/

📋 Build/Test Logs: output/logs/test_results.log

📊 Coverage Report: output/coverage/html/index.html

📌 Notes
All tests are refined whether they pass or fail initially.

Logs and HTML reports help debug build/test issues.

Coverage is calculated automatically after a successful build.
