from quiz import Quiz
import json
import random
from datetime import datetime

class QuizGame:

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.history = []
        self.load_state()

    def init_quizzes(self) :
        self.quizzes = [
            Quiz("대한민국의 수도는?",["서울", "부산", "대구", "인천"],1, "한강이 흐르는 곳"),
            Quiz("파이썬의 창시자는?", ["귀도 반 로섬", "제임스 고슬링", "비야네", "데니스 리치"],1, "게임 캐릭터 이름 같습니다."),
            Quiz("축구 감독인 사람은?", ["아카자", "홍명보", "펩시콜라", "펩"], 4, "대머리"),
            Quiz("코디세이의 위치는?", ["평양", "쓰촨성", "약간포동", "개포동"], 4, "3번 아니면 4번"),
            Quiz("학습 네이토의 정체는?", ["깡통", "할루시네이션", "AI Chat Bot", "네이트"],3, "ACB"),
        ]

    def run(self):
        try :
            while True:
                self.show_menu()

                menu = self.get_menu()

                if menu == 1:
                    self.play_quiz()

                elif menu == 2:
                    self.add_quiz()

                elif menu == 3:
                    self.show_quiz_list()

                elif menu == 4:
                    self.show_best_score()
                elif menu == 5 :
                    self.delete_quiz()
                elif menu == 6 :
                    self.print_history()

                elif menu == 0:
                    self.save_state()
                    print("프로그램 종료")
                    break
        except (KeyboardInterrupt, EOFError) :
            print("\n 프로그램을 안전하게 종료합니다.")
            self.save_state()

    def show_menu(self):
            print("""
==========================
Quiz Game
==========================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 최고 점수
5. 퀴즈 삭제
6. 점수 기록 보기
0. 종료
==========================
""")

    def get_menu(self):
            while True:
                try:
                    menu = int(input("메뉴를 선택하세요: "))

                    if 0 <= menu <= 6:
                        return menu

                    print("0~4 사이의 숫자를 입력하세요.")

                except ValueError:
                    print("숫자를 입력하세요.")

    def play_quiz(self):
        score = 0.0

        print("\n===== 퀴즈 시작 =====")

        while True:
            try:
                count = int(input(f"몇 문제를 푸시겠습니까? (1~{len(self.quizzes)}) : "))

                if 1 <= count <= len(self.quizzes):
                    break

                print(f"1~{len(self.quizzes)} 사이의 숫자를 입력하세요.")

            except ValueError:
                print("숫자를 입력하세요.")

        random_quizzes = random.sample(self.quizzes, count)

        for i, quiz in enumerate(random_quizzes, start=1):
            print(f"\n[{i}번 문제]")

            quiz.print_quiz()

            hint_used = False

            while True :
                choice = input("힌트를 보시겠습니까? (y/n) : ").lower()

                if choice == 'y' :
                    quiz.print_hint()
                    hint_used = True
                    break
                elif choice == 'n' :
                    break
                else :
                    print("y 또는 n을 입력해주세요")

            while True :
                try :
                    answer = int(input("정답 번호를 입력하세요 : "))
                    if 1 <= answer <=4 :
                        break
                    print("1~4를 입력하세요")
                except ValueError :
                    print("숫자를 입력하세요")

            if quiz.check_answer(answer):
                print("정답입니다!")

                if hint_used :
                    score += 0.5
                else :
                    score +=1

            else:
                print(f"오답입니다! 정답은 {quiz.get_answer()}번 입니다.")

        print("\n===== 퀴즈 종료 =====")
        print(f"점수 : {score} / {count}")

        self.save_history(count, score)

        if score > self.best_score:
            self.best_score = score
            print("🎉 최고 점수가 갱신되었습니다!")
        else :
            print("최고 점수는 갱신되지 않았습니다.")

        self.save_state()

    def add_quiz(self):
        while True:
            question = input("문제 : ").strip()

            if question:
                break

            print("문제를 입력하세요.")

        choices = []

        for i in range(1, 5):
            while True:
                choice = input(f"{i}번 보기 : ").strip()

                if choice:
                    choices.append(choice)
                    break

                print("보기를 입력하세요.")

        while True :
            try :
                answer = int(input("정답 번호 : "))
                if 1<= answer <= 4 :
                    break
                print("1~4를 입력하세요")
            except ValueError :
                print("숫자를 입력하세요")

        while True :
            hint = input("힌트 : ").strip()

            if hint :
                break
            print("힌트를 입력하세요")

        quiz = Quiz(question, choices, answer, hint)

        self.quizzes.append(quiz)
        self.save_state()

        print("퀴즈가 추가되었습니다.")

    def show_quiz_list(self):
        print("\n===== 퀴즈 목록 =====")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{i}]")
            quiz.print_quiz()
            print(f"정답 : {quiz.get_answer()}번")

    def show_best_score(self):
        print(f"\n현재 최고 점수 : {self.best_score}")

    def delete_quiz(self) :
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quiz_list()

        while True:
            try:
                num = int(input("\n삭제할 퀴즈 번호를 입력하세요 : "))

                if 1 <= num <= len(self.quizzes):
                    break

                print(f"1~{len(self.quizzes)} 사이의 번호를 입력하세요.")

            except ValueError:
                print("숫자를 입력하세요.")
        confirm = input("정말 삭제하겠습니까? (y/n) : ").lower()

        if confirm != 'y' :
            print("삭제가 취소되었습니다.")
            return

        deleted = self.quizzes.pop(num - 1)

        self.save_state()

        print(f"'{deleted.question}' 퀴즈가 삭제되었습니다.")

    def save_state(self):
        data = {
                "best_score": self.best_score,
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "history": self.history}

        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_state(self):
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.best_score = data["best_score"]

            self.history = data.get("history", [])

            self.quizzes = []

            for quiz_data in data["quizzes"]:
                quiz = Quiz(
                    quiz_data["question"],
                    quiz_data["choices"],
                    quiz_data["answer"],
                    quiz_data["hint"]
                    )

                self.quizzes.append(quiz)

        except FileNotFoundError:
            print("저장 파일이 없습니다. 기본 퀴즈를 생성합니다.")
            self.init_quizzes()
            self.save_state()

        except json.JSONDecodeError:
            print("저장 파일이 손상되었습니다. 기본 퀴즈로 복구합니다.")
            self.init_quizzes()
            self.save_state()

    def save_history(self, quiz_count, score) :
        history = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "quiz_count": quiz_count,
            "score": score
        }
        self.history.append(history)

    def print_history(self):
        if not self.history:
            print("저장된 기록이 없습니다.")
            return

        print("\n===== 점수 기록 =====")

        for i, history in enumerate(self.history, start=1):
            print(f"[{i}]")
            print(f"날짜 : {history['datetime']}")
            print(f"푼 문제 수 : {history['quiz_count']}")
            print(f"점수 : {history['score']}")
            print()
