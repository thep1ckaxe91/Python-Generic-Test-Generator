import argparse
from subprocess import run
import os
import sys
import shutil
import glob

problem_dir = os.path.join(os.path.dirname(__file__), "problems")

def create_problem(problem_id: int, problem_type: str, problem_prefix: str, checker_lang: str | None = None) -> None:
    print(f"Creating problem {problem_id}...")
    problem_name = f"{problem_prefix}{problem_type}{problem_id}"
    problem_path = os.path.join(problem_dir, problem_name)

    if os.path.exists(problem_path):
        print(f"Error: Problem directory '{problem_name}' already exists.")
        sys.exit(1)

    os.makedirs(os.path.join(problem_path, problem_name), exist_ok=True)

    template_dir = os.path.join(problem_dir, "template")

    files_to_copy = {
        "gen.py": "gen.py",
        "judge.py": "judge.py",
        "submission.py": "submission.py",
        "solution.py": f"{problem_name}.py",
        "problem.md": f"{problem_name}.md",
    }

    for template_file, dest_file in files_to_copy.items():
        shutil.copy(
            os.path.join(template_dir, template_file),
            os.path.join(problem_path, dest_file),
        )

    if checker_lang:
        checker_name = f"{problem_name}.checker.{checker_lang}"
        shutil.copy(
            os.path.join(template_dir, f"checker.{checker_lang}"),
            os.path.join(problem_path, checker_name),
        )
    print(f"Problem {problem_name} created successfully.")


def generate_tests(problem_name: str) -> None:
    print(f"Generating tests for {problem_name}...")
    problem_path = os.path.join(problem_dir, problem_name)

    if not os.path.isdir(problem_path):
        print(f"Error: Problem directory '{problem_name}' not found.")
        exit(1)

    try:
        run(
            ["python3", os.path.join(problem_path, "gen.py")],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except Exception as e:
        print(f"Error generating test data for {problem_name}: {e}")
        return

    print(f"Problem {problem_name} generated successfully. Zipping test files...")
    zip_path = os.path.join(problem_path, problem_name)
    if os.path.exists(f"{zip_path}.zip"):
        os.remove(f"{zip_path}.zip")
    shutil.make_archive(
        zip_path,
        "zip",
        root_dir=os.path.join(problem_path, problem_name),
    )


def prune_files():
    print("Pruning files...")
    files_to_remove = []
    for ext in ["**/*.zip", "**/*.inp", "**/*.out"]:
        files_to_remove.extend(glob.glob(os.path.join(problem_dir, ext), recursive=True))

    for file_path in files_to_remove:
        try:
            os.remove(file_path)
            print(f"Removed {file_path}")
        except OSError as e:
            print(f"Error removing {file_path}: {e}")
    print("Pruning complete.")


def judge_problem(problem_name: str):
    print(f"Judging problem {problem_name}...")
    problem_path = os.path.join(problem_dir, problem_name)
    if not os.path.isdir(problem_path):
        print(f"Error: Problem directory '{problem_name}' not found.")
        return

    judge_script = os.path.join(problem_path, "judge.py")
    if not os.path.exists(judge_script):
        print(f"Error: 'judge.py' not found in '{problem_name}' directory.")
        return

    try:
        run(
            ["python3", judge_script],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=problem_path,
        )
    except Exception as e:
        print(f"Error judging {problem_name}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manager for competitive programming problems."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'new' command
    parser_new = subparsers.add_parser("new", help="Create a new problem")
    parser_new.add_argument("problem_prefix", help="Prefix for the problem name")
    parser_new.add_argument("problem_type", help="Type of the problem")
    parser_new.add_argument(
        "ids", nargs="+", type=int, help="List of problem IDs to generate"
    )
    parser_new.add_argument(
        "--checker",
        choices=["py", "cpp"],
        help="Create a checker file (py or cpp)",
    )

    # 'gen' command
    parser_gen = subparsers.add_parser("gen", help="Generate test cases for a problem")
    parser_gen.add_argument("problem_names", nargs="+", help="Name(s) of the problem(s) to generate tests for")

    # 'prune' command
    subparsers.add_parser("prune", help="Remove all .zip, .inp, and .out files")

    # 'judge' command
    parser_judge = subparsers.add_parser("judge", help="Judge a submission")
    parser_judge.add_argument("problem_name", help="Name of the problem to judge")

    args = parser.parse_args()

    if args.command == "new":
        for problem_id in args.ids:
            create_problem(problem_id, args.problem_type, args.problem_prefix, args.checker)
    elif args.command == "gen":
        for problem_name in args.problem_names:
            generate_tests(problem_name)
    elif args.command == "prune":
        prune_files()
    elif args.command == "judge":
        judge_problem(args.problem_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
