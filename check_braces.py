import sys

def check_braces(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    stack = []
    line_num = 1
    for char in content:
        if char == '{':
            stack.append(line_num)
        elif char == '}':
            if not stack:
                print(f"Error: Unmatched '}}' at line {line_num} in {filepath}")
                return False
            stack.pop()
        if char == '\n':
            line_num += 1

    if stack:
        print(f"Error: Unmatched '{{' opened at line {stack[-1]} in {filepath}")
        return False

    print(f"Success: Braces balanced in {filepath}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_braces.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    check_braces(filepath)
