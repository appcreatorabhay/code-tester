import os
import zipfile
import subprocess
from pathlib import Path
import yaml

VALID_EXTENSIONS = (".cpp", ".cc", ".cxx", ".c++", ".h", ".hpp")

def load_prompt(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)["instruction"]

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def extract_code_block(response):
    inside = False
    code = []
    for line in response.splitlines():
        if line.strip().startswith("```"):
            inside = not inside
        elif inside:
            code.append(line)
    return "\n".join(code)

def generate_tests(source_dir, test_output_dir, model="gemma:2b"):
    os.makedirs(test_output_dir, exist_ok=True)
    prompt = load_prompt("prompts/unit_test.yaml")

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(VALID_EXTENSIONS):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()

                input_prompt = f"{prompt}\n\n{code}"
                result = subprocess.run(
                    ["ollama", "run", model],
                    input=input_prompt.encode(),
                    stdout=subprocess.PIPE
                )
                test_code = extract_code_block(result.stdout.decode())
                with open(os.path.join(test_output_dir, f"test_{file}.cpp"), "w") as out:
                    out.write(test_code)

def refine_failed_tests(log_path, test_dir, refined_output_dir, model="gemma:2b"):
    os.makedirs(refined_output_dir, exist_ok=True)
    refine_prompt = load_prompt("prompts/refine_test.yaml")

    if not os.path.exists(log_path):
        return  # No logs to analyze

    with open(log_path, "r") as log_file:
        log_content = log_file.read()

    for test_file in os.listdir(test_dir):
        full_path = os.path.join(test_dir, test_file)
        if test_file.endswith(".cpp") and test_file in log_content:
            with open(full_path, 'r') as f:
                test_code = f.read()
            prompt = f"{refine_prompt}\n\n{test_code}"
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode(),
                stdout=subprocess.PIPE
            )
            refined_code = extract_code_block(result.stdout.decode())
            with open(os.path.join(refined_output_dir, test_file), "w") as out:
                out.write(refined_code)

def create_cmake(source_dir):
    cmake = f"""
cmake_minimum_required(VERSION 3.10)
project(GeneratedTests)

set(CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}} -g -O0 --coverage")
set(CMAKE_EXE_LINKER_FLAGS "${{CMAKE_EXE_LINKER_FLAGS}} --coverage")

file(GLOB_RECURSE SRC_FILES {source_dir}/*.cpp {source_dir}/*.cc {source_dir}/*.cxx)
file(GLOB_RECURSE TEST_FILES output/test/refined/*.cpp)

add_executable(runTests ${{SRC_FILES}} ${{TEST_FILES}})

find_package(GTest REQUIRED)
include_directories(${{GTEST_INCLUDE_DIRS}})

target_link_libraries(runTests ${{GTEST_LIBRARIES}} pthread)

enable_testing()
add_test(NAME AllTests COMMAND runTests)
"""
    with open("CMakeLists.txt", "w") as f:
        f.write(cmake)

def run_build():
    subprocess.run(["bash", "utils/build_and_test.sh"])

def run_coverage():
    subprocess.run(["bash", "utils/coverage.sh"])

def run_pipeline(zip_path):
    EXTRACT_DIR = "extracted/"
    TEST_DIR = "output/test/"
    REFINED_DIR = "output/test/refined/"
    LOG_PATH = "output/logs/test_results.log"

    # Clean old output
    os.makedirs(TEST_DIR, exist_ok=True)
    os.makedirs(REFINED_DIR, exist_ok=True)
    os.makedirs("output/logs", exist_ok=True)

    extract_zip(zip_path, EXTRACT_DIR)
    generate_tests(EXTRACT_DIR, TEST_DIR)
    # Initially, use raw tests as refined ones
    for file in os.listdir(TEST_DIR):
        if file.endswith(".cpp"):
            src = os.path.join(TEST_DIR, file)
            dst = os.path.join(REFINED_DIR, file)
            with open(src, "r") as f_src, open(dst, "w") as f_dst:
                f_dst.write(f_src.read())

    create_cmake(EXTRACT_DIR)
    run_build()

    # Refine if build/test failed
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as log:
            log_content = log.read()
            if "FAILED" in log_content or "error:" in log_content:
                refine_failed_tests(LOG_PATH, TEST_DIR, REFINED_DIR)
                create_cmake(EXTRACT_DIR)
                run_build()

    run_coverage()

# For standalone test
if __name__ == "__main__":
    run_pipeline("sample_project.zip")
