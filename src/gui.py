import customtkinter as ct
from Predictor_db.NBA_Predictor.db_management import get_predictions, get_results

ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")

gameID = 300


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.title("NBA Predictor")
        self.minsize(300, 200)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.label = ct.CTkLabel(master=self, text=self.getLabel())
        self.label.grid(row=0, column=0, columnspan=2,
                        padx=20, pady=(20, 0), sticky="nsew")

        self.nextButton = ct.CTkButton(
            master=self, command=lambda: self.next_button(), text='next game')
        self.nextButton.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        self.prevButton = ct.CTkButton(
            master=self, command=lambda: self.prev_button(), text='prev game')
        self.prevButton.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

    def next_button(self):
        global gameID
        gameID += 1
        self.label.configure(text=self.getLabel())

    def prev_button(self):
        global gameID
        gameID -= 1
        self.label.configure(text=self.getLabel())

    def getLabel(self):
        values = get_predictions('games', gameID)[0]
        text = f'{values[2]} @ {values[1]} \n  \
            {values[3]} - {values[4]} \n'

        return text


app = App()
app.mainloop()
