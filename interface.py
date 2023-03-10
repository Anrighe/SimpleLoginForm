from dbconnector import Connector
import customtkinter as ctk


class Interface:
    def __init__(self):
        self.__windowWidth = 330
        self.__windowHeight = 400
        self.__spawnOffset = 30
        self.__window = ctk.CTk()
        self.__screenWidth = self.__window.winfo_screenwidth()
        self.__screenHeight = self.__window.winfo_screenheight()
        self.__x = (self.__screenWidth // 2) - (self.__window.winfo_reqwidth() // 2)
        self.__y = (self.__screenHeight // 2) - (self.__window.winfo_reqheight() // 2)
        self.__window.resizable(False, False)
        self.__window.title("Login")
        self.__window.geometry("+{}+{}".format(self.__x, self.__y))

        self.__titleLabel = ctk.CTkLabel(self.__window, text='Simple Login Form', text_color='lightblue', font=('@NSimSun', 28, 'bold'))

        self.__usernameFrame = ctk.CTkFrame(self.__window, fg_color=self.__window.fg_color)
        self.__usernameLabel = ctk.CTkLabel(self.__usernameFrame, text='Username', text_color='lightblue', font=('@NSimSun', 20))
        self.__usernameEntry = ctk.CTkEntry(self.__usernameFrame, state=ctk.DISABLED)
        self.__usernameEntry.bind('<Return>', lambda e: self.__login())

        self.__passwordFrame = ctk.CTkFrame(self.__window, fg_color=self.__window.fg_color)
        self.__passwordLabel = ctk.CTkLabel(self.__passwordFrame, text='Password', text_color='lightblue', font=('@NSimSun', 20))
        self.__passwordEntry = ctk.CTkEntry(self.__passwordFrame, state=ctk.DISABLED, show='*')
        self.__passwordEntry.bind('<Return>', lambda e: self.__login())

        self.__loginButton = ctk.CTkButton(self.__window, text='Login', text_color='lightblue', font=('@NSimSun', 20, 'bold'),
                                           command=self.__login)

        self.__optionsFrame = ctk.CTkFrame(self.__window, fg_color=self.__window.fg_color)
        self.__registerLabel = ctk.CTkLabel(self.__optionsFrame, text='Register',
                                            text_color='#154c79', font=('@NSimSun', 18, 'underline', 'bold'))
        self.__registerLabel.bind('<Button-1>', self.__register)
        self.__resetPasswordLabel = ctk.CTkLabel(self.__optionsFrame, text='Forgot password?',
                                                 text_color='#154c79', font=('@NSimSun', 18, 'underline', 'bold'))
        self.__resetPasswordLabel.bind('<Button-1>', self.__resetPassword)

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

        self.__registerLabel.pack(side=ctk.LEFT, padx=20)
        self.__resetPasswordLabel.pack(side=ctk.RIGHT, padx=20)
        self.__optionsFrame.pack(side=ctk.BOTTOM, pady=15)

        self.__window.update()

        # Initial verification of the Database's reachability
        self.__verifier = Connector(verifier=True)
        self.__updateReachability()

        self.__window.mainloop()

    def __login(self):
        self.__updateReachability()
        if not (self.__usernameEntry.get() == '' or self.__passwordEntry.get() == ''):
            self.__connector = Connector(self.__usernameEntry.get(), self.__passwordEntry.get())
            if self.__connector.connect() is True:
                self.__titleLabel.configure(text_color='green')
            else:
                self.__titleLabel.configure(text_color='red')

    def __updateReachability(self):
        if self.__verifier.isDatabaseReachable:
            self.__usernameEntry.configure(state=ctk.NORMAL)
            self.__passwordEntry.configure(state=ctk.NORMAL)
            self.__connectionLabel.configure(text='Connected', text_color='green')
        else:
            self.__connectionLabel.configure(text='Not connected', text_color='red')

    def __register(self, event):
        self.__topRegister = ctk.CTkToplevel()  # Creates a Toplevel window
        self.__topRegister.title('Register')
        self.__x = (self.__screenWidth // 2) - (self.__topRegister.winfo_reqwidth() // 2)
        self.__y = (self.__screenHeight // 2) - (self.__topRegister.winfo_reqheight() // 2)
        self.__topRegister.geometry("+{}+{}".format(self.__x + self.__spawnOffset, self.__y + self.__spawnOffset))
        self.__topRegister.geometry(f'{self.__windowWidth}x{self.__windowHeight}')
        self.__topRegister.resizable(False, False)
        self.__topRegister.attributes('-topmost', True)

        self.__registerTitleLabel = ctk.CTkLabel(self.__topRegister, text='Register', text_color='lightblue',
                                                 font=('@NSimSun', 28, 'bold'))

        self.__registrationFeedbackLabel = ctk.CTkLabel(self.__topRegister, text='', text_color='lightblue')

        self.__registerUsernameEntry = ctk.CTkEntry(self.__topRegister, placeholder_text='Username',
                                                    placeholder_text_color='lightblue', width=270)

        self.__registerPasswordEntry = ctk.CTkEntry(self.__topRegister, show='*', placeholder_text_color='lightblue',
                                                    placeholder_text='Password', width=270)

        self.__repeatRegisterPasswordEntry = ctk.CTkEntry(self.__topRegister, show='*', placeholder_text_color='lightblue',
                                                          placeholder_text='Confirm password', width=270)

        self.__termsBox = ctk.CTkCheckBox(self.__topRegister, text='I accept the Terms of Use & Privacy Policy.',
                                          text_color='lightblue')

        self.__registerButton = ctk.CTkButton(self.__topRegister, text='Register', text_color='lightblue',
                                              font=('@NSimSun', 20, 'bold'), command=self.__registerRequest)

        self.__registerTitleLabel.pack(pady=30)
        self.__registrationFeedbackLabel.pack()
        self.__registerUsernameEntry.pack(pady=10)
        self.__registerPasswordEntry.pack(pady=10)
        self.__repeatRegisterPasswordEntry.pack(pady=10)
        self.__termsBox.pack(pady=20)
        self.__registerButton.pack(pady=15)

    def __registerRequest(self):
        self.__termsBox.configure(text_color='lightblue')
        self.__registerUsernameEntry.configure(placeholder_text_color='lightblue')
        self.__registerPasswordEntry.configure(placeholder_text_color='lightblue', text_color='lightblue')
        self.__repeatRegisterPasswordEntry.configure(placeholder_text_color='lightblue', text_color='lightblue')
        if self.__termsBox.get():
            if not (self.__registerUsernameEntry.get() == '' or self.__registerPasswordEntry.get() == '' or self.__repeatRegisterPasswordEntry.get() == ''):
                if self.__registerPasswordEntry.get() == self.__repeatRegisterPasswordEntry.get():
                    self.__connector = Connector(self.__registerUsernameEntry.get(), self.__registerPasswordEntry.get())

                    if self.__verifier.isDatabaseReachable and self.__connector.register():
                        self.__registrationFeedbackLabel.configure(text='The registration was successful.', text_color='green')
                    else:
                        self.__registrationFeedbackLabel.configure(text='Error during the registration.', text_color='red')

        if self.__registerUsernameEntry.get() == '':
            self.__registerUsernameEntry.configure(placeholder_text_color='red')

        if self.__registerPasswordEntry.get() == '':
            self.__registerPasswordEntry.configure(placeholder_text_color='red')

        if self.__repeatRegisterPasswordEntry.get() == '':
            self.__repeatRegisterPasswordEntry.configure(placeholder_text_color='red')

        if self.__registerPasswordEntry.get() != self.__repeatRegisterPasswordEntry.get():
            self.__repeatRegisterPasswordEntry.configure(text_color='red')

        if not self.__termsBox.get():
            self.__termsBox.configure(text_color='red')

    def __resetPassword(self, event):
        self.__topReset = ctk.CTkToplevel()  # Creates a Toplevel window
        self.__topReset.title('Register')
        self.__x = (self.__screenWidth // 2) - (self.__topReset.winfo_reqwidth() // 2)
        self.__y = (self.__screenHeight // 2) - (self.__topReset.winfo_reqheight() // 2)
        self.__topReset.geometry("+{}+{}".format(self.__x + self.__spawnOffset, self.__y + self.__spawnOffset))
        self.__topReset.geometry(f'{self.__windowWidth}x{self.__windowHeight}')
        self.__topReset.resizable(False, False)
        self.__topReset.attributes('-topmost', True)

        self.__resetTitleLabel = ctk.CTkLabel(self.__topReset, text='Reset password', text_color='lightblue',
                                              font=('@NSimSun', 28, 'bold'))

        self.__resetFeedbackLabel = ctk.CTkLabel(self.__topReset, text='', text_color='lightblue')

        self.__resetUsernameEntry = ctk.CTkEntry(self.__topReset, placeholder_text='Username',
                                                 placeholder_text_color='lightblue', width=270)

        self.__resetOldPasswordEntry = ctk.CTkEntry(self.__topReset, show='*', placeholder_text_color='lightblue',
                                                    placeholder_text='Old password', width=270)

        self.__resetNewPasswordEntry = ctk.CTkEntry(self.__topReset, show='*', placeholder_text_color='lightblue',
                                                    placeholder_text='New password', width=270)

        self.__repeatResetNewPasswordEntry = ctk.CTkEntry(self.__topReset, show='*',
                                                          placeholder_text_color='lightblue',
                                                          placeholder_text='Confirm new password', width=270)

        self.__resetButton = ctk.CTkButton(self.__topReset, text='Reset password', text_color='lightblue',
                                           font=('@NSimSun', 20, 'bold'), command=self.__resetRequest)

        self.__resetTitleLabel.pack(pady=25)
        self.__resetFeedbackLabel.pack()
        self.__resetUsernameEntry.pack(pady=10)
        self.__resetOldPasswordEntry.pack(pady=10)
        self.__resetNewPasswordEntry.pack(pady=10)
        self.__repeatResetNewPasswordEntry.pack(pady=10)
        self.__resetButton.pack(pady=30)

    def __resetRequest(self):
        self.__resetUsernameEntry.configure(placeholder_text_color='lightblue')
        self.__resetOldPasswordEntry.configure(placeholder_text_color='lightblue', text_color='lightblue')
        self.__resetNewPasswordEntry.configure(placeholder_text_color='lightblue', text_color='lightblue')
        self.__repeatResetNewPasswordEntry.configure(placeholder_text_color='lightblue', text_color='lightblue')

        if not (self.__resetUsernameEntry.get() == '' or self.__resetOldPasswordEntry.get() == ''
                or self.__resetNewPasswordEntry.get() == '' or self.__repeatResetNewPasswordEntry.get() == ''):
            if self.__resetNewPasswordEntry.get() == self.__repeatResetNewPasswordEntry.get():

                # Checks for a user with the specified username and the old password
                self.__connector = Connector(self.__resetUsernameEntry.get(), self.__resetOldPasswordEntry.get())

                if self.__verifier.isDatabaseReachable and self.__connector.connect():
                    self.__resetFeedbackLabel.configure(text='User has been found', text_color='green')
                    self.__connector = Connector(self.__resetUsernameEntry.get(), self.__resetNewPasswordEntry.get())
                    if self.__connector.resetPassword():
                        self.__resetFeedbackLabel.configure(text='Successfully changed password', text_color='green')
                    else:
                        self.__resetFeedbackLabel.configure(text='Could not change password', text_color='red')
                else:
                    self.__resetFeedbackLabel.configure(text='No user found', text_color='red')

        if self.__resetUsernameEntry.get() == '':
            self.__resetUsernameEntry.configure(placeholder_text_color='red')

        if self.__resetOldPasswordEntry.get() == '':
            self.__resetOldPasswordEntry.configure(placeholder_text_color='red')

        if self.__resetNewPasswordEntry.get() == '':
            self.__resetNewPasswordEntry.configure(placeholder_text_color='red')

        if self.__resetNewPasswordEntry.get() != self.__repeatResetNewPasswordEntry.get():
            self.__repeatResetNewPasswordEntry.configure(text_color='red')

        if self.__repeatResetNewPasswordEntry.get() == '':
            self.__repeatResetNewPasswordEntry.configure(placeholder_text_color='red')
