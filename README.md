# Python Test Case Generator

This repository provides a framework for generating test cases for Python scripts. It's particularly useful for tasks that involve file-based inputs and outputs, such as competitive programming problems, data processing pipelines, or any script that reads from and writes to files.

## Features

*   **Scalable Test Generation:** Easily generate a large number of test cases.
*   **Customizable Generators:** Each problem has its own test case generator (`gen.py`) that can be customized to produce specific types of data.
*   **Automated Scaffolding:** The `manager.py` script automates the creation of new problem directories, setting up the necessary file structure from a template.
*   **File-Based I/O:** Designed for testing scripts that read from and write to files.
*   **Local Judging:** Includes a `judge.py` template for local testing and validation of solutions.
    *   **Note:** The local judging system is currently under development and not fully implemented. The `judge.py` file is a template and does not yet utilize the checker.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [<repository_url>](https://github.com/thep1ckaxe91/Python-Generic-Test-Generator.git)
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Creating a New Problem

To create a new problem, use the `manager.py` script:

```bash
python manager.py <problem_prefix> <problem_type> <id1> <id2> ...
```

**Example:**

```bash
python manager.py pythonmastery pandas 7 8 9
```

This command will create new problem directories inside the `problems/` folder (e.g., `problems/pythonmasterypandas7/`). Each new problem directory will be populated with files from the `template/` directory.

### 2. Customizing the Test Case Generator (`gen.py`)

After creating a new problem, you need to customize the `gen.py` file to generate the desired test cases. Open `problems/<problem_name>/gen.py` and modify the following:

*   **`number_of_tests`**: An integer that specifies the number of test cases to generate.
*   **`input_file` and `output_file`**: Strings that define the names of the input and output files. If `input_file` is set to `"stdin"`, the script will use standard input and output.
*   **`io_binary`**: A boolean that indicates whether the I/O is in binary or text format.
*   **`gen_test_number(num: int)`**: This function contains the core logic for generating a single test case. You should modify this function to write the desired input data to the input file. You can use the `faker` library to generate random data.

### 3. Writing the Solution

Write your solution in the `<problem_name>.py` file. This script will be executed by the `gen.py` script to generate the output for each test case.

### 4. Generating Test Cases

Once you have customized `gen.py` and written your solution, you can generate the test cases by running the `manager.py` script again with the same arguments as in step 1.

```bash
python manager.py <problem_prefix> <problem_type> <id1> <id2> ...
```

This will create a set of test case directories (e.g., `Test001`, `Test002`, etc.) inside the problem's directory. Each test case directory will contain an input file and a corresponding output file.

### 5. Running a Solution Manually

To run a solution for a problem manually, execute the problem's main Python file:

```bash
python problems/<problem_name>/<problem_name>.py
```

This will typically read the input data from a file, process it, and write the output to another file.

## Local Judging

The local judging system is currently under development. The `judge.py` file in the template is a basic placeholder and does not yet implement a complete judging solution or utilize the C++ checker in the `checker` directory. Contributions to improve the judging system are welcome.

## Dependencies

This project relies on the following Python libraries:

*   [Faker](https://faker.readthedocs.io/): For generating fake data in test cases.
*   [dmoj](https://pypi.org/project/dmoj/): For interacting with the DMOJ online judge.
*   [matplotlib](https://matplotlib.org/): For data visualization.
*   [numpy](https://numpy.org/): For numerical operations.

All dependencies are listed in the `requirements.txt` file.
