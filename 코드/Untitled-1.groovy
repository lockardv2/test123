// 간단한 캘린더 앱 (HTML+JS, 브라우저 콘솔에서 동작)
class SimpleCalendar {
    constructor(year, month) {
        this.year = year;
        this.month = month; // 1~12
    }

    getFirstDayOfWeek() {
        // 0: Sunday, ... 6: Saturday
        return new Date(this.year, this.month - 1, 1).getDay();
    }

    getDaysInMonth() {
        return new Date(this.year, this.month, 0).getDate();
    }

    render() {
        const days = this.getDaysInMonth();
        const startDay = this.getFirstDayOfWeek();

        let calendar = "일 월 화 수 목 금 토\n";
        let dayCount = 0;

        // 첫줄 공백 채우기
        for (let i = 0; i < startDay; i++) {
            calendar += "   ";
            dayCount++;
        }

        for (let d = 1; d <= days; d++) {
            calendar += (d < 10 ? " " : "") + d + " ";
            dayCount++;
            if (dayCount % 7 === 0) calendar += "\n";
        }

        return calendar;
    }
}

// 사용 예시:
const cal = new SimpleCalendar(2024, 6);
console.log(cal.render());

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
1234567890
1234567890 
hello world
Thread.startDaemon {
    println("Hello, World!")
    println("Hello, World!")
    println("Hello, World!")
}
Thread.startDaemon {
    println("Hello, World!")
    println("Hello, World!")
    println("Hello, World!")
}
