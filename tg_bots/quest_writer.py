import tkinter as tk
from tkinter import messagebox
import json

import terms


def from_list_to_string(list_):
    text = ''
    for item in list_:
        text = '{} {},'.format(text, item)
    return text


DATA_FILE_NAME = 'data.json'


class QuestWriter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Text Quest Creator')
        self.root.geometry('800x700')

        self.text_area = tk.Text(self.root, width=95, height=20)
        self.text_area.bind("<Key>", lambda e: self.ctrl_event(e))
        self.pages = []

        # loading file if exists, creating new if not
        try:
            with open(DATA_FILE_NAME, 'r') as fn:
                self.data = json.load(fn)
        except FileNotFoundError:
            self.make_new_game()
        # self.id is the id of current page
        self.id = len(self.data) - 1
        # self.current_data is the data of current page
        self.current_data = self.make_current_data()

        self.update_pages_id()

        # region WIDGETS
        self.menu_var = tk.StringVar()
        self.menu_var.set('{}'.format(self.pages[-1]))

        tk.Label(self.root, text='Choose the page: ').place(x=10, y=13)

        self.om1 = tk.OptionMenu(self.root, self.menu_var, *self.pages, command=self.select_id_from_option_menu)
        self.om1.place(x=130, y=10)

        self.page_id_var = tk.StringVar()
        self.set_page_id_string_var()
        tk.Label(self.root, textvariable=self.page_id_var).place(x=10, y=50)

        self.links_from = tk.StringVar()
        self.set_links_from_var()
        tk.Label(self.root, textvariable=self.links_from).place(x=10, y=70)

        self.text_area.place(x=10, y=100)
        self.text_area.insert('1.0', self.current_data.get(terms.QUEST_TEXT))

        self.entry_war = tk.StringVar()
        tk.Entry(self.root, textvariable=self.entry_war, width=60).place(x=10, y=450)

        tk.Button(self.root, text='Add new button', command=self.add_button).place(x=400, y=445)

        tk.Label(self.root, text='Link to existing page (if need): ').place(x=530, y=450)

        self.link_for_button_var = tk.StringVar()
        self.om2 = tk.OptionMenu(self.root, self.link_for_button_var, *self.pages)
        self.om2.place(x=700, y=443)

        tk.Label(self.root, text='Added buttons (click on button to go to the page it links):').place(x=10, y=500)

        tk.Button(self.root, text='SAVE PROJECT TO FILE', command=self.write_to_file).place(x=650, y=70)
        # endregion

        self.buttons = []
        self.del_buttons = []
        self.show_created_buttons()

    # adding copy/paste event by <CTRL+C>/<CTRL+V> to text area
    def ctrl_event(self, event):
        if event.state == 4 and event.keysym == 'c':
            content = self.text_area.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            return "break"
        elif event.state == 4 and event.keysym == 'v':
            self.text_area.insert('end', self.root.selection_get(selection='CLIPBOARD'))
            return "break"
        else:
            pass

    # starting new game
    def make_new_game(self):
        self.data = []
        self.create_new_page(new_game=True)
        self.text_area.insert(1.0, 'Delete this text and fill it with your own, this will be the main text of the page.'
                                   '\n\nClick on the "SAVE PROJECT TO FILE" button to save all data to a file. '
                                   'You can save to a \nfile before finishing work. Until then, all intermediate '
                                   'changes are stored in the program\'s \nmemory until you save or close the program. '
                                   '\n\nTo add buttons to the page, use the form below. If you specify a link to '
                                   'an existing page \nnext to the "Add new button" button, the button will lead to it,'
                                   ' otherwise a new page will be \ncreated and the button will lead to it. '
                                   '\n\nIf you click on the created button, you will be taken to the page to which'
                                   ' this button links. \nYou can go to any page of the quest by clicking on its'
                                   ' number in the list above. \n\nThe author wishes you successes in your work!\n'
                                   'Let\'s do some nice content!')

    # updating page`s id in the list for correct view in OptionMenu widgets
    def update_pages_id(self):
        self.pages.clear()
        for page in self.data:
            self.pages.append(page.get(terms.PAGE_ID))

    # updating OptionMenu widgets
    def set_new_om(self):
        self.om1.destroy()
        self.om1 = tk.OptionMenu(self.root, self.menu_var, *self.pages,
                                 command=self.select_id_from_option_menu)
        self.om1.place(x=130, y=10)
        self.om2.destroy()
        self.om2 = tk.OptionMenu(self.root, self.link_for_button_var, *self.pages)
        self.om2.place(x=700, y=443)

    # adding new link button to the page
    def add_button(self):
        b_text = self.entry_war.get()
        b_id = self.link_for_button_var.get()
        last_id = str(len(self.data))

        if b_text == '':
            messagebox.showerror('An error has occurred', 'Button\'s text field can\'t be empty')
            return
        if b_id == '':
            b_id = last_id
        button = {terms.BUTTON_ID: b_id, terms.BUTTON_TEXT: b_text}
        self.current_data.get(terms.BUTTONS).append(button)
        if b_id == last_id:
            self.create_new_page()
        else:
            self.data[int(b_id)].get(terms.LINKS_FROM).append(self.id)

        self.entry_war.set('')
        self.link_for_button_var.set('')
        self.save_to_data()
        self.renew()

    # adding new page to project
    def create_new_page(self, new_game=False):
        page_id = 0 if new_game else len(self.data)
        page = {terms.PAGE_ID: page_id, terms.QUEST_TEXT: "", terms.BUTTONS: [], terms.LINKS_FROM: []}
        if not new_game:
            page[terms.LINKS_FROM].append(self.id)
        self.data.append(page)

    # temporarily saving data
    def save_to_data(self):
        self.current_data[terms.QUEST_TEXT] = self.text_area.get(1.0, tk.END)
        self.data[self.id] = self.current_data

    # refreshing all
    def renew(self):
        self.update_pages_id()
        self.set_page_id_string_var()
        self.current_data = self.make_current_data()
        self.set_new_om()
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert('1.0', self.current_data.get(terms.QUEST_TEXT))
        self.set_links_from_var()
        self.show_created_buttons()

    # showing already created buttons
    def show_created_buttons(self):
        for btn in self.buttons:
            btn.destroy()
        for btn_ in self.del_buttons:
            btn_.destroy()
        self.buttons.clear()
        self.del_buttons.clear()
        start = 520
        step = 30
        for button in self.current_data.get(terms.BUTTONS):
            btn = tk.Button(self.root, text=button.get(terms.BUTTON_TEXT),
                            command=lambda button_=button: self.go_to_new_page(button_.get(terms.BUTTON_ID)))
            btn.place(x=60, y=start)
            self.buttons.append(btn)

            del_btn = tk.Button(self.root, text='Update',
                                command=lambda button_=button: ChangeButtonPopup(self, 'Button updating', 300, 200,
                                                                                 self.current_data.get(terms.BUTTONS)
                                                                                 .index(button_)))
            del_btn.place(x=10, y=start)
            self.del_buttons.append(del_btn)
            start += step

    # going to new page by id
    def go_to_new_page(self, page_id):
        self.save_to_data()
        self.id = int(page_id)
        self.renew()

    # setting links from parent pages
    def set_links_from_var(self):
        self.links_from.set('Links from other pages to this: {}'.format(from_list_to_string(self.current_data.
                                                                                            get(terms.LINKS_FROM))))

    # showing current page's id
    def set_page_id_string_var(self):
        self.page_id_var.set('ID of current page {}'.format(self.id))

    # getting self.current_data
    def make_current_data(self):
        return self.data[self.id]

    # saving game to file
    def write_to_file(self):
        self.save_to_data()
        self.renew()
        try:
            with open(DATA_FILE_NAME, 'w') as fn:
                json.dump(self.data, fn, indent=4)
        except Exception as e:
            messagebox.showerror('An error has occurred', 'Something went wrong')
            print(e)
        else:
            messagebox.showinfo('Success', 'Data saved to data.json file')

    # changing page by click to OptionMenu id
    def select_id_from_option_menu(self, event):
        self.save_to_data()
        self.id = int(self.menu_var.get())
        self.renew()

    # running program
    def run(self):
        self.root.mainloop()


