
# main.py
import os
from Aviral.myrepl.repl import repl

def main():
    user_name = os.getlogin()

    print(f"Hello {user_name}! This is the Monkey programming language!")
    print("Feel free to type in commands")

    repl.start()

if __name__ == "__main__":
    main()
