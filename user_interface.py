#Simar Cheema
#31075859
#simarc@uci.edu

import tkinter as tk
from tkinter import DISABLED, S, Button, ttk, filedialog
from tkinter.font import NORMAL
from Profile import Post
from Profile import Profile
from ds_messenger import DirectMessenger

class ValueError(Exception):
    pass

class Body(tk.Frame):
    """Draws all of the widgets in the body portion of the root frame."""

    def __init__(self, root, select_callback=None):
        """Sets Body class attribute values upon instantiation and creates a frame to support placing body widgets."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._messages = [Post]
        self.usr = ''
        self._draw()
    
    def node_select(self, event):
        """Update the entry_editor with the full post entry when the corresponding node in the posts_tree is selected."""
        try:
            index = int(self.posts_tree.selection()[0])
            l = list(self._messages.keys())
            for ind, value in enumerate(l):
                if ind == index:
                    self.usr = value
            entry = self._messages[self.usr]['message']
            self.reset_display()
            self.set_text_entry(entry, usr=self.usr)
        except:
            pass

    def get_text_entry(self) -> str:

        """Returns the text that is currently displayed in the text_editor widget."""

        return self.text_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, lst1:list, usr=None):

        """In the display box, function displays the messages in entry_editor widget that You and other User have sent to each other.
            We loop through the lst1 parameter and if the first 6 letters equal '\*sent' then that is your message. Insert to UI the string 'You:' plus YOUR message.
            Else if the first 6 letters do not equal '\*sent' then that is message is another user. Insert to UI their username plus THEIR message."""

        self.entry_editor.configure(state=tk.NORMAL)
        for text1 in lst1:
            if text1[:6] == '*sent:':
                self.entry_editor.insert(0.0, 'You: ' + text1[6:] + '\n')
            else:
                self.entry_editor.insert(0.0, self.usr.capitalize() + ': ' + text1 + '\n')
        self.entry_editor.configure(state=tk.DISABLED)

    def set_posts(self, posts:dict):
        """We use a for loop to iterate through posts which is a dictionary. Inside the for loop, we call the _insert_post_tree function. 
        The first parameter (k) is the index starting at 0 and adding 1 each time. Second parameter (u) is the key of the dictionary (entry). 
        After we loop through the entire dictionary, Set the messages attribute to posts (dictionary)"""

        k = 0
        for u in posts.keys():
            self._insert_post_tree(k, u)
            k += 1
        self._messages = posts

    def reset_display(self):
        """When user presses 'NEW' or 'OPEN' command, we have to reset all previous messages / users on UI with current ones"""
        self.entry_editor.configure(state=tk.NORMAL)
        self.entry_editor.delete(1.0, tk.END)
        self.entry_editor.configure(state=tk.DISABLED)

    def reset_ui(self):
        """Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
            as when a new DSU file is loaded"""

        self.reset_display()
        self._messages = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    def _insert_post_tree(self, id, post: Post):
        """Displays all messages that user has sent text to"""
        self.posts_tree.insert('', id, id, text=post)
    
    def _draw(self):
        # Displays FRAME of left side
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        # Displays the right bottom 
        self.text_editor = tk.Text(editor_frame, width=0, height=8)
        self.text_editor.pack(fill=tk.X, side=tk.BOTTOM, expand=False, padx=0, pady=0)
        self.text_editor.configure(font=('courier', 12, 'normal'), background='white', fg='black')
        # Displays the right top
        self.entry_editor = tk.Text(editor_frame, width=0, height=25)
        self.entry_editor.configure(state=tk.DISABLED)
        self.entry_editor.pack(fill='both', side=tk.TOP, expand=True, padx=0, pady=0)
        self.entry_editor.configure(font=('courier', 12, 'normal'), background='white', fg='black')     ##CECCBE

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Drawing all of the widgets in the footer portion of the root frame."""

    def __init__(self, root, save_callback=None, online_callback=None):
        """Sets Footer class attribute values upon instantiation and creates a frame to support placing widgets."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        self.is_online = tk.IntVar()
        self._click = False
        self._draw()

    def save_click(self):
        """There is a checkbox buttom for user to clicked. If checkbox is clicked, this function will execute.
            Calls the _save_callback function."""
        if self._save_callback is not None:
            self._save_callback()

    def set_status(self, message):
        """Updates the text that is displayed in the footer_label widget"""
        self.footer_label.configure(text=message)

    def online_click(self):
        """Calls the callback function specified in the online_callback class attribute, if available, when the chk_button widget has been clicked."""
        if self._online_callback is not None:
            self._online_callback(self.is_online.get())

    def _draw(self):
        """Call only once upon initialization to add widgets to the frame"""
        save_button = tk.Button(master=self, text="Send Message", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

        self.chk_button = tk.Checkbutton(master=self, text="Dark Mode", variable=self.is_online)
        self.chk_button.configure(command=self.online_click) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

class MainApp(tk.Frame):
    """Responsible for drawing all of the widgets in the main portion of the root frame. Also manages all method calls for
        the NaClProfile class."""

    def __init__(self, root):
        """Sets MainApp class attribute values upon instantiation and creates a frame to support placing widgets."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._is_online = False
        self._profile_filename = None
        self._current_profile = Profile()
        self._draw()

    def check_something(self):
        """This function allows user to send a message to another user. When the send message is clicked, the message that user created will be sent from their device
            to the other person's device. Message should appear on both devices."""
        s = self.body.get_text_entry()
        self.new = self.dm.retrieve_new(self._profile_filename)
        self.body.text_editor.delete(1.0, tk.END)
        self.body.text_editor.insert(0.0, '')
        if self.new != []:
            self._current_profile.load_profile(self._profile_filename)
            self.dm = DirectMessenger('168.235.86.101', self._current_profile.username, self._current_profile.password, self._profile_filename)
            self.body._messages = self._current_profile.get_sent()
            if self.body.usr != '':
                entry = self.body._messages[self.body.usr]['message']
                self.body.reset_display()
                self.body.set_text_entry(entry)
                self._current_profile.save_profile(self._profile_filename)
        self.root.after(3000, self.check_something)
        self.body.text_editor.insert(0.0, s)


    def open_profile(self):
        """When user clicks on the 'OPEN' menu item, they can choose an existing dsu file to open. All messages / users data are displayed on UI."""
        try:
            filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
            self._profile_filename = filename.name
            self._current_profile = Profile()
            self._current_profile.load_profile(self._profile_filename)
            self.dm = DirectMessenger('168.235.86.101', self._current_profile.username, self._current_profile.password, self._profile_filename)
            self.body.reset_ui()
            self.body.set_posts(self._current_profile.get_sent())
            main.after(3000, app.check_something) 
        except:
            print('Can not open file. Try again.')
 
    def close(self):
        """When user clicks on the 'CLOSE' menu item, progam closes/"""
        self.root.destroy()

    def send_message(self):
        """Saves the text currently in the entry_editor widget to the active DSU file."""
        string = self.body.get_text_entry()
        self.dm.send(string, self.body.usr, self._profile_filename)
        self.body.text_editor.delete(1.0, tk.END)
        self.body.text_editor.insert(0.0, '')
        self._current_profile.load_profile(self._profile_filename)
        self.body._messages = self._current_profile.get_sent()
        entry = self.body._messages[self.body.usr]['message']
        self.body.reset_display()
        self.body.set_text_entry(entry)

    def add_user(self):
        """In the menu option, there is a 'ADD USER' buttom for user to add another to send messages to. When option is clicked,
            a new UI will appear, asking for a username. User presses 'SUBMIT' when done."""
        self.add = tk.Tk()
        self.add.title('Add User')
        self.body.user_frame = tk.Frame(master=self.add, width=300, height=200)
        self.body.user_frame.pack()
        self.body.label = tk.Label(self.body.user_frame, text='Username:')
        self.body.label.place(x=30, y=50)
        self.body.entry = tk.Entry(self.body.user_frame)
        self.body.entry.place(x=100, y=50)
        self.body.button = tk.Button(self.body.user_frame, text = "Submit", command = self.submit)
        self.body.button.place(x=150, y=120)
    
    def submit(self):
        """'SUMBIT occurs when user wants to add another user to talk to. If user enters name that already exist, pass. If new name then save to profile and set name 
            on left side of UI.'"""
        user = self.body.entry.get()
        i = {'message': [], 'timestamp': []}
        self.add.destroy()
        self.body.reset_ui()
        if user in self._current_profile.sent:
            pass
        else:
            self._current_profile.sent[user] = i
            self._current_profile.save_profile(self._profile_filename)
        self._current_profile.load_profile(self._profile_filename)
        self.body.set_posts(self._current_profile.get_sent())

    def online_changed(self, value:bool):
        """Sets the main app's Display to Dark Mode or Light."""
        try:
            if value == 1:
                self.footer.set_status('Dark Mode')
                self._is_online = True
                self.body.entry_editor.configure(font=('courier', 12, 'normal'), background='#2B2B2B', fg='green')     ##2B2B2B
                self.body.text_editor.configure(font=('courier', 12, 'normal'), background='#2B2B2B', fg='green') 

            else:
                self.footer.set_status('Light Mode')
                self._is_online = False
                self.body.entry_editor.configure(font=('courier', 12, 'normal'), background='white', fg='black')     ##CECCBE
                self.body.text_editor.configure(font=('courier', 12, 'normal'), background='white', fg='black')     ##CECCBE
        except:
            raise ValueError('A value error occured when changing to Dark Mode')

    def _draw(self):
        """Call only once, upon initialization to add widgets to root frame. Build menu that adds to root frame."""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Open', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        menu_file.add_command(label='Add User', command=self.add_user)
        # menu_file.add_command(label='Dark Mode', command=self.add_user)
        """The Body and Footer classes must be initialized and packed into the root window."""
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, save_callback=self.send_message, online_callback=self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()
    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("Private Messenger")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)
    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    app = MainApp(main)


    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())

    # main.after(3000, app.check_something) 

    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
