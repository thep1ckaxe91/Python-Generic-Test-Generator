import os
from subprocess import run
from concurrent.futures import ThreadPoolExecutor, Future
from random import uniform, randint, random, choice, shuffle
from faker import Faker

fake = Faker()

workers = 6

problem_name = "" # will be the name of the only folder in the same dir with this file
for _,dirs,__ in os.walk(os.path.dirname(__file__)):
    problem_name = dirs[0]
    break
number_of_tests = 1  # CHANGE THIS to the number of tests you want to generate

test_dir = os.path.join(os.path.dirname(__file__), problem_name)


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


def gen_outputs() -> None:
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
                    input=open(
                        os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.inp")
                    ).read(),
                    text=True,
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


def gen_inputs() -> None:
    os.makedirs(test_dir, exist_ok=True)

    with ThreadPoolExecutor(workers) as pool:
        for i in range(1, number_of_tests + 1):
            test_path = os.path.join(test_dir, f"Test{i:03d}")
            os.makedirs(test_path, exist_ok=True)
            # gen_test_number(i)
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
    gen_outputs()


if __name__ == "__main__":
    gen_tests()
    print("Done.")
