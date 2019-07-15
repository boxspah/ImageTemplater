import tkinter as tk
import tkinter.messagebox
import warnings

class PlatformSelect:
    def __init__(self, pList):
        self.window = tk.Tk()
        self.window.title('Select destination platform(s)')

        # create dictionary to store checkbox values
        self.selectedPlatforms = {}
        for p in pList:
            self.selectedPlatforms[p] = 0

        # create and pack a checkbox for every platform
        for p in self.selectedPlatforms:
            self.selectedPlatforms[p] = tk.IntVar(value=0)
            l = tk.Checkbutton(self.window, text=p, variable=self.selectedPlatforms[p], onvalue=1, offvalue=0)
            l.pack()

        # button to proceed
        self.c = tk.Button(self.window, text='Continue', command=self.confirm)
        self.c.pack()

        self.window.mainloop()

    def confirm(self):
        sel_array = [y.get() for x, y in self.selectedPlatforms.items()]
        # close window and continue only if at least 1 platform is selected
        if sum(sel_array) < 1:
            warnings.warn('No platforms selected. Not closing window.')
            tkinter.messagebox.showwarning('Select a platform', 'Please select at least one platform from the list.')
        elif sum(sel_array) >= 1:
            self.window.destroy()