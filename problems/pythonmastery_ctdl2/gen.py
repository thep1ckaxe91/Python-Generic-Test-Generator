import os
from subprocess import run
from concurrent.futures import ThreadPoolExecutor, Future

workers = 4

problem_name = "pythonmastery_ctdl2" # change this to the problem name
number_of_tests = 30 # change this to the number of tests you want to generate

test_dir = os.path.join(os.path.dirname(__file__), problem_name)

def gen_test_number(num: int) -> None:
    print(f"Generating inp test {num}...")
    try:
        with open( os.path.join(test_dir, f"Test{num:03d}", f"{problem_name}.inp"), "w") as f:
            from random import randint, uniform, random, choice
            from faker import Faker
            fake = Faker()
            d = {}
            n = randint(90,100)
            q = randint(10**4 - 10**3, 10**4)
            f.write(f"{n} {q}\n")
            def fake_password() -> str:
                return fake.password(length=randint(8, 20), special_chars=False, digits=True, upper_case=True, lower_case=True).replace(" ", "_")
            for _ in range(n):
                username = fake.name().replace(" ", "_")[:20]
                password = fake_password()
                d[username] = password
                f.write(f"{username} {password}\n")

            def random_query(op: int) -> int:
                match op:
                    case 1:  # REGISTER
                        username = fake.name().replace(" ", "_")[:20]
                        if random() < 0.2:  # 20% chance to use existing username
                            try:
                                username = choice(list(d.keys()))
                            except IndexError:
                                pass
                        password = fake_password()
                        if username not in d:
                            d[username] = password
                        f.write(f"REGISTER {username} {password}\n")
                        return 1
                    case 2:  # CHANGE
                        username = choice(list(d.keys())) if random() > 0.1 else fake.name().replace(" ", "_")[:20]
                        password = d[username] if username in d and random() > 0.1 else fake_password()
                        new_password = fake_password()
                        if username in d:
                            if password == d[username]:
                                d[username] = new_password
                        f.write(f"CHANGE {username} {password} {new_password}\n")    
                        return 2
                    case 3:  # LOGIN 
                        username = choice(list(d.keys())) if random() > 0.1 else fake.name().replace(" ", "_")[:20]
                        password = d[username] if username in d and random() > 0.1 else fake_password()
                        f.write(f"LOGIN {username} {password}\n")
                        return 3
                    case _:
                        return 0
            
            for _ in range(q):
                op = random_query(randint(1, 3))
                if op==0:
                    raise ValueError("Invalid operation generated")
            
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
+------------------------------------------------------------------+
|          Generating inputs for {problem_name}...                 |
+------------------------------------------------------------------+
          """)
    gen_inputs()
    print(f"""
+------------------------------------------------------------------+
|          Generating outputs for {problem_name}...                 |
+------------------------------------------------------------------+
          """)
    gen_outputs()

if __name__ == "__main__":
    gen_tests()
    print(f"Tests generated in {test_dir}")
    print(f"Test files: {os.listdir(test_dir)}")
    print(f"Test directories: {os.listdir(os.path.dirname(test_dir))}")
    print("Done.")