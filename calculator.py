def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b

def calculator():
    print("=== 간단한 계산기 ===")
    print("연산자: +, -, *, /")
    print("종료하려면 'q'를 입력하세요.\n")

    while True:
        user_input = input("계산식 입력 (예: 3 + 4): ").strip()

        if user_input.lower() == 'q':
            print("계산기를 종료합니다.")
            break

        try:
            parts = user_input.split()
            if len(parts) != 3:
                print("올바른 형식으로 입력하세요. 예: 3 + 4\n")
                continue

            a, operator, b = parts
            a, b = float(a), float(b)

            if operator == '+':
                result = add(a, b)
            elif operator == '-':
                result = subtract(a, b)
            elif operator == '*':
                result = multiply(a, b)
            elif operator == '/':
                result = divide(a, b)
            else:
                print(f"지원하지 않는 연산자: {operator}\n")
                continue

            # 정수면 정수로, 소수면 소수로 출력
            if result == int(result):
                print(f"결과: {int(result)}\n")
            else:
                print(f"결과: {result}\n")

        except ValueError as e:
            print(f"오류: {e}\n")
        except Exception:
            print("올바른 숫자를 입력하세요.\n")

if __name__ == "__main__":
    calculator()
