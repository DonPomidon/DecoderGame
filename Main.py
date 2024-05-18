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
        self.a = ""
        self.list1 = []
        self.list2 = []

    def count_result(self, secret_code, guess):
        """
        Вираховуємо співпадіння.
        """
        self.a = ""
        self.list1 = []
        self.list2 = []

        for i in range(4):
            if secret_code[i] == guess[i]:
                self.a += "+"
            else:
                self.list1.append(secret_code[i])
                self.list2.append(guess[i])

        for i in self.list1:
            for j in self.list2:
                if i == j:
                    self.list2.remove(i)
                    self.a += "-"
                    break

    def result(self):
        """
        Виводимо результат.
        """
        return self.a


class Statistic:
    def __init__(self):
        """
        Статистика гри.

        :param total_wins: Загальна кількість програшів.
        :param total_lose: Загальна кількість виграшів.
        """
        self.total_wins, self.total_lose = self.load_from_file()
        if os.path.isfile('Result.txt'):
            try:
                with open('Result.txt', 'r', encoding='utf-8') as file:
                    file.read()
                    return
            except FileNotFoundError:
                self.save_to_file()
        else:
            self.save_to_file()

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
        try:
            with open('Result.txt', 'r', encoding='utf-8') as file:
                data = file.read().strip().split(', ')
                self.total_wins = int(data[0].split(': ')[1])
                self.total_lose = int(data[1].split(': ')[1])
                return self.total_wins, self.total_lose
        except FileNotFoundError:
            return 0, 0

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
        :param result: Записуємо результати гри.
        """
        self.secret_code = GenerateRandomNumber()
        self.analyze = Analyze()
        self.win = "++++"
        self.result = GameResults(self)

    def start_new_game(self):
        """
        Створюємо нову гру.
        """
        self.secret_code = GenerateRandomNumber()
        self.play_game()

    def play_game(self):
        """
        Починаємо нову гру.
        """
        pass

    def easy_game(self):
        """
        Гра на легкій складності.
        """
        self.game(8, 2)
        self.play_game()

    def medium_game(self):
        """
        Гра на середній складності.
        """
        self.game(6, 2)
        self.play_game()

    def hard_game(self):
        """
        Гра на тяжкій складності.
        """
        self.game(4, 1)
        self.play_game()

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
                print(f"\nРезультат: {self.analyze.result()}")
                attempts -= 1
                if self.analyze.result() == self.win:
                    self.result.add_result(True)
                    return
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
        self.result.add_result(False)
        return


class GameResults:
    def __init__(self, games):
        """
        Додаємо результати гри в статистику.

        :param games: Приймаємо об'єкт гри.
        """
        self.game = games

    def add_result(self, win):
        """
        Додаємо виграши та програші.
        """
        if win:
            stat.add_win()
        else:
            stat.add_lose()
            print(f"\nВи використали всі спроби! Таємний код був: {self.game.secret_code.return_number()}")
        self.ask_replay()

    def ask_replay(self):
        """
        Перезапуск гри.
        """
        user_again = input("\nХочете зіграти ще раз?(Так або Ні) ")
        if user_again == "Так":
            self.game.start_new_game()
        elif user_again == "Ні":
            print("\nДякуємо за гру! Повертаємо вас у головне меню.")
            play_game()
        else:
            print("\nНеправильний вибір!")
            self.ask_replay()


def play_game():
    """
    Функція управління грою.

    :param stat: Підтягуємо статистику.
    :param rules: Підтягуємо правила гри.
    """
    global stat
    rules = Rules
    print("\nПривіт!\n")
    print("Раді вітати вас у грі Дешифратор!\n")
    print("Головне меню:\n Грати\n Правила\n Статистика\n Вихід\n")
    user_input = input("Ваш вибір: ")

    if user_input == "Грати":
        while True:
            print("\nСкладність: \nЛегко(У вас 8 спроб та 2 підказки) \nСередній(У вас 6 спроб та 2 підказки) \nТяжко(У вас 4 спроби і 1 підказка)")
            difficult = ""
            while not (difficult == "Легко" or difficult == "Середній" or difficult == "Тяжко"):
                difficult = input("\nВиберіть складність: ")
                game = Game()
                if difficult == "Легко":
                    game.easy_game()

                elif difficult == "Середній":
                    game.medium_game()

                elif difficult == "Тяжко":
                    game.hard_game()

                else:
                    print("Неправильний вибір! Будь-ласка виберіть складність.")

    elif user_input == "Правила":
        print("\nПравила гри:")
        rules.rules()
        play_game()

    elif user_input == "Статистика":
        stat.print_result()
        play_game()

    elif user_input == "Вихід":
        exit()

    else:
        print("Неправильний вибір!")
        play_game()


if __name__ == "__main__":
    stat = Statistic()
    play_game()
