import getpass
from sagar.my_repl import repl

def main():
    user = getpass.getuser()

    print(f"Hello Mr {user}. Welcome to Monkey programming language.")
    print("Feel free to try this:")

    repl.start()

if __name__ == "__main__":
    main()

