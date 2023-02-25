from dbconnector import Connector
import customtkinter as ctk


class Interface:
    def __init__(self):
        self.__screenWidth = 300
        self.__screenHeight = 350
        self.__window = ctk.CTk()
        self.__window.resizable(False, False)
        self.__window.title("Login")
        self.__window.geometry(f'{self.__screenWidth}x{self.__screenHeight}')

        self.__titleLabel = ctk.CTkLabel(self.__window, text='Simple Login Form', text_color='lightblue', font=('@NSimSun', 28, 'bold'))

        self.__usernameFrame = ctk.CTkFrame(self.__window)
        self.__usernameLabel = ctk.CTkLabel(self.__usernameFrame, text='Username', text_color='lightblue', font=('@NSimSun', 20))
        self.__usernameEntry = ctk.CTkEntry(self.__usernameFrame, state=ctk.DISABLED)

        self.__passwordFrame = ctk.CTkFrame(self.__window)
        self.__passwordLabel = ctk.CTkLabel(self.__passwordFrame, text='Password', text_color='lightblue', font=('@NSimSun', 20))
        self.__passwordEntry = ctk.CTkEntry(self.__passwordFrame, state=ctk.DISABLED, show='*')

        self.__loginButton = ctk.CTkButton(self.__window, text='Login', text_color='lightblue', font=('@NSimSun', 20, 'bold'),
                                           command=self.__login)

        self.__connectionLabel = ctk.CTkLabel(self.__window, text='Connecting...', text_color='orange', font=('@NSimSun', 16))

        self.__titleLabel.pack(pady=50)

        self.__usernameLabel.pack(side=ctk.LEFT)
        self.__usernameEntry.pack(side=ctk.LEFT, padx=10)
        self.__usernameFrame.pack(pady=0)

        self.__passwordLabel.pack(side=ctk.LEFT)
        self.__passwordEntry.pack(side=ctk.LEFT, padx=10)
        self.__passwordFrame.pack(pady=20)

        self.__loginButton.pack(pady=25)

        self.__connectionLabel.pack(side=ctk.BOTTOM, anchor="e", padx=8, pady=8)


        # Initial verification of the Database's reachability
        self.__verifier = Connector(verifier=True)
        self.__reachable = self.__verifier.isDatabaseReachable
        if self.__reachable:
            self.__usernameEntry.configure(state=ctk.NORMAL)
            self.__passwordEntry.configure(state=ctk.NORMAL)
            self.__connectionLabel.configure(text='Connected', text_color='green')

        self.__window.mainloop()

    def __login(self):
        if not (self.__usernameEntry.get() == '' or self.__passwordEntry.get() == ''):
            self.__connector = Connector(self.__usernameEntry.get(), self.__passwordEntry.get())
            if self.__connector.connect() is True:
                self.__titleLabel.configure(text_color='green')
            else:
                self.__titleLabel.configure(text_color='red')
