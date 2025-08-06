import os
from subprocess import run
from concurrent.futures import ThreadPoolExecutor, Future
from random import uniform, randint, random, choice
from faker import Faker
fake = Faker()

workers = 6

problem_name = "pythonmastery_ctdl3" # change this to the problem name
number_of_tests = 20 # change this to the number of tests you want to generate

test_dir = os.path.join(os.path.dirname(__file__), problem_name)

def gen_test_number(num: int) -> None:
    print(f"Generating inp test {num}...")
    try:
        with open( os.path.join(test_dir, f"Test{num:03d}", f"{problem_name}.inp"), "w") as f:
            n = randint(10**5-10**4,10**5)
            q = randint(10**5-10**4,10**5)
            
            f.write(f"{n} {q}\n")
            a = [randint(-10**9,10**9) for _ in range(n)]
            for _ in range(randint(1,5)):
                for i in range(n):
                    a[i] = choice(a)
                
            f.write(" ".join([str(v) for v in a]) + "\n")
        
            for _ in range(q):
                f.write(f"{randint(-10**9,10**9)}\n" if random() < 0.1 else f"{choice(a)}\n")

        print(f"Test {num} generated successfully.")
    except Exception as e:
        print(f"Error generating test {num}: {e}")
        return

def gen_outputs() -> None:
    futures: list[Future] = []
    output_files = []
    with ThreadPoolExecutor(workers) as pool:
        for i in range(1, number_of_tests + 1):
            output_files.append(open(os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.out"), "w"))
            print(f"Generating out test {i}...")
            futures.append(
                pool.submit(
                    run,
                    ["python3", os.path.join(os.path.dirname(__file__), f"{problem_name}.py")],
                    input=open(os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.inp")).read(),
                    text=True,
                    stdout=output_files[-1],
                    check=True
                )
            )
    for future, file in zip(futures, output_files):
        try:
            future.result()
        except Exception as e:
            print(f"Error generating output: {e}")
            return
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
    print(f"""
####################################################################
PROBLEM NAME: {problem_name.upper()}
####################################################################
+------------------------------------------------------------------+
|                        Generating inputs                         |
+------------------------------------------------------------------+
          """)
    gen_inputs()
    print(f"""
+------------------------------------------------------------------+
|                       Generating outputs                         |
+------------------------------------------------------------------+
          """)
    gen_outputs()

if __name__ == "__main__":
    gen_tests()
    print(f"Tests generated in {test_dir}")
    print(f"Test files: {os.listdir(test_dir)}")
    print(f"Test directories: {os.listdir(os.path.dirname(test_dir))}")
    print("Done.")