import sys

def show_menu():
    """
    Shows menu
    """
    menu = []
    menu.append("*"*25)
    menu.append("Usage: controller.py <command>")
    menu.append("Available commands:")
    menu.append(" * [full-update]       - reads all mails and updates stored data")
    menu.append(" * [usual-update]      - reads only new mails")
    menu.append(" * [clear-all --force] - removes database")
    menu.append(" * [site-check]        - goes through saved offers and checks for updates on webpage")
    menu.append("*"*25)
    print("\n".join(menu))


if __name__ == "__main__":
    print("arguments: ", sys.argv)
    show_menu()