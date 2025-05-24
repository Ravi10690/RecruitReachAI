"""Development server with auto-reload for the Gradio application."""

import time
import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppReloader(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_app()

    def start_app(self):
        """Start the Gradio app process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("\nStarting app...")
        self.process = subprocess.Popen([sys.executable, "app.py"])

    def on_modified(self, event):
        """Handle file modification events."""
        if event.src_path.endswith('.py'):
            print(f"\nDetected change in {event.src_path}")
            self.start_app()

def main():
    """Run the development server with auto-reload."""
    reloader = AppReloader()
    observer = Observer()
    observer.schedule(reloader, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if reloader.process:
            reloader.process.terminate()
    observer.join()

if __name__ == "__main__":
    main()
