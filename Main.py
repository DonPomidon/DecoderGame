import random
import os
import Rules


class GenerateRandomNumber:
    def __init__(self):
        """
        Генерація таємного коду.
        """
        self.random_code = [random.randint(1, 6) for _ in range(4)]

    def return_number(self):
        """
        Вивід коду.
        """
        return self.random_code


class Analyze:
    def __init__(self):
        """
        Аналізатор кодів кододавця і гравця.

        :param a: Результат.
        :param list1: Відсіюємо залишок коду кододавця.
        :param list2: Відсіюємо залишок коду гравця.
        """
        self.result = ""
        self.list1 = []
        self.list2 = []

    def count_result(self, secret_code, guess):
        """
        Вираховуємо співпадіння.
        """
        self.result = ""
        self.list1 = []
        self.list2 = []

        for i in range(4):
            if secret_code[i] == guess[i]:
                self.result += "+"
            else:
                self.list1.append(secret_code[i])
                self.list2.append(guess[i])

        for i in self.list1:
            for j in self.list2:
                if i == j:
                    self.list2.remove(i)
                    self.result += "-"
                    break

    def print_result(self):
        """
        Виводимо результат.
        """
        return self.result


class Statistic:
    def __init__(self):
        """
        Статистика гри.

        :param total_wins: Загальна кількість програшів.
        :param total_lose: Загальна кількість виграшів.
        """
        self.total_wins, self.total_lose = self.load_from_file()

    def add_win(self):
        """
        Додаємо виграш.
        """
        self.total_wins += 1
        self.save_to_file()

    def add_lose(self):
        """
        Додаємо програш.
        """
        self.total_lose += 1
        self.save_to_file()

    def save_to_file(self):
        """
        Зберігаємо результати у файл.
        """
        with open('Result.txt', 'w', encoding='utf-8') as file:
            file.write(f"Загальна кількість виграшів: {self.total_wins}, програшів: {self.total_lose}")

    def load_from_file(self):
        """
        Завантажуємо результати з файлу.
        """
        if os.path.isfile('Result.txt'):
            try:
                with open('Result.txt', 'r', encoding='utf-8') as file:
                    file.read()
                try:
                    with open('Result.txt', 'r', encoding='utf-8') as file:
                        data = file.read().strip().split(', ')
                        self.total_wins = int(data[0].split(': ')[1])
                        self.total_lose = int(data[1].split(': ')[1])
                except FileNotFoundError:
                    return 0, 0
                return self.total_wins, self.total_lose
            except FileNotFoundError:
                self.save_to_file()
        else:
            self.save_to_file()

    def print_result(self):
        """
        Виводимо результат.
        """
        try:
            with open('Result.txt', 'r', encoding='utf-8') as file:
                print(file.read())
        except FileNotFoundError:
            self.save_to_file()


class Game:
    def __init__(self):
        """
        Тіло гри.

        :param secret_code: Генеруємо секретний код.
        :param analyze: Аналізуємо результати.
        :param win: Значення яке потрібне для виграшу.
        :param stat: Взаємодіємо з статистикою.
        :param rules: Підтягуємо правила гри.
        :param user_input: Взаємодія користувача з головним меню.
        """
        self.secret_code = GenerateRandomNumber()
        self.analyze = Analyze()
        self.win = "++++"
        self.rules = Rules
        self.user_input = ""
        self.stat = Statistic()

    def start_game(self):
        """
        Запуск гри.
        """
        print("\nПривіт!\n")
        print("Раді вітати вас у грі Дешифратор!\n")
        self.main_menu()

    def main_menu(self):
        """
        Головне меню.
        """
        print("\nГоловне меню:\n Грати\n Правила\n Статистика\n Вихід\n")
        self.user_input = input("Ваш вибір: ")

        if self.user_input == "Грати":
            self.play_game()

        elif self.user_input == "Правила":
            print("\nПравила гри:")
            self.rules.rules()
            self.main_menu()

        elif self.user_input == "Статистика":
            self.stat.print_result()
            self.main_menu()

        elif self.user_input == "Вихід":
            exit()

        else:
            print("Неправильний вибір!")
            self.main_menu()

    @staticmethod
    def difficulty():
        """
        Види складності гри.
        """
        return {
            "Легко" : (8, 2),
            "Середній" : (6, 2),
            "Тяжко" : (4, 1)
        }

    def choose_difficulty(self):
        """
        Вибір складності гри.
        """
        difficulties = self.difficulty()
        print("\nОберіть складність: ")
        for level in difficulties:
            print(f"{level} (спроб: {difficulties[level][0]}, підказок: {difficulties[level][1]})")

        while True:
            choice = input("\nОберіть складність: ")
            if choice in difficulties:
                return difficulties[choice]
            else:
                print("Неправильний вибір! Будь-ласка оберіть складність.")

    def play_game(self):
        """
        Генерація нової гри.
        """
        self.secret_code = GenerateRandomNumber()
        attempts, hints = self.choose_difficulty()
        self.game(attempts, hints)

    def game(self, attempts, hints):
        """
        Логіка гри.
        """
        print("\nПочинаємо гру!")
        while attempts > 0:
            guess = input("Виберіть чотири числа від 1 до 6: ")
            if len(guess) == 4 and all(x.isdigit() and 1 <= int(x) <= 6 for x in guess):
                guess_numbers = [int(x) for x in guess]
                self.analyze.count_result(self.secret_code.return_number(), guess_numbers)
                print(f"\nРезультат: {self.analyze.print_result()}")
                attempts -= 1
                if self.analyze.print_result() == self.win:
                    print("Вітаємо! Ви перемогли!")
                    self.stat.add_win()
                    self.ask_replay()
                else:
                    print(f"\nУ вас залишилось спроб: {attempts}")
                    while hints > 0:
                        hint = input("\nХочете використати підказку?(Так або Ні) ")
                        if hint == "Так":
                            hints -= 1
                            print(f"\nЦифра в таємному коді: {random.choice(self.secret_code.return_number())}")
                            break
                        elif hint == "Ні":
                            print(f"\nУ вас залишилось підказок: {hints}")
                            break
                        else:
                            print("Неправильний вибір! Будь-ласка вкажіть Так або Ні.")
            else:
                print("Неправильний формат коду! Будь-ласка ведіть 4 цифри в діапазоні від 1 до 6")
        print(f"\nВи використали всі спроби! Таємний код був: {self.secret_code.return_number()}")
        self.stat.add_lose()
        self.ask_replay()

    def ask_replay(self):
        """
        Перезапуск гри.
        """
        user_again = input("\nХочете зіграти ще раз?(Так або Ні) ")
        if user_again == "Так":
            self.play_game()
        elif user_again == "Ні":
            print("\nДякуємо за гру! Повертаємо вас у головне меню.")
            self.main_menu()
        else:
            print("\nНеправильний вибір!")
            self.ask_replay()


if __name__ == "__main__":
    game = Game()
    game.start_game()
