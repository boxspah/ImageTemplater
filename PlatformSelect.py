import tkinter as tk
import tkinter.messagebox
import warnings

class PlatformSelect:
    def __init__(self, pList, file_path):
        self.window = tk.Tk()
        self.window.title('Select destination platform(s)')
        # remove maximize and minimize window buttons
        self.window.attributes('-toolwindow', 1)
        # force window to stay on top
        self.window.attributes('-topmost', 1)
        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        current_file = tk.LabelFrame(text='Currently editing:', bd=3, relief=tk.GROOVE, padx=10, pady=5)
        file_name = tk.Entry(current_file, width=40)
        file_name.insert(0, file_path)
        file_name.config(state='readonly')
        file_name.pack()
        current_file.pack(padx=10)

        # create dictionary to store checkbox values
        self.selectedPlatforms = {}

        # create a checkbox for every platform
        for p in pList:
            self.selectedPlatforms[p] = tk.IntVar(value=0)
            l = tk.Checkbutton(self.window, text=p, variable=self.selectedPlatforms[p], onvalue=1, offvalue=0, height=2, padx=40)
            l.pack(fill=tk.BOTH, expand=True)

        # keyboard bindings for platforms
        for n in range(len(pList)):
            self.window.bind_all(str(n+1), self.toggle_platform)

        # button to proceed
        c = tk.Button(self.window, text='Continue', underline=0, command=self.confirm, padx=5, pady=5)
        self.window.bind_all('c', self.confirm)
        self.window.bind_all('<Return>', self.confirm)
        c.pack(fill=tk.BOTH, expand=True)

        # set minimum window size
        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())
        self.window.mainloop()

    def close(self):
        if tkinter.messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.window.destroy()
            raise SystemExit('User requested termination')

    def toggle_platform(self, key_event):
        affected_key = list(self.selectedPlatforms.keys())[int(key_event.keysym)-1]
        old_value = self.selectedPlatforms[affected_key].get()
        self.selectedPlatforms[affected_key].set(1 if old_value is 0 else 0)

    def confirm(self, key_event=None):
        sel_array = [y.get() for x, y in self.selectedPlatforms.items()]
        # close window and continue only if at least 1 platform is selected
        if sum(sel_array) < 1:
            tkinter.messagebox.showwarning('Select a platform', 'Please select at least one platform from the list.')
        elif sum(sel_array) >= 1:
            self.window.destroy()