class ChangeButtonPopup(tk.Toplevel):
    def __init__(self, app, title, w, h, button_index):
        super().__init__(app.root)
        self.app = app
        self.geometry('{}x{}'.format(w, h))
        self.grab_set()
        self.focus_force()
        self.title(title)
        self.button_index = button_index
        self.button = self.app.current_data.get(terms.BUTTONS)[self.button_index]
        self.entry_var = tk.StringVar()
        self.menu_var = tk.StringVar()
        self.entry_var.set(self.button.get(terms.BUTTON_TEXT))
        self.menu_var.set(self.button.get(terms.BUTTON_ID))
        tk.Label(self, text='Text of the button \n(if you want to remove button, delete text from field)').pack()
        tk.Entry(self, textvariable=self.entry_var, width=40).pack()
        tk.Label(self, text='Link of the button').pack()
        tk.OptionMenu(self, self.menu_var, *app.pages).pack()
        tk.Button(self, text='Update and close', command=self.change).pack()

    def change(self):
        button_text = self.entry_var.get()
        button_id = self.menu_var.get()
        del_id = self.button.get(terms.BUTTON_ID)
        if button_text == '':
            self.app.data[int(del_id)].get(terms.LINKS_FROM).remove(self.app.id)
            self.app.current_data.get(terms.BUTTONS).remove(self.button)
        else:
            button = {
                terms.BUTTON_ID: button_id,
                terms.BUTTON_TEXT: button_text
            }
            if del_id != button_id:
                self.app.data[int(del_id)].get(terms.LINKS_FROM).remove(self.app.id)
                self.app.data[int(button_id)].get(terms.LINKS_FROM).append(self.app.id)
            self.app.current_data.get(terms.BUTTONS)[self.button_index] = button

        self.app.save_to_data()
        self.app.renew()
        self.destroy()


if __name__ == '__main__':
    QuestWriter().run()
