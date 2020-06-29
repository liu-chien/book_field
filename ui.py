import tkinter as tk
import threading
import os
import datetime
from time import sleep
from book_field import Agent
from wait_until import wait_until
import PyQt5

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Book Badminton Field")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        frame1 = tk.Frame(self)
        frame1.pack(fill=tk.X)
        lbl1 = tk.Label(frame1, text="Account", width=6)
        lbl1.pack(side=tk.LEFT, padx=5, pady=5)
        self.account = tk.Entry(frame1)
        self.account.pack(fill=tk.X, padx=5, expand=True)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.X)
        lbl2 = tk.Label(frame2, text="Password", width=6)
        lbl2.pack(side=tk.LEFT, padx=5, pady=5)
        self.passwd = tk.Entry(frame2)
        self.passwd.pack(fill=tk.X, padx=5, expand=True)

        frame3 = tk.Frame(self)
        frame3.pack(fill=tk.X)
        lbl3 = tk.Label(frame3, text="Date", width=6)
        lbl3.pack(side=tk.LEFT, padx=5, pady=5)
        self.date = tk.Entry(frame3)
        self.date.pack(fill=tk.X, padx=5, expand=True)

        frame4 = tk.Frame(self)
        frame4.pack(fill=tk.X)
        lbl4 = tk.Label(frame4, text="Time", width=6)
        lbl4.pack(side=tk.LEFT, padx=5, pady=5)
        self.time = tk.Entry(frame4)
        self.time.pack(fill=tk.X, padx=5, expand=True)

        frame5 = tk.Frame(self)
        frame5.pack(fill=tk.X)
        lbl5 = tk.Label(frame5, text="No. Field", width=6)
        lbl5.pack(side=tk.LEFT, padx=5, pady=5)
        self.field = tk.Entry(frame5)
        self.field.pack(fill=tk.X, padx=5, expand=True)

        self._restore_info()

        self.summit = tk.Button(self)
        self.summit["text"] = "Send Request\n(Check your info ageain)"
        self.summit["command"] = self.send_booking_request
        self.summit.pack(pady=20)

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.master.destroy)
        # self.quit.pack()
    def send_booking_request(self):
        if hasattr(self, "t"):
            print("只能Summit一次，請關掉重開")
            return 0
        self._save_info()
        self.t = threading.Thread(target = self._book_field)
        self.t.start()

        

    def _save_info(self):
        dirname = "book_info"
        filename = os.path.join(dirname, "book_info.txt")
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        if os.path.isfile(filename):
            os.remove(filename)
        account = self.account.get()
        passwd = self.passwd.get()
        date = self.date.get()
        time = self.time.get()
        field = self.field.get()

        with open(filename, "w") as f:
            f.write(account + "\n")
            f.write(passwd + "\n")
            f.write(date + "\n")
            f.write(time + "\n")
            f.write(field)

        print("Save info")
              
    def _restore_info(self):
        dirname = "book_info"
        filename = os.path.join(dirname, "book_info.txt")

        if not os.path.isfile(filename):
            print("Cannot load previous booking info")
            return 1
        
        with open(filename, "r") as f:
            account = f.readline().replace("\n", "")
            passwd = f.readline().replace("\n", "")
            date = f.readline().replace("\n", "")
            time = f.readline().replace("\n", "")
            field = f.readline().replace("\n", "")
        self.account.insert(0, account)
        self.passwd.insert(0, passwd)
        self.date.insert(0, date)
        self.time.insert(0, time)
        self.field.insert(0, field)

    def _book_field(self):
        account = self.account.get()
        passwd = self.passwd.get()
        dates = self.date.get().split(" ")
        times = self.time.get().split(" ")
        order = self.field.get().split(" ")

        if account == "" or passwd == "" or dates == [""] or times == [""] or order == [""]:
            print("Fill in booking info before summitting.")
            return 1

        for date in dates:
            for time in times:
                # Booking information
                time = int(time)
                time_slot = int(time - 6)  # 07:00 refers to time slot 1
                
                # year, month, date, hour, minute, second, microsecond
                start_time = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]), time, 0, 0, 0) - datetime.timedelta(days=3)
                end_time = start_time + datetime.timedelta(seconds=0.7)

                # Log in account
                wait_until(start_time - datetime.timedelta(minutes=1))
                agent = Agent(time_slot, date, account, passwd)

                # field order
                field_order = [int(item) for item in order]
                available_field = agent.search_available_field()
                field_order = [item for item in field_order if item in available_field]

                # Book
                wait_until(start_time - datetime.timedelta(seconds=0.1))
                counter = 0     # Number of booked field
                stop = False
                while True:
                    for field in field_order:
                        if agent.book_field(field):
                            counter += 1
                            if counter >= 2:
                                stop = True
                                break
                    if stop or datetime.datetime.now() > end_time:
                        break
                print("搶完場了，記得上網查結果 (:３っ)∋")
        

root = tk.Tk()
root.geometry("600x300+300+300")
app = Application(master=root)

app.mainloop()