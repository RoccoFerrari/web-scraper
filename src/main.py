# run: ../venv/bin/python main.py
import scraper_logic as sl
from gui import *

if __name__ == "__main__":
    # Standard boilerplate to run the Tkinter application
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()
