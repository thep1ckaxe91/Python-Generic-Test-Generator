import sys

def check(inp, out, ans):
    # inp: input file content
    # out: user output file content
    # ans: correct output file content
    # return True if correct, False otherwise
    return out.strip() == ans.strip()

if __name__ == '__main__':
    inp_file = sys.argv[1]
    out_file = sys.argv[2]
    ans_file = sys.argv[3]

    with open(inp_file, 'r') as f:
        inp = f.read()
    with open(out_file, 'r') as f:
        out = f.read()
    with open(ans_file, 'r') as f:
        ans = f.read()

    if check(inp, out, ans):
        sys.exit(0)
    else:
        sys.exit(1)
