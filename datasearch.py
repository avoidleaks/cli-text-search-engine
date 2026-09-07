import os
import sys
import time

TYPE_SPEED = 0.01
FAST_SPEED = 0.003

RESET = "\033[0m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
GREEN = "\033[92m"

ASCII_ART = f"""
{CYAN}

   ██████ ▓█████ ▄▄▄       ██▀███   ▄████▄   ██░ ██ 
▒██    ▒ ▓█   ▀▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▓██░ ██▒
░ ▓██▄   ▒███  ▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒██▀▀██░
  ▒   ██▒▒▓█  ▄░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░▓█ ░██ 
▒██████▒▒░▒████▒▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░░▓█▒░██▓
▒ ▒▓▒ ▒ ░░░ ▒░ ░▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒ ░░▒░▒
░ ░▒  ░ ░ ░ ░  ░ ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒    ▒ ░▒░ ░
░  ░  ░     ░    ░   ▒     ░░   ░ ░         ░  ░░ ░
      ░     ░  ░     ░  ░   ░     ░ ░       ░  ░  ░
                                  ░                
                                      

       Made By : Skill * 
     
                                                                                                                                                                                  
{YELLOW}
      TEXT SEARCH ENGINE
{RESET}
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_ascii():
    print(ASCII_ART)
    time.sleep(0.8)


def dramatic_print(text, speed=TYPE_SPEED, end_pause=0.15):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()
    time.sleep(end_pause)


def pause(seconds=0.6):
    time.sleep(seconds)

def clean_path(path):
    return path.strip().strip('"').strip("'")


def choose_folder():
    while True:
        dramatic_print(" Enter folder path containing .txt files")
        dramatic_print("(type 'q' to quit)", FAST_SPEED)

        folder = clean_path(input("> "))

        if folder.lower() == "q":
            return None

        if os.path.isdir(folder):
            dramatic_print(f"{GREEN}✔ Folder accepted.{RESET}")
            pause()
            return folder

        dramatic_print(f"{RED}✖ Invalid folder path.{RESET}")
        pause()

def list_txt_files(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(".txt")]

    if not files:
        dramatic_print("⚠ No .txt files found.")
        return []

    dramatic_print("\n Available text files:\n", FAST_SPEED)
    for i, file in enumerate(files, 1):
        dramatic_print(f"[{i}] {file}", FAST_SPEED, 0.02)

    return files


def choose_file(files):
    while True:
        dramatic_print("\nChoose a file number (or 'b' to go back):", FAST_SPEED)
        choice = input("> ").strip().lower()

        if choice == "b":
            return None

        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]

        dramatic_print("✖ Invalid choice.")

def search_engine(lines):
    while True:
        dramatic_print("\n SEARCH OPTIONS", FAST_SPEED)
        dramatic_print("[1] Search", FAST_SPEED)
        dramatic_print("[b] Return To Last Option", FAST_SPEED)

        choice = input("> ").strip().lower()

        if choice == "b":
            return

        if choice != "1":
            dramatic_print("✖ Invalid option.")
            continue

        dramatic_print("\nEnter keyword to search:", FAST_SPEED)
        keyword = input("> ").strip()

        if not keyword:
            dramatic_print("✖ Empty keyword.")
            continue

        clear_screen()
        dramatic_print(f" Results for '{keyword}':\n", FAST_SPEED)

        found = False
        keyword_lower = keyword.lower()

        for i, line in enumerate(lines, 1):
            if keyword_lower in line.lower():
                found = True
                highlighted = highlight_text(line.rstrip(), keyword)
                print(f"{CYAN}[Line {i}]{RESET} {highlighted}")

        if not found:
            dramatic_print(f"{RED}❌ No matches found.{RESET}")

        dramatic_print("\n─ End of results ─", FAST_SPEED)

def highlight_text(text, keyword):
    lower_text = text.lower()
    lower_key = keyword.lower()
    result = ""
    i = 0

    while i < len(text):
        if lower_text[i:i+len(keyword)] == lower_key:
            result += f"{YELLOW}{text[i:i+len(keyword)]}{RESET}"
            i += len(keyword)
        else:
            result += text[i]
            i += 1

    return result

def load_file(folder, filename):
    path = os.path.join(folder, filename)

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except Exception as e:
        dramatic_print(f"{RED}✖ Error reading file: {e}{RESET}")
        return None

def main():
    clear_screen()
    print_ascii()
    dramatic_print("=== TEXT SEARCH ENGINE LOADED ===", 0.04, 1.2)

    while True:
        folder = choose_folder()
        if folder is None:
            dramatic_print("\n Exiting...")
            break

        while True:
            clear_screen()
            files = list_txt_files(folder)
            if not files:
                input("\nPress ENTER to choose another folder...")
                break

            filename = choose_file(files)
            if filename is None:
                break

            dramatic_print(f"\n Loading '{filename}'...", FAST_SPEED)
            lines = load_file(folder, filename)
            if lines is None:
                pause()
                continue

            search_engine(lines)

if __name__ == "__main__":
    main()