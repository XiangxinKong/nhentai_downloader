import tkinter as tk
import tkinter.messagebox
from downloader import downloader


class main(tk.Tk):
    def __init__(self):
        # initialize the widow
        super().__init__()
        super().title('NH Downloader')
        super().geometry('400x250')
        self.configure(background='black')
        self.consolo = None

        # initialize the canvas with image
        global image_file
        canvas = tk.Canvas(self, width=400, height=65, bg='black')
        canvas.pack(side="top")
        image_file = tk.PhotoImage(file='logo.gif')
        canvas.create_image(50, 0, anchor='n', image=image_file)
        canvas.create_text(255, 18, fill="white", font="Times 13 italic bold",
                           text="Abandon all hope, ye who enter here")

        # initialize the labels
        tk.Label(self, text='Url:', foreground="white", font=('Arial', 16,), bg="black").place(x=10, y=95)
        tk.Label(self, text='To:', foreground="white", font=('Arial', 16,), bg="black").place(x=10, y=135)

        # initialize the labels
        self.var_address = tk.StringVar()
        self.var_url = tk.StringVar()
        self.var_address.set('manga/')
        self.var_url.set('https://nhentai.net/g/xxxxxx/')
        tk.Entry(self, textvariable=self.var_address, font=('Arial', 14), width=28).place(x=60, y=140)  # address field
        tk.Entry(self, textvariable=self.var_url, font=('Arial', 14), width=28).place(x=60, y=100)  # url field

        # initialize the button
        tk.Button(self, text='Download', font=('Arial', 12), command=self.download).place(x=290, y=185)

    # begin to download
    def download(self):
        try:
            self.consolo.destroy()
        except:
            pass
        # initialize the download state window
        self.consolo = tk.Tk()
        self.consolo.title('NH Downloader')
        self.consolo.geometry('300x140')
        m_text = tkinter.Text(self.consolo, width=40, height=9)
        m_text.pack()
        # initialize the downloader
        downloader = downloader.__init__(self.var_address.get(), self.var_url.get(), m_text)
        downloader.start()
        self.var_url.set("")
        # display
        self.consolo.mainloop()

if __name__ == "__main__":
    k = main()
    k.mainloop()
