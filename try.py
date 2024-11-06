from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Maximized PyQt5 App")

        # Start the window maximized (not full-screen)
        self.showMaximized()

        # Create a vertical layout to organize the widgets
        layout = QVBoxLayout()

        # Create a label that will display the entered text
        self.label = QLabel("Enter your name below and click Submit.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("titleLabel")  # Assign an object name for CSS targeting
        layout.addWidget(self.label)

        # Create a text input field where the user can type their name
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your name")
        self.input_field.setObjectName("inputField")  # Assign an object name for CSS targeting
        layout.addWidget(self.input_field)

        # Create a button to submit the text from the input field
        self.submit_button = QPushButton("Submit")
        self.submit_button.setObjectName("submitButton")  # Assign an object name for CSS targeting
        self.submit_button.clicked.connect(self.update_label)  # Connect the button to the update method
        layout.addWidget(self.submit_button)

        # Create a button to toggle maximized window on and off
        self.toggle_button = QPushButton("Toggle Maximized")
        self.toggle_button.setObjectName("toggleButton")  # Assign an object name for CSS targeting
        self.toggle_button.clicked.connect(self.toggle_maximized)  # Connect to the toggle method
        layout.addWidget(self.toggle_button)

        # Set the layout to the window
        self.setLayout(layout)

        # Apply the CSS styles to the widgets
        self.apply_styles()

    def apply_styles(self):
        """
        This method applies CSS-like styles to the widgets in the window.
        You can customize colors, font sizes, padding, borders, etc.
        """
        style_sheet = """
            QWidget {
                background-color: #f0f0f0;  /* Light background color for the whole window */
            }

            #titleLabel {
                font-size: 24px;  /* Font size for the label */
                color: #2c3e50;   /* Text color for the label */
                padding: 10px;
            }

            #inputField {
                padding: 10px;  /* Padding inside the input field */
                font-size: 18px;  /* Font size for the input text */
                border: 2px solid #3498db;  /* Border color and thickness */
                border-radius: 5px;  /* Rounded corners */
                background-color: #ffffff;  /* Input field background color */
            }

            #submitButton {
                background-color: #3498db;  /* Button background color */
                color: white;  /* Button text color */
                padding: 10px;  /* Padding inside the button */
                font-size: 18px;  /* Font size for the button text */
                border-radius: 5px;  /* Rounded corners for the button */
            }

            #submitButton:hover {
                background-color: #2980b9;  /* Button background color when hovered */
            }

            #toggleButton {
                background-color: #2ecc71;  /* Green background color for the toggle button */
                color: white;  /* Button text color */
                padding: 10px;  /* Padding inside the button */
                font-size: 18px;  /* Font size for the button text */
                border-radius: 5px;  /* Rounded corners for the button */
            }

            #toggleButton:hover {
                background-color: #27ae60;  /* Button background color when hovered */
            }
        """
        # Apply the style sheet to the window and all its child widgets
        self.setStyleSheet(style_sheet)

    def update_label(self):
        """
        This method gets the text from the input field and updates the label.
        """
        name = self.input_field.text()  # Get the text from the input field
        if name:  # If there's text, update the label
            self.label.setText(f"Hello, {name}!")
        else:  # If the input field is empty, show a default message
            self.label.setText("Please enter your name.")

    def toggle_maximized(self):
        """
        This method toggles the window maximized state on and off.
        """
        if self.isMaximized():
            self.showNormal()  # If the window is maximized, switch to normal window size
        else:
            self.showMaximized()  # If not maximized, switch to maximized window

# Main code to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the MainWindow class
    window = MainWindow()

    # Show the window (starts in maximized mode)
    window.show()

    # Execute the application's main loop
    sys.exit(app.exec_())
