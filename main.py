"""importing ui file for user interface"""
from ui import Ui
from text import texts
import random

text = random.choice(texts).replace("\n", "").strip()

ui = Ui(text=text)
