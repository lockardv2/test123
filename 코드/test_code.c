#include <stdio.h>

int is_leap_year(int year) {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

int get_days_in_month(int year, int month) {
    int days_in_month[] = {31,28,31,30,31,30,31,31,30,31,30,31};
    if (month == 2 && is_leap_year(year))
        return 29;
    return days_in_month[month - 1];
}

int get_weekday(int year, int month, int day) {
    // Zeller's Congruence
    if (month < 3) {
        month += 12;
        year -= 1;
    }
    int K = year % 100;
    int J = year / 100;
    int h = (day + 13 * (month + 1) / 5 + K + K / 4 + J / 4 + 5 * J) % 7;
    // 0=Saturday, 1=Sunday, ..., 6=Friday
    return (h + 6) % 7; // 0=Sunday
}

void print_calendar(int year, int month) {
    printf("     %d년 %d월\n", year, month);
    printf(" 일 월 화 수 목 금 토\n");

    int first_day = get_weekday(year, month, 1);
    int days = get_days_in_month(year, month);

    // Print leading spaces
    for (int i = 0; i < first_day; i++)
        printf("   ");

    for (int day = 1; day <= days; day++) {
        printf("%3d", day);
        if ((first_day + day) % 7 == 0)
            printf("\n");
    }
    printf("\n");
}

int main() {
    int year, month;
    printf("년과 월을 입력하세요 (예: 2024 6): ");
    scanf("%d %d", &year, &month);

    if (year < 1 || month < 1 || month > 12) {
        printf("올바른 년과 월을 입력하세요.\n");
        return 1;
    }

    print_calendar(year, month);
    return 0;
}

/*
    2024년 6월
  일 월 화 수 목 금 토
        1  2  3  4  5  6
  7  8  9 10 11 12 13
 14 15 16 17 18 19 20
 21 22 23 24 25 26 27
 28 29 30
*/  

/*
    2024년 6월
  일 월 화 수 목 금 토
        1  2  3  4  5  6
  7  8  9 10 11 12 13
 14 15 16 17 18 19 20
 21 22 23 24 25 26 27
 28 29 30
*/  

정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1
정답: 1

다음 코드의 출력 결과는 무엇인가?
#include <stdio.h>

int main() {
    int x = 10;
    int y = 20;
    int z = 30;
    printf("%d %d %d\n", x, y, z);
    return 0;
}


정답: 10 20 30

다음 코드의 출력 결과는 무엇인가?
#include <stdio.h>
int main() {
    int x = 10;
    int y = 20;
    int z = 30;
    printf("%d %d %d\n", x, y, z);
    return 0;
}

abcdefg
hhhhhhh
jjjjjjj
kkkkkkk
lllllll