import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
import pyautogui
import time
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import json
import os

# Configure logging to append to the file
logging.basicConfig(
    filename='mute_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'  # Append mode
)

# File paths and constants
SETTINGS_FILE = 'settings.json'
REQUEST_FILE = 'following.html'

# Load settings or create default settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
    else:
        settings = {}
    
    # Set defaults for missing keys
    settings.setdefault("excluded_ids", [
        "arush.bhimwal", "amex.taken", "arush.onion",
        "majestical.gaming", "horizon.personal.computers", "arcanebyte.games"
    ])
    settings.setdefault("batch_size", 5)  # Default batch size
    return settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file, indent=4)

# Load IDs that were muted in previous runs
def load_already_muted_ids(log_file):
    muted_ids = set()
    try:
        with open(log_file, 'r') as file:
            for line in file:
                if 'Muted' in line:
                    muted_id = line.split('Muted ')[1].split(':')[0]
                    muted_ids.add(muted_id)
    except FileNotFoundError:
        pass
    return muted_ids

# Function to parse the HTML file and extract the list of people
def extract_people_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        people = [a.text for a in soup.find_all('a')]
        return people

# Initialize settings and data
settings = load_settings()
muted_ids = load_already_muted_ids('mute_log.txt')
following = extract_people_from_html(REQUEST_FILE)
people_to_mute = [person for person in following if person not in settings["excluded_ids"]]
profile_links = [f'https://www.instagram.com/{person}/' for person in people_to_mute if person not in muted_ids]

class InstagramMuteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Mute App")

        # GUI elements setup
        self.details_frame = tk.Frame(root)
        self.details_frame.pack(pady=10, padx=10)

        # Display count and settings
        self.following_count_label = tk.Label(self.details_frame, text=f"Number of People You Follow: {len(following)}")
        self.following_count_label.grid(row=0, column=0, sticky="w")
        self.excluded_count_label = tk.Label(self.details_frame, text=f"Excluded IDs: {len(settings['excluded_ids'])}")
        self.excluded_count_label.grid(row=1, column=0, sticky="w")
        estimated_time = len(profile_links) * 6  # Example estimate: 6 seconds per mute action
        self.estimated_time_label = tk.Label(self.details_frame, text=f"Estimated Run Time: {estimated_time} seconds")
        self.estimated_time_label.grid(row=2, column=0, sticky="w")
        self.muted_ids_label = tk.Label(self.details_frame, text=f"Already Muted IDs: {len(muted_ids)}")
        self.muted_ids_label.grid(row=3, column=0, sticky="w")

        # Settings controls
        self.save_button = tk.Button(self.details_frame, text="Save Settings", command=self.save_settings)
        self.save_button.grid(row=4, column=0, sticky="w", pady=10)
        
        self.add_excluded_label = tk.Label(self.details_frame, text="Add ID to Exclude List:")
        self.add_excluded_label.grid(row=5, column=0, sticky="w")
        self.add_excluded_entry = tk.Entry(self.details_frame)
        self.add_excluded_entry.grid(row=5, column=1)
        self.add_exclude_button = tk.Button(self.details_frame, text="Add", command=self.add_excluded_id)
        self.add_exclude_button.grid(row=5, column=2, padx=5)
        
        self.mute_list_label = tk.Label(self.details_frame, text="IDs to Mute:")
        self.mute_list_label.grid(row=6, column=0, sticky="w")
        self.mute_list_text = scrolledtext.ScrolledText(self.details_frame, width=40, height=10)
        self.mute_list_text.grid(row=7, column=0, columnspan=3, pady=5)
        self.display_mute_list()
        
        self.batch_size_label = tk.Label(self.details_frame, text="Set Batch Size:")
        self.batch_size_label.grid(row=8, column=0, sticky="w")
        self.batch_size_entry = tk.Entry(self.details_frame)
        self.batch_size_entry.insert(tk.END, str(settings['batch_size']))
        self.batch_size_entry.grid(row=8, column=1)
        self.set_batch_size_button = tk.Button(self.details_frame, text="Set Batch Size", command=self.set_batch_size)
        self.set_batch_size_button.grid(row=8, column=2, padx=5)

        # Action buttons
        self.mute_button = tk.Button(root, text="Start Muting", command=self.start_muting)
        self.mute_button.pack(pady=10)

        # Track batch processing
        self.batch_index = 0
        self.max_batch_index = len(profile_links) // settings["batch_size"]

    def display_mute_list(self):
        self.mute_list_text.delete(1.0, tk.END)
        for link in profile_links:
            self.mute_list_text.insert(tk.END, f"{link.split('/')[-2]}\n")

    def add_excluded_id(self):
        new_id = self.add_excluded_entry.get().strip()
        if new_id and new_id not in settings["excluded_ids"]:
            settings["excluded_ids"].append(new_id)
            self.excluded_count_label.config(text=f"Excluded IDs: {len(settings['excluded_ids'])}")
            self.add_excluded_entry.delete(0, tk.END)
            messagebox.showinfo("ID Excluded", f"{new_id} added to excluded list.")
            self.display_mute_list()
            save_settings(settings)

    def save_settings(self):
        save_settings(settings)
        messagebox.showinfo("Settings Saved", "Your settings have been saved.")

    def set_batch_size(self):
        try:
            new_batch_size = int(self.batch_size_entry.get())
            if new_batch_size > 0:
                settings["batch_size"] = new_batch_size
                self.max_batch_index = len(profile_links) // new_batch_size
                messagebox.showinfo("Batch Size Updated", f"Batch size set to {new_batch_size}.")
                self.display_mute_list()
                save_settings(settings)
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid batch size (greater than 0).")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for batch size.")

    def start_muting(self):
        # Process IDs in batches
        self.batch_index = 0
        self.process_next_batch()

    def process_next_batch(self):
        start_index = self.batch_index * settings["batch_size"]
        end_index = (self.batch_index + 1) * settings["batch_size"]
        batch_links = profile_links[start_index:end_index]

        if batch_links:
            for url in batch_links:
                self.mute_next_profile(url)
                time.sleep(4)
                self.mute_posts_and_stories(url)

            logging.info(f"Processed batch {self.batch_index + 1}: {', '.join(batch_links)}")
            self.batch_index += 1
            if self.batch_index <= self.max_batch_index:
                self.ask_for_approval_to_continue()

    def ask_for_approval_to_continue(self):
        result = messagebox.askyesno("Continue", "Do you want to process the next batch?")
        if result:
            self.process_next_batch()
        else:
            messagebox.showinfo("Paused", "Batch processing paused. You can continue later.")

    def mute_next_profile(self, url):
        webbrowser.open(url)
        time.sleep(4)
        self.root.update()

    def mute_posts_and_stories(self, url):
        username = url.split('/')[-2]
        try:
            pyautogui.hotkey('ctrl', 'f')
            pyautogui.typewrite('follow')
            pyautogui.press('esc')
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(2)
            
            pyautogui.hotkey('ctrl', 'f')
            pyautogui.typewrite('following')
            pyautogui.press('enter')
            pyautogui.press('esc')
            pyautogui.press('enter')
            time.sleep(3)

            pyautogui.hotkey('ctrl', 'f')
            pyautogui.typewrite('mute')
            pyautogui.press('enter')
            pyautogui.press('esc')
            pyautogui.press('enter')
            time.sleep(2)

            screenshot = pyautogui.screenshot()
            x1, y1 = 1141, 531
            x2, y2 = 1141, 592
            color1 = screenshot.getpixel((x1, y1))
            color2 = screenshot.getpixel((x2, y2))

            muted_posts, muted_stories = False, False

            if color1 == (38, 38, 38):
                pyautogui.hotkey('ctrl', 'f')
                pyautogui.typewrite('posts')
                pyautogui.press('esc')
                pyautogui.press('enter')
                muted_posts = True

            if color2 == (38, 38, 38):
                pyautogui.hotkey('ctrl', 'f')
                pyautogui.typewrite('stories')
                pyautogui.press('esc')
                pyautogui.press('enter')
                muted_stories = True

            pyautogui.hotkey('ctrl', 'f')
            pyautogui.typewrite('save')
            pyautogui.press('esc')
            pyautogui.press('enter')
            time.sleep(2)

            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('enter')
            time.sleep(2)
            print("Muted user")

            logging.info(f"Muted {username}: {'posts' if muted_posts else ''} {'stories' if muted_stories else ''}")
        except Exception as e:
            logging.error(f"Error muting {username}: {e}")

# Initialize and start the application
root = tk.Tk()
app = InstagramMuteApp(root)
root.mainloop() 