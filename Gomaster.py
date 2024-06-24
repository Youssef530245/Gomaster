import requests
from requests_futures.sessions import FuturesSession
import concurrent.futures
import os
import pyfiglet



print()
def display_center(text):
    # Get terminal width
    terminal_width = os.get_terminal_size().columns
    
    # Calculate left padding to center the text
    left_padding = (terminal_width - len(text)) // 3
    
    # Display text with padding
    print(" " * left_padding + text)

def main():
    text = "Gomaster"
    banner = pyfiglet.figlet_format(text, font="big", width=160)
    display_center(banner)
    display_center("-----------------------------------")
    display_center("--- Made by Eng Youssef Mohamed ---")
    display_center("-----------------------------------")
    display_center("-----------------------------------")
    display_center("---   github.com/Youssef530245  ---")
    display_center("-----------------------------------")
    print() 
    print()
if __name__ == "__main__":
    main()
####---------------------------------------------------------###


# Directory brute-forcing function
def check_directory(ip, word_list):
    session = FuturesSession()
    
    def fetch(url):
        try:
            response = session.get(url).result()
            if response.status_code == 200:
                print(f"Found directory: {url}")
        except requests.exceptions.RequestException:
            # Ignore the URL if an error occurs
            pass

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for word in word_list:
            url = f"http://{ip}/{word.strip()}"
            futures.append(executor.submit(fetch, url))
        
        for future in concurrent.futures.as_completed(futures):
            pass  # Just to ensure all tasks are completed

def main():
    ip = input("Enter the IP address: ")
    wordlist_path = input("Enter the path to the word list file: ")

    try:
        with open(wordlist_path, 'r') as file:
            word_list = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {wordlist_path}")
        return

    print("Starting directory brute-forcing...")
    check_directory(ip, word_list)
    print("Directory brute-forcing completed.")

if __name__ == "__main__":
    main()
