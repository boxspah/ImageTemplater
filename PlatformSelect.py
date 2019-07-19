import tkinter as tk
import tkinter.messagebox
import warnings

class PlatformSelect:
    def __init__(self, pList):
        self.window = tk.Tk()
        self.window.title('Select destination platform(s)')
        # remove maximize and minimize window buttons
        self.window.attributes('-toolwindow', 1)
        # force window to stay on top
        self.window.attributes('-topmost', 1)

        # handle window close event
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        # create dictionary to store checkbox values
        self.selectedPlatforms = {}
        for p in pList:
            self.selectedPlatforms[p] = 0

        # create a checkbox for every platform
        for p in self.selectedPlatforms:
            self.selectedPlatforms[p] = tk.IntVar(value=0)
            l = tk.Checkbutton(self.window, text=p, variable=self.selectedPlatforms[p], onvalue=1, offvalue=0, height=2, padx=40)
            l.pack(fill=tk.BOTH, expand=True)

        # button to proceed
        c = tk.Button(self.window, text='Continue', command=self.confirm, padx=5, pady=5)
        c.pack(fill=tk.BOTH, expand=True)

        # set minimum window size
        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())
        self.window.mainloop()

    def close(self):
        if tkinter.messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.window.destroy()
            raise SystemExit('User requested termination')

    def confirm(self):
        sel_array = [y.get() for x, y in self.selectedPlatforms.items()]
        # close window and continue only if at least 1 platform is selected
        if sum(sel_array) < 1:
            tkinter.messagebox.showwarning('Select a platform', 'Please select at least one platform from the list.')
        elif sum(sel_array) >= 1:
            self.window.destroy()