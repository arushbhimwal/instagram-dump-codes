import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and maximize the window by default
        self.setWindowTitle("Instagram Business Dashboard")
        self.showMaximized()

        # Create the QStackedWidget to hold multiple pages
        self.stacked_widget = QStackedWidget()

        # Page 1: Access Token Entry
        self.access_token_page = self.create_access_token_page()

        # Page 2: Instagram Business IDs Entry
        self.instagram_ids_page = self.create_instagram_ids_page()

        # Add the pages to the QStackedWidget
        self.stacked_widget.addWidget(self.access_token_page)
        self.stacked_widget.addWidget(self.instagram_ids_page)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Load saved data if available
        self.load_saved_data()

    def create_access_token_page(self):
        """Create the first page to ask for the Facebook Access Token."""
        page = QWidget()
        layout = QVBoxLayout()

        # Access Token Label and Input
        label = QLabel("Enter Facebook Access Token")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.access_token_input = QLineEdit()
        self.access_token_input.setPlaceholderText("Enter your Access Token here")
        layout.addWidget(self.access_token_input)

        # Continue Button
        continue_button = QPushButton("Continue")
        continue_button.clicked.connect(self.go_to_instagram_ids_page)
        layout.addWidget(continue_button)

        page.setLayout(layout)
        return page

    def create_instagram_ids_page(self):
        """Create the second page to ask for multiple Instagram Business IDs."""
        page = QWidget()
        layout = QVBoxLayout()

        # Instagram IDs Label and Input
        label = QLabel("Enter Instagram Business IDs (comma-separated)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.instagram_ids_input = QLineEdit()
        self.instagram_ids_input.setPlaceholderText("Enter Instagram Business IDs (e.g., 1234567890,0987654321)")
        layout.addWidget(self.instagram_ids_input)

        # Continue Button
        continue_button = QPushButton("Generate Dashboards")
        continue_button.clicked.connect(self.generate_dashboards)
        layout.addWidget(continue_button)

        page.setLayout(layout)
        return page

    def create_instagram_dashboard(self, business_id):
        """Create the dashboard for each Instagram Business ID by making an API call."""
        page = QWidget()
        layout = QVBoxLayout()

        # Fetch data from Instagram Graph API
        try:
            # Sample endpoint to get account insights
            url = f"https://graph.facebook.com/v17.0/{business_id}/insights?metric=impressions,reach,profile_views&access_token={self.access_token_input.text()}"
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                label = QLabel(f"Error fetching data for Business ID {business_id}: {data['error']['message']}")
            else:
                # Display fetched data
                insights = data.get("data", [])
                insights_text = "\n".join([f"{metric['name']}: {metric['values'][0]['value']}" for metric in insights])
                label = QLabel(f"Dashboard for Business ID: {business_id}\n\n{insights_text}")

        except Exception as e:
            label = QLabel(f"Error fetching data: {e}")

        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        prev_button = QPushButton("← Previous ID")
        prev_button.clicked.connect(self.go_to_previous_id)
        nav_layout.addWidget(prev_button)
        
        next_button = QPushButton("Next ID →")
        next_button.clicked.connect(self.go_to_next_id)
        nav_layout.addWidget(next_button)

        layout.addLayout(nav_layout)
        page.setLayout(layout)
        return page

    def generate_dashboards(self):
        """Generate a dashboard page for each Instagram Business ID."""
        # Get the input from Instagram IDs field
        instagram_ids = self.instagram_ids_input.text().split(',')

        # Remove any existing dashboard pages from the stack
        while self.stacked_widget.count() > 2:
            self.stacked_widget.removeWidget(self.stacked_widget.widget(2))

        # Create a dashboard for each Instagram ID
        for business_id in instagram_ids:
            business_id = business_id.strip()
            if business_id:
                dashboard = self.create_instagram_dashboard(business_id)
                self.stacked_widget.addWidget(dashboard)

        # Save the access token and IDs
        self.save_data(self.access_token_input.text(), instagram_ids)

        # Go to the first dashboard
        self.stacked_widget.setCurrentIndex(2)

    def go_to_instagram_ids_page(self):
        """Switch to the Instagram IDs input page."""
        self.stacked_widget.setCurrentWidget(self.instagram_ids_page)

    def go_to_previous_id(self):
        """Navigate to the previous Instagram dashboard."""
        current_index = self.stacked_widget.currentIndex()
        if current_index > 2:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    def go_to_next_id(self):
        """Navigate to the next Instagram dashboard."""
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)

    def save_data(self, access_token, instagram_ids):
        """Save the access token and Instagram IDs to a JSON file."""
        data = {
            "access_token": access_token,
            "instagram_ids": instagram_ids
        }
        with open('saved_data.json', 'w') as f:
            json.dump(data, f)

    def load_saved_data(self):
        """Load the saved access token and Instagram IDs from a JSON file."""
        try:
            with open('saved_data.json', 'r') as f:
                data = json.load(f)
                self.access_token_input.setText(data.get("access_token", ""))
                self.instagram_ids_input.setText(','.join(data.get("instagram_ids", [])))
        except FileNotFoundError:
            pass

# Main code to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
