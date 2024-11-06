from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Main Window")

        # Start the window maximized
        self.showMaximized()

        # Create a vertical layout for the main window
        layout = QVBoxLayout()

        # Create a label for the main window
        self.label = QLabel("Welcome to the Main Window!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("mainLabel")
        layout.addWidget(self.label)

        # Create a button that opens the secondary window
        self.switch_button = QPushButton("Go to Secondary Window")
        self.switch_button.setObjectName("switchButton")
        self.switch_button.clicked.connect(self.open_secondary_window)  # Connect to switch window
        layout.addWidget(self.switch_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Create an instance of the secondary window
        self.secondary_window = SecondaryWindow()

        # Apply styles (CSS-like styling) to both windows
        self.apply_styles()

    def apply_styles(self):
        """
        Apply CSS-like styles to widgets in the main and secondary windows.
        """
        style_sheet = """
            QWidget {
                background-color: #f0f0f0;  /* Light background color */
            }

            #mainLabel, #secondaryLabel {
                font-size: 24px;
                color: #2c3e50;
                padding: 10px;
            }

            #switchButton, #backButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 18px;
                border-radius: 5px;
            }

            #switchButton:hover, #backButton:hover {
                background-color: #2980b9;
            }
        """
        self.setStyleSheet(style_sheet)
        self.secondary_window.setStyleSheet(style_sheet)

    def open_secondary_window(self):
        """
        This method hides the main window and shows the secondary window.
        """
        self.hide()  # Hide the main window
        self.secondary_window.show()  # Show the secondary window


class SecondaryWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Secondary Window")

        # Start the window maximized
        self.showMaximized()

        # Create a vertical layout for the secondary window
        layout = QVBoxLayout()

        # Create a label for the secondary window
        self.label = QLabel("Welcome to the Secondary Window!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("secondaryLabel")
        layout.addWidget(self.label)

        # Create a button to go back to the main window
        self.back_button = QPushButton("Back to Main Window")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.go_back_to_main)  # Connect to the go-back method
        layout.addWidget(self.back_button)

        # Set the layout for the secondary window
        self.setLayout(layout)

    def go_back_to_main(self):
        """
        This method hides the secondary window and shows the main window.
        """
        self.hide()  # Hide the secondary window
        main_window.show()  # Show the main window


# Main code to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the MainWindow class
    main_window = MainWindow()

    # Show the main window
    main_window.show()

    # Execute the application's main loop
    sys.exit(app.exec_())
