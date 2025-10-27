import curses
from menus import Main, Search, Create, Update_Delete
import ui
from dbclient import DBClient


class Context: #shared dependencies class, to avoid a hundred trillion arguments when creating menus
    def __init__(self, stdscr, win, ui, actions, dbclient, app):
        self.stdscr = stdscr
        self.win = win
        self.ui = ui
        self.actions = actions
        self.dbclient = dbclient
        self.app = app
        
class App:

    def actions(self, menu, objectID=None): 
        curses.curs_set(1) 
        if menu == "main":
            self.current_menu = Main(self.context)
        elif menu == "search":
            self.current_menu = Search(self.context)
        elif menu == "create":
            self.current_menu = Create(self.context)
        elif menu == "update_delete":
            self.current_menu = Update_Delete(self.context, objectID)



    def run(self):
        while True:
            try:
                self.current_menu.key_receiver(self.current_menu) #this attribute is needed for method choose in Basemenu
            except KeyboardInterrupt:
                break

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.ui = ui.UI(stdscr)
        self.win = self.ui.make_ui(stdscr, 3) 
        self.context = Context(self.stdscr, self.win, self.ui, self.actions, DBClient(), self) 
        self.current_menu = Main(self.context)

        self.run()


def main(stdscr):
    app = App(stdscr)

curses.wrapper(main)




"""    win = curses.newwin( 3, 18, 2, 2)f
        box = Textbox(win)
        rectangle(stdscr, 1, 1, 5, 20)
        
        stdscr.refresh()

        box.edit()
        text = box.gather().strip().replace("\n", "")
        stdscr.addstr(10, 40, text)

        stdscr.getch()

"""

