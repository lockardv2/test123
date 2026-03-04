#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
가위바위보 게임 (Rock-Paper-Scissors Game)
플레이어 vs 컴퓨터
"""

import random
import sys


class RockPaperScissors:
    """가위바위보 게임 클래스"""

    def __init__(self):
        self.choices = {
            '1': '가위',
            '2': '바위',
            '3': '보'
        }
        self.player_score = 0
        self.computer_score = 0
        self.tie_count = 0

    def get_computer_choice(self):
        """컴퓨터의 선택을 랜덤하게 반환"""
        return random.choice(list(self.choices.values()))

    def get_player_choice(self):
        """플레이어의 선택을 입력받음"""
        print("\n=== 선택하세요 ===")
        print("1. 가위")
        print("2. 바위")
        print("3. 보")
        print("q. 게임 종료")
        print("==================")

        while True:
            choice = input("선택 (1-3, q): ").strip()

            if choice.lower() == 'q':
                return None

            if choice in self.choices:
                return self.choices[choice]

            print("잘못된 입력입니다. 1, 2, 3 중 하나를 선택하세요.")

    def determine_winner(self, player, computer):
        """승자를 결정"""
        if player == computer:
            return "무승부"

        winning_combinations = {
            '가위': '보',
            '바위': '가위',
            '보': '바위'
        }

        if winning_combinations[player] == computer:
            return "플레이어"
        else:
            return "컴퓨터"

    def update_score(self, result):
        """점수 업데이트"""
        if result == "플레이어":
            self.player_score += 1
        elif result == "컴퓨터":
            self.computer_score += 1
        else:
            self.tie_count += 1

    def display_result(self, player_choice, computer_choice, result):
        """결과 출력"""
        print(f"\n플레이어: {player_choice}")
        print(f"컴퓨터: {computer_choice}")
        print(f"결과: {result}!")

    def display_score(self):
        """현재 점수 출력"""
        print("\n" + "="*40)
        print(f"플레이어: {self.player_score} | 컴퓨터: {self.computer_score} | 무승부: {self.tie_count}")
        print("="*40)

    def play_round(self):
        """한 라운드 진행"""
        player_choice = self.get_player_choice()

        if player_choice is None:
            return False

        computer_choice = self.get_computer_choice()
        result = self.determine_winner(player_choice, computer_choice)

        self.update_score(result)
        self.display_result(player_choice, computer_choice, result)
        self.display_score()

        return True

    def play(self):
        """게임 시작"""
        print("\n" + "="*40)
        print("🎮 가위바위보 게임에 오신 것을 환영합니다! 🎮")
        print("="*40)

        while True:
            if not self.play_round():
                break

        self.display_final_results()

    def display_final_results(self):
        """최종 결과 출력"""
        print("\n" + "="*40)
        print("게임 종료!")
        print("="*40)
        print(f"최종 점수:")
        print(f"  플레이어: {self.player_score}")
        print(f"  컴퓨터: {self.computer_score}")
        print(f"  무승부: {self.tie_count}")

        if self.player_score > self.computer_score:
            print("\n🎉 축하합니다! 플레이어 승리! 🎉")
        elif self.player_score < self.computer_score:
            print("\n💻 컴퓨터 승리! 다음에 다시 도전하세요!")
        else:
            print("\n🤝 전체적으로 무승부입니다!")
        print("="*40 + "\n")


def main():
    """메인 함수"""
    try:
        game = RockPaperScissors()
        game.play()
    except KeyboardInterrupt:
        print("\n\n게임이 중단되었습니다.")
        sys.exit(0)


if __name__ == "__main__":
    main()
