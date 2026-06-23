import time
import random

text = "안녕하세요"

for char in text:
    print(char, end='', flush=True)
    time.sleep(0.5)
print()

print("\n간단한 숫자 맞추기 게임을 시작합니다!")
target = random.randint(1, 100)
attempts = 0

while True:
    try:
        guess_input = input("\n1부터 100 사이의 숫자를 맞춰보세요: ")
        guess = int(guess_input)

        if not 1 <= guess <= 100:
            print("잘못된 입력입니다. 1과 100 사이의 숫자를 입력해주세요.")
            continue

        attempts += 1

        if guess < target:
            print("더 큰 숫자입니다!")
        elif guess > target:
            print("더 작은 숫자입니다!")
        else:
            print(f"\n축하합니다! {attempts}번 만에 숫자를 맞추셨습니다!")
            break
    except ValueError:
        print("잘못된 입력입니다. 숫자를 입력해주세요.")