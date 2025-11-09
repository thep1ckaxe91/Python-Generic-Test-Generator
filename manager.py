from subprocess import run
import os
import sys
import shutil

problem_dir = os.path.join(os.path.dirname(__file__), "problems")


def gen_problem(problem_id: int, problem_type: str, problem_prefix: str) -> None:
    print(f"Generating problem {problem_id}...")
    problem_name = f"{problem_prefix}{problem_type}{problem_id}"
    os.makedirs(
        os.path.join(problem_dir, problem_name, problem_name), exist_ok=True
    )  # make tests dir

    # Ensure if required files doesnt exist, it create with templates
    if not os.path.exists(os.path.join(problem_dir, problem_name, "gen.py")):
        shutil.copy(
            os.path.join(problem_dir, "template", "gen.py"),
            os.path.join(problem_dir, problem_name, "gen.py"),
        )
    
    if not os.path.exists(os.path.join(problem_dir, problem_name, "judge.py")):
        shutil.copy(
            os.path.join(problem_dir, "template", "judge.py"),
            os.path.join(problem_dir, problem_name, "judge.py"),
        )

    if not os.path.exists(os.path.join(problem_dir, problem_name, "submission.py")):
        shutil.copy(
            os.path.join(problem_dir, "template", "submission.py"),
            os.path.join(problem_dir, problem_name, "submission.py"),
        )

    if not os.path.exists(os.path.join(problem_dir, problem_name, problem_name + ".py")):
        shutil.copy(
            os.path.join(problem_dir, "template", "solution.py"),
            os.path.join(problem_dir, problem_name, problem_name + ".py"),
        )
    if not os.path.exists(os.path.join(problem_dir, problem_name, problem_name + ".md")):
        shutil.copy(
            os.path.join(problem_dir, "template", "problem.md"),
            os.path.join(problem_dir, problem_name, problem_name + ".md"),
        )


    
    try:
        run(
            ["python3", os.path.join(problem_dir, problem_name, "gen.py")],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except Exception as e:
        print(f"Error generating test data for {problem_id}: {e}")
        return

    print(f"Problem {problem_name} generated successfully. Zipping test files...")
    if os.path.exists(os.path.join(problem_dir, problem_name, problem_name+'.zip')):
        os.remove(os.path.join(problem_dir, problem_name, problem_name+'.zip'))
    shutil.make_archive(
        os.path.join(problem_dir, problem_name, problem_name),
        "zip",
        root_dir=os.path.join(problem_dir, problem_name, problem_name),
        base_dir=os.path.join(problem_dir, problem_name, problem_name),
    )


try:
    problems: list[int] = list(map(int, sys.argv[3:]))  # change this
    problem_prefix = sys.argv[1]
    problem_type = sys.argv[2] or ""    
except:
    print(
        "Invalid argv, please enter the following format: problem_prefix problem_type id1 id2 id3 ..."
    )
    exit(1)


def main() -> None:
    for problem_id in problems:
        gen_problem(problem_id, problem_type, problem_prefix)


if __name__ == "__main__":
    main()
