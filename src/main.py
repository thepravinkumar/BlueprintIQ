import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app  # Import Flask app from app.py

from src.gui import BlueprintIQApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueprintIQApp(root)
    root.mainloop()
