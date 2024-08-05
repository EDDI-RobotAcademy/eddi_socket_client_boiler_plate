from colorama import init, Fore, Style

init()


class ColorPrinter:
    @staticmethod
    def print_important_message(text):
        print(f"{Fore.RED}{text}{Style.RESET_ALL}")

    @staticmethod
    def print_important_data(redText, greenText):
        print(f"{Fore.RED}{redText}: {Fore.GREEN}{greenText}{Style.RESET_ALL}")
