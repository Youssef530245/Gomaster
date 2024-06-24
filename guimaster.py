import tkinter as tk
from tkinter import filedialog, scrolledtext
import requests
from requests_futures.sessions import FuturesSession
import concurrent.futures
import threading

# Directory brute-forcing function
def check_directory(ip, word_list, results_text):
    session = FuturesSession()

    def fetch(url):
        try:
            response = session.get(url).result()
            if response.status_code == 200:
                results_text.insert(tk.END, f"Found directory: {url}\n")
                results_text.see(tk.END)  # Scroll to the end
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

# Function to start the brute-forcing process in a new thread
def start_bruteforce():
    ip = ip_entry.get()
    wordlist_path = wordlist_entry.get()

    try:
        with open(wordlist_path, 'r') as file:
            word_list = file.readlines()
    except FileNotFoundError:
        results_text.insert(tk.END, f"File not found: {wordlist_path}\n")
        return

    results_text.insert(tk.END, "Starting directory brute-forcing...\n")
    threading.Thread(target=check_directory, args=(ip, word_list, results_text)).start()

# Function to browse and select the word list file
def browse_file():
    file_path = filedialog.askopenfilename()
    wordlist_entry.delete(0, tk.END)
    wordlist_entry.insert(0, file_path)

# GUI setup
root = tk.Tk()
root.title("Directory B-Forcing Tool (Eng:youssef)")

tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Word List File:").grid(row=1, column=0, padx=10, pady=10)
wordlist_entry = tk.Entry(root)
wordlist_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, padx=10, pady=10)

start_button = tk.Button(root, text="Start", command=start_bruteforce)
start_button.grid(row=2, column=1, padx=10, pady=10)

results_text = scrolledtext.ScrolledText(root, width=50, height=20)
results_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
