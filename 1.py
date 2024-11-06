from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Multi-Page PyQt5 App")
        self.showMaximized()

        # Create a QStackedWidget to hold multiple pages
        self.stacked_widget = QStackedWidget()

        # Create the main page and secondary page
        self.main_page = self.create_main_page()
        self.secondary_page = self.create_secondary_page()

        # Add the pages to the QStackedWidget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.secondary_page)

        # Set the first page as the default page
        self.stacked_widget.setCurrentWidget(self.main_page)

        # Create the main layout and add the QStackedWidget to it
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Apply CSS-like styles to the entire app
        self.apply_styles()

    def apply_styles(self):
        """
        Apply CSS-like styles to widgets in the main and secondary pages.
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

    def create_main_page(self):
        """
        Create the main page with a label and a button to navigate to the secondary page.
        """
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Welcome to the Main Page!")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("mainLabel")
        layout.addWidget(label)

        switch_button = QPushButton("Go to Secondary Page")
        switch_button.setObjectName("switchButton")
        switch_button.clicked.connect(self.go_to_secondary_page)  # Switch to secondary page
        layout.addWidget(switch_button)

        page.setLayout(layout)
        return page

    def create_secondary_page(self):
        """
        Create the secondary page with a label and a button to navigate back to the main page.
        """
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Welcome to the Secondary Page!")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("secondaryLabel")
        layout.addWidget(label)

        back_button = QPushButton("Back to Main Page")
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.go_to_main_page)  # Switch back to main page
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def go_to_secondary_page(self):
        """
        Switch to the secondary page.
        """
        self.stacked_widget.setCurrentWidget(self.secondary_page)

    def go_to_main_page(self):
        """
        Switch back to the main page.
        """
        self.stacked_widget.setCurrentWidget(self.main_page)

# Main code to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the MainWindow class
    window = MainWindow()

    # Show the main window
    window.show()

    # Execute the application's main loop
    sys.exit(app.exec_())
