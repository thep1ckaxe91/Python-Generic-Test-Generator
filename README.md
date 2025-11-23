# Python Test Case Generator

This repository provides a framework for generating test cases for Python scripts, with a structure inspired by competitive programming platforms like **DMOJ**. It's designed for problems that use file-based I/O.

## Getting Started

1.  **Clone the repository and navigate into it.**
    ```bash
    git clone https://github.com/thep1ckaxe91/Python-Generic-Test-Generator.git
    cd Python-Generic-Test-Generator
    ```
2.  **Create and activate a virtual environment.**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies.**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The `manager.py` script helps you manage your problems.

| Command | Description |
| :--- | :--- |
| `new` | Creates a new problem directory from a template. |
| `gen` | Generates test cases for a problem. |
| `prune` | Removes all generated test files (`.zip`, `.inp`, `.out`). |
| `judge` | Runs the local judge for a specific problem. |

Use `python manager.py <command> --help` for more details on each command.

#### Creating a New Problem

```bash
python manager.py new <prefix> <type> <id1> <id2> ... [--checker <py/cpp>]
```
- **Example**: `python manager.py new pythonmastery pandas 1 2 3`
- This creates problem directories like `problems/pythonmasterypandas1/`.
- The `--checker` flag will also create a checker file (e.g., `pythonmasterypandas1.checker.cpp`).

#### Generating Test Cases

```bash
python manager.py gen <problem_name_1> <problem_name_2> ...
```
- **Example**: `python manager.py gen pythonmasterypandas1`

#### Local Judging

The local judging system is a work in progress. The goal is to have `judge.py` automatically run your `submission.py` against the generated test cases, similar to an online judge. Currently, it's a template and does not yet use the checker.

To test it, run:
```bash
python manager.py judge <problem_name>
```

## After Creating a Problem

1.  **Customize `gen.py`**: Modify this file in your new problem directory to define how test cases are generated.
2.  **Write your solution**: Place your solution code in `<problem_name>.py`.
3.  **Generate test cases**: Run the `gen` command to generate the `.in` and `.out` files.
