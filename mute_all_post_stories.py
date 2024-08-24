
import tkinter as tk
import webbrowser
import pyautogui
import time
from bs4 import BeautifulSoup

# Function to parse the HTML file and extract the list of people
def extract_people_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        people = [a.text for a in soup.find_all('a')]
        return people

# Paths to your downloaded Instagram data files
request_file = 'following.html'


# Extract the lists of people you follow and who follow you
following = extract_people_from_html(request_file)
muted = extract_people_from_html(request_file)

# except my id's
me = ["arush_bhimwal","amextaken","arush.onion","majestical_gaming","horizon_personal_computers","arcanebyte.games"]

# Find people you follow who don't follow you back
request = [person for person in following if person not in me and person not in muted]

# Create a list of profile links for people who don't follow you back
request_with_links = [f'https://www.instagram.com/{person}/' for person in request]

# Print not_following_back
print(request)


class LinkOpenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Opener")
        
        # Index to keep track of which link to open next
        self.current_index = 0
        
        # Create and pack a button to open the next link
        self.open_link_button = tk.Button(
            root,
            text="Open Next Link",
            command=self.open_next_link,
            width=20,
            height=2
        )
        self.open_link_button.pack(pady=20)
        
        # Create a label to display the current link being opened
        self.link_label = tk.Label(root, text="", wraplength=300)
        self.link_label.pack(pady=10)
        
    def open_next_link(self):
        # Open the current link if index is within range
        if self.current_index < len(request_with_links):
            url = request_with_links[self.current_index]
            webbrowser.open(url)
            
            # Update the label to show the current link
            self.link_label.config(text=f"Opened: {url}")
            
            # Increment the index for the next link
            self.current_index += 1
        else:
            # If all links have been opened, update the button and label
            self.open_link_button.config(text="No More Links")
            self.link_label.config(text="All links have been opened.")
            self.open_link_button.config(state=tk.DISABLED)

    def unfollow_user(self):
        try:
            # Locate and click the 'Following' button
            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('following')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'Following' button
            time.sleep(1)

            # Locate and click the 'Unfollow' button
            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('mute')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'mute' button

            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('posts')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'posts' button

            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('stories')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'stories' button
            
            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('save')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'save' button
            
            pyautogui.press('tab')            
            pyautogui.press('tab')
            pyautogui.press('enter')
            time.sleep(1)
            print("muted user")
        except Exception as e:
            print(f"Could not unfollow user: {e}")

# Create the main window
root = tk.Tk()
app = LinkOpenerApp(root)

# Unfollow users who don't follow you back
for url in request_with_links:
    app.open_next_link()
    time.sleep(4)  # Wait for the page to load
    app.unfollow_user()

# Start the main loop
root.mainloop()
