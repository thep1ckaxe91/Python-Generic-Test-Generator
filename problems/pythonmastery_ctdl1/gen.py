import os
from subprocess import run
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

workers = 4


problem_name = "pythonmastery_ctdl1" # change this to the problem name
number_of_tests = 50 # change this to the number of tests you want to generate

test_dir = os.path.join(os.path.dirname(__file__), problem_name)

def gen_test_number(num: int) -> None:
    with open( os.path.join(test_dir, f"Test{num:03d}", f"{problem_name}.inp"), "w") as f:
        from random import randint, uniform, random, choice
        from faker import Faker
        fake = Faker()
        d = {}
        n = randint(10**5 - 10**4, 10**5)
        q = randint(10**5 - 10**4, 10**5)
        f.write(f"{n} {q}\n")

        print("Generating initial data...")

        for _ in range(n):
            name = fake.name().replace(" ", "_")
            score = uniform(0, 10)
            d[name] = score
            f.write(f"{name} {score:.2f}\n")
        def random_query(op: int) -> int:
            match op:
                case 1:  # ADD
                    if random() < 0.2:
                        name = choice(list(d.keys()))
                    else:
                        name = fake.name().replace(" ", "_")
                        
                    score = uniform(0, 10)
                    
                    if d.get(name) is None:
                        d[name] = score
                                        
                    f.write(f"ADD {name} {score:.2f}\n")
                    return 1
                case 2:  # UPDATE
                    if random() < 0.8:
                        name = choice(list(d.keys()))
                    else:
                        name = fake.name().replace(" ", "_")
                    score = uniform(0, 10)

                    if d.get(name) is not None:
                        d[name] = score

                    f.write(f"UPDATE {name} {score:.2f}\n")
                    return 2
                case 3:  # REMOVE 
                    if random() < 0.8:
                        name = choice(list(d.keys()))
                    else:
                        name = fake.name().replace(" ", "_")
                    
                    if d.get(name) is not None:
                        d.pop(name)

                    f.write(f"REMOVE {name}\n")
                    return 3
                case 4:  # PRINT
                    if random() < 0.9:
                        name = choice(list(d.keys()))
                    else:
                        name = fake.name().replace(" ", "_")
                    f.write(f"PRINT {name}\n")
                    return 4
                case _:
                    return 0
        
        print("Generating queries...")
        
        for _ in range(q):
            op = random_query(randint(1, 4))
            if op == 0:
                raise ValueError("Invalid operation generated")
            

def gen_outputs() -> None:
    for i in range(1, number_of_tests + 1):
        print(f"Generating outputs for test {i}...")
        with open(os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.out"), "w") as f:
            run(
                ["python3", os.path.join(os.path.dirname(__file__), f"{problem_name}.py")],
                input=open(os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.inp")).read(),
                text=True,
                stdout=f,
                check=True
            )
def gen_inputs() -> None:
    os.makedirs(test_dir, exist_ok=True)
    
    with ThreadPoolExecutor(workers) as pool:
        # this could be multithreaded if needed
        for i in range(1, number_of_tests + 1):
            test_path = os.path.join(test_dir, f"Test{i:03d}")
            os.makedirs(test_path, exist_ok=True)
            print(f"Generating input for test {i}...")
            pool.submit(gen_test_number, i)


def gen_tests() -> None:
    # gen_inputs()
    gen_outputs()

if __name__ == "__main__":
    gen_tests()
    print(f"Tests generated in {test_dir}")
    print(f"Test files: {os.listdir(test_dir)}")
    print(f"Test directories: {os.listdir(os.path.dirname(test_dir))}")
    print("Done.")