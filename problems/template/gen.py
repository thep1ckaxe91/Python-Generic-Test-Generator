import os, time
from subprocess import run, TimeoutExpired
from concurrent.futures import ThreadPoolExecutor, Future
from random import uniform, randint, random, choice, shuffle, randbytes
from faker import Faker
from shutil import copy


fake = Faker()

workers = 6

problem_name = os.path.basename(os.path.dirname(__file__)) # No modification

number_of_tests = 1  # CHANGE THIS to the number of tests you want to generate
io_binary = False # True if the output file is binary format
test_dir = os.path.join(os.path.dirname(__file__), problem_name) # No modification

input_file = "stdin" # If leave as stdin, the code use stdio instead, change to full file name if want file io
output_file = "stdout"

def gen_test_number(num: int) -> None:
    print(f"Generating inp test {num}...")
    try:
        with open(
            os.path.join(test_dir, f"Test{num:03d}", f"{problem_name}.inp"), "w"
        ) as f:
            f.write("This is a template input data, please make your own and delete this")

        print(f"Test {num} generated successfully.")
    except Exception as e:
        print(f"Error generating test {num}: {e}")
        return


def gen_outputs_std() -> None:
    futures: list[Future] = []
    output_files = []
    with ThreadPoolExecutor(workers) as pool:
        for i in range(1, number_of_tests + 1):
            output_files.append(
                open(os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.out"), "w")
            )
            print(f"Generating out test {i}...")
            futures.append(
                pool.submit(
                    run,
                    [
                        "python3",
                        os.path.join(os.path.dirname(__file__), f"{problem_name}.py"),
                    ],
                    stdin=open(
                        os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.inp"), 'r'
                    ),
                    text=(not io_binary),
                    stdout=output_files[-1],
                    check=True,
                )
            )
    for future, file in zip(futures, output_files):
        try:
            future.result()
        except Exception as e:
            print(f"Error generating output: {e}")
        finally:
            file.close()

def gen_outputs_file() -> None:
    for i in range(1, number_of_tests + 1):
        print(f"Generating out test {i}...")

        copy(
            os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.inp"),
            os.path.join(os.path.dirname(__file__), input_file)
        )
        timeout = 5
        try:
            start = time.perf_counter()
            run(
                [
                    "python3",
                    os.path.join(os.path.dirname(__file__), f"{problem_name}.py"),
                ],
                cwd=os.path.dirname(__file__),
                check=True,
                timeout=timeout
            )
            end = time.perf_counter()
            print(f"Test {i} output generated in {end - start:.2f}s")
        except TimeoutExpired:
            print(f"Test {i} runtime exceed {timeout}s, abort")
        copy(
            os.path.join(os.path.dirname(__file__), output_file),
            os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.out"),
        )

def gen_inputs() -> None:
    os.makedirs(test_dir, exist_ok=True)

    with ThreadPoolExecutor(workers) as pool:
        for i in range(1, number_of_tests + 1):
            test_path = os.path.join(test_dir, f"Test{i:03d}")
            os.makedirs(test_path, exist_ok=True)
            pool.submit(gen_test_number, i)


def gen_tests() -> None:
    print(
        f"""
####################################################################
PROBLEM NAME: {problem_name.upper()}
####################################################################
+------------------------------------------------------------------+
|                        Generating inputs                         |
+------------------------------------------------------------------+
          """
    )
    gen_inputs()
    print(
        f"""
+------------------------------------------------------------------+
|                       Generating outputs                         |
+------------------------------------------------------------------+
          """
    )
    if input_file == "stdin":
        gen_outputs_std()
    else:
        gen_outputs_file()


if __name__ == "__main__":
    gen_tests()
    print("Done.")
