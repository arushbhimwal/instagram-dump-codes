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
following_file = 'following.html'
followers_file1 = 'followers_1.html'
followers_file2 = 'followers_2.html'
followers_file3 = 'followers_3.html'
followers_file4 = 'followers_4.html'
followers_file5 = 'followers_5.html'
followers_file6 = 'followers_6.html'




# Extract the lists of people you follow and who follow you
following = extract_people_from_html(following_file)
followers1 = extract_people_from_html(followers_file1)
followers2 = extract_people_from_html(followers_file2)
followers3 = extract_people_from_html(followers_file3)
followers4 = extract_people_from_html(followers_file4)
followers5 = extract_people_from_html(followers_file5)
followers6 = extract_people_from_html(followers_file6)

# Find people you follow who don't follow you back
not_following_back = [person for person in following if person not in followers1 and person not in followers2 and person not in followers3 and person not in followers4 and person not in followers5 and person not in followers6]

# Create a list of profile links for people who don't follow you back
not_following_back_with_links = [f'https://www.instagram.com/{person}/' for person in not_following_back]

# # Print not_following_back
# print(not_following_back)


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
        if self.current_index < len(not_following_back_with_links):
            url = not_following_back_with_links[self.current_index]
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
            pyautogui.typewrite('Following')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'Following' button
            time.sleep(2.5)

            # Locate and click the 'Unfollow' button
            pyautogui.hotkey('ctrl', 'f')  # Open the find dialog
            pyautogui.typewrite('Unfollow')
            pyautogui.press('esc')  # Close the find dialog
            pyautogui.press('enter')  # Click the 'Unfollow' button
            time.sleep(1)
            print("Unfollowed " , not_following_back)
        except Exception as e:
            print(f"Could not unfollow user: {e}")

# Create the main window
root = tk.Tk()
app = LinkOpenerApp(root)

# Unfollow users who don't follow you back
for url in not_following_back_with_links:
    app.open_next_link()
    time.sleep(4)  # Wait for the page to load
    app.unfollow_user()

# Start the main loop
root.mainloop()
