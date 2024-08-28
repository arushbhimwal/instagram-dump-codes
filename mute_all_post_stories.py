import tkinter as tk
import webbrowser
import pyautogui
import time
from bs4 import BeautifulSoup
from PIL import Image

# Function to parse the HTML file and extract the list of people
def extract_people_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        people = [a.text for a in soup.find_all('a')]
        return people

# Paths to your downloaded Instagram data files
request_file = 'following.html'

# Extract the list of people you follow
following = extract_people_from_html(request_file)

# Exclude your own accounts
my_accounts = ["arush_bhimwal","amextaken","arush.onion","majestical_gaming","horizon_personal_computers","arcanebyte.games"]

# Generate a list of profile links for the people you follow
people_to_mute = [person for person in following if person not in my_accounts ]
profile_links = [f'https://www.instagram.com/{person}/' for person in people_to_mute]

# Print not_following_back
print(people_to_mute)


class InstagramMuteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Mute App")
        
        # Index to keep track of the current profile being processed
        self.current_index = 0
        
        # Create and pack a button to mute the next profile
        self.mute_button = tk.Button(
            root,
            text="Mute Next Profile",
            command=self.mute_next_profile,
            width=20,
            height=2
        )
        self.mute_button.pack(pady=20)
        
        # Create a label to display the current profile being muted
        self.profile_label = tk.Label(root, text="", wraplength=300)
        self.profile_label.pack(pady=10)
        
    def mute_next_profile(self):
        # Open the current profile and attempt to mute posts and stories
        if self.current_index < len(profile_links):
            url = profile_links[self.current_index]
            webbrowser.open(url)
            
            # Update the label to show the current profile being processed
            self.profile_label.config(text=f"Opened: {url}")
            
            # Increment the index for the next profile
            self.current_index += 1
        else:
            # If all profiles have been processed, update the button and label
            self.mute_button.config(text="No More Profiles")
            self.profile_label.config(text="All profiles have been muted.")
            self.mute_button.config(state=tk.DISABLED)

    def mute_posts_and_stories(self):
        try:
            # Locate and click the 'Following' button
            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('following')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'Following' button
            time.sleep(1)

            # Locate and click the 'mute' button
            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('mute')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'mute' button

            # Take a screenshot to check the color of the mute options
            screenshot = pyautogui.screenshot()
            x1, y1 = 1165,524
            x2, y2 = 1165,588
            color1 = screenshot.getpixel((x1, y1))
            color2 = screenshot.getpixel((x2, y2))

            print(f"Color at (1165, 524): {color1}")
            print(f"Color at (1165, 588): {color2}")

            # Mute posts if the checkbox is unchecked (color is (38, 38, 38))
            if color1 == (38, 38, 38):
                pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
                pyautogui.typewrite('posts')
                pyautogui.press('esc')  # Close the find dialog
                pyautogui.press('enter')  # Click the 'posts' button
                print("post muted")

            # Mute stories if the checkbox is unchecked (color is (38, 38, 38))
            if color2 == (38, 38, 38):
                pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
                pyautogui.typewrite('stories')
                pyautogui.press('esc')  # Close the find dialog
                pyautogui.press('enter')  # Click the 'stories' button
                print("story muted")
            
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
            print(f"Could not mute posts and stories: {e}")

# Create the main window
root = tk.Tk()
app = InstagramMuteApp(root)

# Mute posts and stories from your followers
for url in profile_links:
    app.mute_next_profile()
    time.sleep(4)  # Wait for the page to load
    app.mute_posts_and_stories()

# Start the main loop
root.mainloop()




