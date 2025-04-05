from PySide6.QtCore import QObject, QThread, Signal
import requests
import time
import json

class APIService(QObject):
    data_generated = Signal(dict)
    
    def __init__(self, api_url, update_rate=0.1, retry_delay=1.0, parent=None):
        super().__init__(parent)
        self.api_url = api_url
        self.update_rate = update_rate
        self.retry_delay = retry_delay
        self.running = False
        self.session = requests.Session()
    
    def start(self):
        """Start the API service in a separate thread."""
        self.running = True
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.start()
    
    def run(self):
        """Main loop that fetches data from the API."""
        while self.running:
            try:
                # Fetch data from the API
                response = self.session.get(self.api_url)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                # Parse the JSON response
                data = response.json()
                
                # Emit the data through the signal
                self.data_generated.emit(data)
                
                # Wait for the configured update rate before next request
                time.sleep(self.update_rate)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data from API: {e}")
                time.sleep(self.retry_delay)  # Wait for the configured retry delay before retrying
    
    def stop(self):
        """Stop the API service."""
        self.running = False
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        self.session.close() 