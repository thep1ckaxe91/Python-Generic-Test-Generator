from gen import problem_name, test_dir, input_file, output_file, number_of_tests
from subprocess import run, TimeoutExpired
from shutil import copy
import os
import time

os.chdir(os.path.dirname(__file__))
def judge_test(test_num: int):

    ans_lines = []
    with open(os.path.join(test_dir, f"Test{test_num:03d}", f"{problem_name}.out")) as f:
        ans_lines = f.readlines()
    out_lines = []
    with open(os.path.join(os.path.dirname(__file__), output_file)) as f:
        out_lines = f.readlines()

    def default():
        try:
            return all([a.strip() == o.strip() for a, o in zip(ans_lines, out_lines, strict=True)])
        except:
            return False

    def float_cmp():
        try:
            return all(
                all(x - y <= 1e-2 for x, y in zip(map(float, a.split()), map(float, o.split()), strict=True))
                for a, o in zip(ans_lines, out_lines)
            )
        except:
            return False

        

    return float_cmp()

SubmissionResult = tuple[int, float, float]

def judge_submission_file(filename: str, timeout: float | None = None) -> SubmissionResult:
    '''
    judge a file within the same dir

    :params:
    - filename: filename without extension, automatically be .py type
    - timeout: if omitted, there will be no time out. If does, will print TLE when there's such test

    :return:
    A tuple with first element be the score and the 2nd element be the max time to execute a test

    '''

    score = 0
    max_time = 0
    total_time = 0
    print(f"Juding {filename}")
    for i in range(1,number_of_tests+1):
        copy(
            os.path.join(test_dir, f"Test{i:03d}", f"{problem_name}.inp"),
            os.path.join(os.path.dirname(__file__), input_file)
        )
        try:
            start = time.perf_counter()
            run_result = run(
                [
                    "python",
                    os.path.join(os.path.dirname(__file__), f"{filename}.py"),
                ],
                cwd=os.path.dirname(__file__),
                check=True,
                timeout=timeout
            )
            end = time.perf_counter()
            max_time = max(max_time, end-start)
            total_time += end-start
        except TimeoutExpired:
            print(f"Test {i}/{number_of_tests}: Time Limit Exceeded")
            if timeout:
                max_time = max(max_time, timeout)
                total_time += timeout
            continue
        except Exception as e:
            res = f"Test {i}/{number_of_tests}: Runtime Error \n({e})"

            
        try:
            if judge_test(i):
                res = (f"Test {i}/{number_of_tests}: Accepted")
                score += 1
            else:
                res = (f"Test {i}/{number_of_tests}: Wrong Answer")
        except:
            res = f"Test {i}/{number_of_tests}: Checker Error"

        print(res)
    print(f"Score: {score}/{number_of_tests}, Max Time: {max_time}, Total time: {total_time}")
    return (score, max_time, total_time)
    

def main():
    # will judge the current solution first, and then judge the submission with solution time + 0.1s
    solution_score = judge_submission_file(problem_name)

    if solution_score[0] != number_of_tests:
        print("There's a problem with solution file")
        return
    
    judge_submission_file("submission",solution_score[1]+0.1)


if __name__ == "__main__":
    main()