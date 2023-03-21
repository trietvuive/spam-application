from tkinter import ttk
from script import RegistrationAutomation

import asyncio
import tkinter as tk

class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show();


class Window(tk.Tk):
    def __init__(self, loop):
        self.automator = RegistrationAutomation()
        self.loop = loop
        self.root = tk.Tk()
        self.root.title = "Thùy Chi App :>"
        self.animation = "░▒▒▒▒"
        self.label = tk.Label(text="")
        self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))
        self.progressbar = ttk.Progressbar(length= 2 * len(self.automator))
        self.progressbar.grid(row=1, columnspan=2, padx=(8, 8), pady=(16, 0))
        button_non_block = tk.Button(text="Run!", width=10, command=lambda: self.loop.create_task(self.calculate_async()))
        button_non_block.grid(row=2, column=1, sticky=tk.W, padx=8, pady=8)

    async def show(self):
        while True:
            self.animation = self.animation[1:] + self.animation[0]
            self.label["text"] = self.animation
            self.root.update()
            await asyncio.sleep(.2)

    async def calculate_async(self):
        n = len(self.automator)
        for i in range(1, n+1):
            self.automator.process_next_student()
            self.progressbar["value"] = i / n * 100
            await asyncio.sleep(2)

asyncio.run(App().exec())
