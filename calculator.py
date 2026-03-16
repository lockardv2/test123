import operator as op


def _divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


OPERATORS = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': _divide,
}


def calculator():
    print("=== 간단한 계산기 ===")
    print("연산자: +, -, *, /")
    print("종료하려면 'q'를 입력하세요.\n")

    while True:
        user_input = input("계산식 입력 (예: 3 + 4): ")

        if user_input.strip() in ('q', 'Q'):
            print("계산기를 종료합니다.")
            break

        try:
            parts = user_input.split()
            if len(parts) != 3:
                print("올바른 형식으로 입력하세요. 예: 3 + 4\n")
                continue

            a_str, operator, b_str = parts

            if operator not in OPERATORS:
                print(f"지원하지 않는 연산자: {operator}\n")
                continue

            a, b = float(a_str), float(b_str)
            result = OPERATORS[operator](a, b)

            print(f"결과: {int(result) if result.is_integer() else result}\n")

        except ValueError as e:
            print(f"오류: {e}\n")


if __name__ == "__main__":
    calculator()
