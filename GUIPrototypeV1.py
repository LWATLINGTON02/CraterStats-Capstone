import tkinter as tk
import craterstats
import time
import os

# from typelock_client import Signup, Login  # Connection to the Client Program

# Initialize the list of lists to store the keypress data
keypress_data = []

# Log the character entered by the user and the time it was pressed
def log_key_press(event):
    # Record the current time (in seconds)
    current_time = time.time()
    # Append the key event name (letter) and the time it was pressed
    keypress_data.append([event.char, current_time])


class TkTemplate(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (GetStartedPage, FormatPage, StatsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GetStartedPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GetStartedPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#1F1F1E")
        self.controller = controller

        #image_path = os.path.join(os.getcwd(), "TypeLock-Logo.png")

#         logo_image = tk.PhotoImage(file=image_path)
#         logo_label = tk.Label(self, image=logo_image, bg="#1F1F1F")
#         logo_label.image = logo_image
#         logo_label.pack(pady=10)

        # Create and format the welcome label
        welcome_label = tk.Label(self, text="Welcome to CraterStats",
                                 font=("Nunito", 18),
                                 fg="#FFFFFF",
                                 bg="#1F1F1F")
        welcome_label.pack(pady=(10, 5))

        # Create and format the "Crater Graph Statistics Settings" label
        graph_stats_label = tk.Label(self,
                               text="Crater Graph Statistics Settings",
                                  font=("Nunito", 16),
                                  fg="#FFFFFF",
                                  bg="#1F1F1F")
        graph_stats_label.pack(anchor=tk.W, pady=(10, 0), padx=179)

        # Create the stats button and redirect to the graph statistics
        # settings page
        stats_button = tk.Button(self, width=20,
                                  text="Stats",
                                  font=("Nunito", 16),
                                  bg="#FFFFFF",
                                  fg="#1F1F1F",
                                  command=lambda: controller.
                                  show_frame(StatsPage))
        stats_button.pack(pady=(0, 10))

        # Create and format the "Graph Format Settings" label
        graph_format_label = tk.Label(self, text="Graph Format Settings",
                                       font=("Nunito", 16),
                                       fg="#FFFFFF",
                                       bg="#1F1F1F")
        graph_format_label.pack(anchor=tk.W, pady=(10, 0), padx=179)

        # Create the format button and redirect to the format page
        format_button = tk.Button(self, width=20,
                                 text="Format",
                                 font=("Nunito", 16),
                                 bg="#FFFFFF",
                                 fg="#1F1F1F",
                                 command=lambda: controller.
                                 show_frame(FormatPage))
        format_button.pack(pady=(0, 10))


class FormatPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#1F1F1F")
        self.controller = controller

        #logo_image = tk.PhotoImage(file="TypeLock-Logo.png")
        #logo_label = tk.Label(self, image=logo_image, bg="#1F1F1F")
        #logo_label.image = logo_image
        #logo_label.pack(pady=10)

        # Show the placeholder text for the entry boxes
        def show_placeholder(event, entry, placeholder):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(fg="#808080")

        # Hide the placeholder text for the entry boxes
        def hide_placeholder(event, entry, placeholder):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(fg="#1F1F1F")

        # Create and format the LOGIN label
        login_label = tk.Label(self, text="Login",
                               font=("Nunito", 18),
                               fg="#FFFFFF",
                               bg="#1F1F1F")
        login_label.pack(pady=(10, 5))

        # Create and format the username label
        username_label = tk.Label(self, text="Username",
                                  font=("Nunito", 16),
                                  fg="#FFFFFF",
                                  bg="#1F1F1F")
        username_label.pack(anchor=tk.W, pady=(10, 0), padx=191)

        # Create and format the username entry box with placeholder text
        username_placeholder = "Type your username"
        username_entry_box = tk.Entry(self, width=20,
                                      font=("Nunito", 16),
                                      bg="#FFFFFF",
                                      fg="#808080",
                                      insertbackground="#FFFFFF")
        username_entry_box.insert(0, username_placeholder)
        username_entry_box.bind("<FocusIn>",
                                lambda event: hide_placeholder(
                                    event,
                                    username_entry_box,
                                    username_placeholder))
        username_entry_box.bind("<FocusOut>",
                                lambda event: show_placeholder(
                                    event,
                                    username_entry_box,
                                    username_placeholder))
        username_entry_box.pack(pady=(0, 10))

        # Create and format the passphrase label
        passphrase_label = tk.Label(self, text="Passphrase",
                                    font=("Nunito", 16),
                                    fg="#FFFFFF",
                                    bg="#1F1F1F")
        passphrase_label.pack(pady=(10, 0))

        # Create the passphrase
        passphrase = "hello world"

        # Display the passphrase
        passphrase_text_label = tk.Label(self, text=f"{passphrase}",
                                         font=("Nunito", 16, "bold"),
                                         fg="#FFFFFF", bg="#1F1F1F")
        passphrase_text_label.pack(pady=(0, 10))

        # Create and format the passphrase entry box with placeholder text
        passphrase_placeholder = "Type the passphrase"
        passphrase_entry_box = tk.Entry(self, width=20,
                                        font=("Nunito", 16),
                                        bg="#FFFFFF",
                                        fg="#808080",
                                        insertbackground="#FFFFFF")
        passphrase_entry_box.insert(0, passphrase_placeholder)
        passphrase_entry_box.bind("<FocusIn>",
                                  lambda event: hide_placeholder(
                                      event,
                                      passphrase_entry_box,
                                      passphrase_placeholder))
        passphrase_entry_box.bind("<FocusOut>",
                                  lambda event: show_placeholder(
                                      event,
                                      passphrase_entry_box,
                                      passphrase_placeholder))
        passphrase_entry_box.pack(pady=(0, 10))

        # Record the data entered inside the password entry box
        passphrase_entry_box.bind("<KeyPress>", log_key_press)

        # Login the user and ouput the data entered
        def login_user():
            username_entered = username_entry_box.get()
            passphrase_entered = passphrase_entry_box.get()
            print(f"Username Entered: {username_entered}")
            print(f"Passphrase Entered: {passphrase_entered}")
            print("Keypress data:", keypress_data)

            # Call client and send data; Login needs to return result
            login = Login(keypress_data, username_entered, passphrase)

            # Get success/fail value from client
            login_result = login.user_login()

            print("Login value: " + str(login_result))

            # Check if the login was successful
            if login_result:
                # Redirect to the Success Page
                controller.show_frame(LoginSuccessPage)
            # Otherwise, assume the login wasn't successful
            else:
                # Redirect to the Failure Page
                controller.show_frame(LoginFailurePage)

            # Clear and reset the information
            clear_and_reset()

        # Create the login button
        login_button = tk.Button(self, width=10,
                                 text="Login",
                                 font=("Nunito", 16),
                                 bg="#FFFFFF",
                                 fg="#1F1F1F",
                                 command=login_user)
        login_button.pack(pady=10)

        # Clear the text from the username and passphrase entry boxes and reset
        def clear_and_reset():
            global keypress_data

            # Unbind the key press event from the passphrase entry box
            passphrase_entry_box.unbind("<KeyPress>")

            # Clear the text from the username and passphrase entry boxes
            username_entry_box.delete(0, tk.END)
            passphrase_entry_box.delete(0, tk.END)

            # Reset the keypress_data list
            keypress_data = []

            # Bind the key press event to the passphrase entry box again
            passphrase_entry_box.bind("<KeyPress>", log_key_press)

            # Reset placeholders
            show_placeholder(None, username_entry_box, username_placeholder)
            show_placeholder(None, passphrase_entry_box,
                             passphrase_placeholder)

        # Create the clear button
        clear_button = tk.Button(self, width=10,
                                 text="Clear",
                                 font=("Nunito", 16),
                                 bg="#FFFFFF",
                                 fg="#1F1F1F",
                                 command=clear_and_reset)
        clear_button.pack(pady=0)

        # Create and format the "Need an account?" label
        need_account_label = tk.Label(self, text="Need an account?",
                                      font=("Nunito", 16),
                                      fg="#FFFFFF",
                                      bg="#1F1F1F")
        need_account_label.pack(pady=(10, 0))

        # Create and format the "SIGNUP" label
        signup_label = tk.Label(self, text="SIGNUP",
                                font=("Nunito", 16, "underline"),
                                fg="#FFFFFF",
                                bg="#1F1F1F")
        signup_label.pack(pady=(0, 10))

        # Bind the hover and click events to the "SIGNUP" label
        signup_label.bind("<Enter>", self.on_signup_hover)
        signup_label.bind("<Leave>", self.on_signup_leave)
        signup_label.bind("<Button-1>",
                          lambda event: controller.show_frame(StatsPage))

    # Change the "SIGNUP" text color when the mouse hovers over it
    def on_signup_hover(self, event):
        event.widget.config(fg="#F3AF4E")  # Change to the desired hover color

    # Reset the "SIGNUP" text color when the mouse leaves it
    def on_signup_leave(self, event):
        event.widget.config(fg="#FFFFFF")  # Reset to the original color


class StatsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#1F1F1F")
        self.controller = controller

#         logo_image = tk.PhotoImage(file="TypeLock-Logo.png")
#         logo_label = tk.Label(self, image=logo_image, bg="#1F1F1F")
#         logo_label.image = logo_image
#         logo_label.pack(pady=10)

        PLOTS = [
                 (" cumulative ", "cumulativeCmd"),
                 ("differential", "differentialCmd"),
                 ("relative (R)", "relativeCmd"),
                 ("  Hartmann  ", "HartmannCmd"),
                 (" chronology ", "chronologyCmd")
                ]
        
        plotType = tk.StringVar()
        chronoVar = tk.StringVar()
        # set the chronoVar default variable
        chronoVar.set("Default")
        showTitle = tk.IntVar()

        # Create and format the crater_stats_label label
        crater_stats_label = tk.Label(self, text="Input Crater Stats",
                                      font=("Nunito", 18),
                                      fg="#FFFFFF",
                                      bg="#1F1F1F")
        crater_stats_label.pack(pady=(10, 5))

        # Create and format the plot_type_label
        plot_type_label = tk.Label(self, text="Plot Type:",
                                   font=("Nunito", 16),
                                   fg="#FFFFFF",
                                   bg="#1F1F1F")
        plot_type_label.pack(anchor=tk.W, pady=(10, 0), padx=191)

        # Loop to create and format the plot type radio buttons
        for text, cmd in PLOTS:
            tk.Radiobutton(self, text=text, variable=plotType,
                           value=cmd).pack()

        # Create and format the chronology_function_label
        chronology_function_label = tk.Label(self, text="Chronology Function:",
                                             font=("Nunito", 16),
                                             fg="#FFFFFF",
                                             bg="#1F1F1F")
        chronology_function_label.pack(pady=(10, 0))
        
        # Create and format the chornology function dropdown menu
        chronoDrop = tk.OptionMenu(self, chronoVar,
                                   "chrono1",
                                   "chrono2",
                                   "chrono3").pack()
        
        # Create and format the graph_title_label
        graph_title_label = tk.Label(self, text="Graph Title:",
                                     font=("Nunito", 16),
                                     fg="#FFFFFF",
                                     bg="#1F1F1F")
        graph_title_label.pack(pady=(10, 0))
        
        # Create and format the title display checkbox
        titleCheck = tk.Checkbutton(self, text="Display Title",
                                    variable=showTitle).pack()



app = TkTemplate()
app.title("TkTemplate")
app.geometry("600x800")
app.configure
app.mainloop()
