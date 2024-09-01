import argparse
import os
import logging
import colorama
import sys
from colorama import Fore, Style
from urllib.parse import urlparse, parse_qs, urlencode
import client  # Importing client from a module named "client"

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

# Configure logging
log_format = '%(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)
logging.getLogger('').handlers[0].setFormatter(logging.Formatter(log_format))

# Hardcoded file extensions to filter out
HARDCODED_EXTENSIONS = [
    ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json",
    ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", ".otf", ".mp4", ".txt"
]

class CustomArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        log_text = """
        >>================================================================<<
        ||                         EasyFuzzScan Tool                     ||
        ||================================================================||
        ||    Mine URLs from the Wayback Machine and clean them up.       ||
        ||----------------------------------------------------------------||
        || Usage Options:                                                 ||
        ||    --domain        : Specify a domain to mine URLs.            ||
        ||    --list          : File with a list of domains.              ||
        ||    --stream        : Stream URLs in real-time.                 ||
        ||    --proxy         : Set a proxy address for web requests.     ||
        ||    --placeholder   : Placeholder for parameter values.         ||
        ||----------------------------------------------------------------||
        ||  Example:                                                      ||
        ||    python Fuzzing.py --domain example.com --stream             ||
        ||----------------------------------------------------------------||
        ||                    Steal with passion by @Awiones              ||
        >>================================================================<<
        """
        return Fore.MAGENTA + log_text + Style.RESET_ALL



def has_extension(url, extensions):
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()
    return extension in extensions

def clean_url(url):
    parsed_url = urlparse(url)
    if (parsed_url.port == 80 and parsed_url.scheme == "http") or (parsed_url.port == 443 and parsed_url.scheme == "https"):
        parsed_url = parsed_url._replace(netloc=parsed_url.netloc.rsplit(":", 1)[0])
    return parsed_url.geturl()

def clean_urls(urls, extensions, placeholder):
    cleaned_urls = set()
    for url in urls:
        cleaned_url = clean_url(url)
        if not has_extension(cleaned_url, extensions):
            parsed_url = urlparse(cleaned_url)
            query_params = parse_qs(parsed_url.query)
            cleaned_params = {key: placeholder for key in query_params}
            cleaned_query = urlencode(cleaned_params, doseq=True)
            cleaned_url = parsed_url._replace(query=cleaned_query).geturl()
            cleaned_urls.add(cleaned_url)
    return list(cleaned_urls)

def fetch_and_clean_urls(domain, extensions, stream_output, proxy, placeholder):
    logging.info(f"{Fore.MAGENTA}[Starting]{Style.RESET_ALL} Fetching URLs for {Fore.CYAN + domain + Style.RESET_ALL}")
    wayback_uri = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&collapse=urlkey&fl=original&page=/"
    response = client.fetch_url_content(wayback_uri, proxy)
    urls = response.text.split()
    
    logging.info(f"{Fore.MAGENTA}[Gather]{Style.RESET_ALL} Found {Fore.GREEN + str(len(urls)) + Style.RESET_ALL} URLs for {Fore.CYAN + domain + Style.RESET_ALL}")
    
    cleaned_urls = clean_urls(urls, extensions, placeholder)
    logging.info(f"{Fore.MAGENTA}[Cleaing]{Style.RESET_ALL} Cleaning URLs for {Fore.CYAN + domain + Style.RESET_ALL}")
    logging.info(f"{Fore.MAGENTA}[Success]{Style.RESET_ALL} Success Mining! {Fore.GREEN + str(len(cleaned_urls)) + Style.RESET_ALL} URLs after cleaning")
    logging.info(f"{Fore.MAGENTA}[INFO]{Style.RESET_ALL} Extracting URLs with parameters")
    
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    result_file = os.path.join(results_dir, f"{domain}.txt")

    with open(result_file, "w") as f:
        for url in cleaned_urls:
            if "?" in url:
                f.write(url + "\n")
                if stream_output:
                    print(url)
    
    logging.info(f"{Fore.MAGENTA}[INFO]{Style.RESET_ALL} Saved cleaned URLs to {Fore.CYAN + result_file + Style.RESET_ALL}")

def main():
    """
    Main function to handle command-line arguments and start the URL mining process.
    """
    # Checking for short versions
    if "-d" in sys.argv:
        print(Fore.RED + "Did you mean --domain?" + Style.RESET_ALL)
        return
    if "-l" in sys.argv:
        print(Fore.RED + "Did you mean --list?" + Style.RESET_ALL)
        return
    if "-s" in sys.argv:
        print(Fore.RED + "Did you mean --stream?" + Style.RESET_ALL)
        return
    if "-p" in sys.argv:
        print(Fore.RED + "Did you mean --proxy?" + Style.RESET_ALL)
        return

    parser = CustomArgumentParser(
        description="Mining URLs from dark corners of Web Archives",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False  # Disables automatic help
    )

    parser.add_argument("--domain", help="Specify the domain to mine URLs for.")
    parser.add_argument("--list", help="File containing a list of domain names.")
    parser.add_argument("--stream", action="store_true", help="Stream URLs on the terminal.")
    parser.add_argument("--proxy", help="Set the proxy address for web requests.", default=None)
    parser.add_argument("--placeholder", help="Placeholder for parameter values.", default="FUZZ")
    parser.add_argument("--help", "-h", action="help", help="Show this help message and exit.")

    args = parser.parse_args()

    if not args.domain and not args.list:
        print(Fore.RED + "Error: Please provide either --domain or --list." + Style.RESET_ALL)
        parser.print_help()
        return
    
    if args.domain and args.list:
        print(Fore.RED + "Error: Please provide either --domain or --list, not both." + Style.RESET_ALL)
        parser.print_help()
        return



    if args.list:
        with open(args.list, "r") as f:
            domains = [line.strip().lower().replace('https://', '').replace('http://', '') for line in f.readlines()]
            domains = [domain for domain in domains if domain]  # Remove empty lines
            domains = list(set(domains))  # Remove duplicates
    else:
        domain = args.domain

    extensions = HARDCODED_EXTENSIONS

    if args.domain:
        fetch_and_clean_urls(domain, extensions, args.stream, args.proxy, args.placeholder)

    if args.list:
        for domain in domains:
            fetch_and_clean_urls(domain, extensions, args.stream, args.proxy, args.placeholder)

if __name__ == "__main__":
    main()
