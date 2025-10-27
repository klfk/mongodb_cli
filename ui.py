import curses
from curses.textpad import Textbox, rectangle
import time
import sys


class UI:

    def actions_receiver(self, win, action, key):
        if action == "move" and key:
            if key == "KEY_UP" and self.selected_item > 0:
                self.selected_item -= 1
            elif key == "KEY_DOWN" and self.selected_item < len(self.items) - 1:
                self.selected_item += 1
            self.draw_items(win, self.items, self.selected_item, self.title)
            
        elif action == "choose":
            return self.selected_item
    
    def key_sender(self, win):
        key = win.getkey()
        return key

    def draw_items(self, win, items, selected_item, title):
        win.clear()
        

        height, width = self.stdscr.getmaxyx()
        center = int(width / 2 - 4)

        self.stdscr.move(4, 0)
        self.stdscr.clrtoeol()
        
        self.title = title
        self.stdscr.addstr(4, center, self.title, self.BLACK_GREEN)
        self.stdscr.refresh()

        for i, item in enumerate(items):
            if i == selected_item:
                win.addstr(i+1, 2, item, self.REVERSED)
            else:
                win.addstr(i + 1, 2, item)
        rectangle(win, 0,0, len(items)+2,28)
        win.refresh()

        win.move(0,1)

    def make_ui(self, stdscr, itemstotal): #global


        stdscr.clear() 
        height, width = stdscr.getmaxyx()
        stdscr.resize(height, width)

        stdscr.attron(self.BLACK_GREEN)
        stdscr.attron(self.REVERSED)
        stdscr.border()
        stdscr.attroff(self.REVERSED)
        stdscr.attroff(self.BLACK_GREEN)

        center = int(width / 2 - 5)
        stdscr.addstr(2, center, " mongodb cli ", self.BLACK_GREEN)
        
        stdscr.addstr(height-2, 2, 'arrows - move, enter - select, esc - cancel, q - quit')
        stdscr.noutrefresh()

        win = curses.newwin(10, 30, 15, 10)
        win.leaveok(False)
        win.keypad(True)

        win.noutrefresh()
        
        curses.doupdate()

        
        return win
    
    def input_textbox(self, context, msg):
        self.context = context

        context.stdscr.addstr(10,10, msg)
        context.stdscr.refresh()
        boxwin = curses.newwin(3, 44, 11, 10)
        textwin = curses.newwin(1, 40, 12,11) 
        textbox = Textbox(textwin)
        

        boxwin.attron(self.BLACK_GREEN)
        boxwin.attron(self.REVERSED)
        rectangle(boxwin, 0, 0, 2, 41)
        boxwin.attroff(self.REVERSED)
        boxwin.attroff(self.BLACK_GREEN)

        boxwin.refresh()
        textwin.refresh()

        textbox.edit()
        
        user_input = textbox.gather().strip().replace("\n", "")
        
        context.stdscr.move(10, 10)
        context.stdscr.clrtoeol()
        boxwin.clear()
        boxwin.refresh()
        textwin.clear()
        textwin.refresh()
        context.stdscr.refresh()
        
        return user_input

    def query_result_behaviour(self):
        x=y=0
        max_y, max_x = self.stdscr.getmaxyx()
        pad_right = min(max_x - 1, 120)
        pad_bottom = min(max_y - 1, 19)
        
        self.query_pad.refresh(0, 0, 7, 62, pad_bottom, pad_right)
        
        if isinstance(self.query_result, str):
            while True:
                key = self.query_pad.getkey()
                if key == "q" or key == "Q":
                    sys.exit()
                elif key == "\x1b" or key == "\n":  # ESC or Enter key
                    return
            return
        
        selected_object = self.selected_object = 0
        if self.query_data:
            formatted_doc = self.format_document(self.query_data[selected_object])
            self.query_pad.addstr(y, 0, formatted_doc, self.REVERSED)
            self.query_pad.refresh(y, x, 7, 62, pad_bottom, pad_right)

        while True:
            if not self.query_data:
                key = self.query_pad.getkey()
                if key == "q" or key == "Q":
                    sys.exit()
                elif key == "\x1b":
                    return
                continue
                
            key = self.query_pad.getkey()
            prev_selected_object = selected_object
            prev_selected_object_y = y

            if key == "KEY_RIGHT":
                x = x+1
            elif key == "KEY_LEFT":
                x= x-1
            elif key == "KEY_UP":
                y = max(0, y-1)
                selected_object = y 
            elif key == "KEY_DOWN":
                y= min(len(self.query_data) - 1, y + 1)
                selected_object = y  
            elif key == "q" or key == "Q":
                sys.exit()
            elif key == "\x1b":
                return
            elif key == "\n":
                break

            
            self.query_pad.addstr(prev_selected_object_y, 0, self.format_document(self.query_data[prev_selected_object]))
            self.query_pad.addstr(y, 0, self.format_document(self.query_data[selected_object]), self.REVERSED)
            self.query_pad.refresh(y, x, 7, 62, pad_bottom, pad_right)

        objectID = str(self.query_data[selected_object]['_id'])
        self.y = y
        self.selected_object = selected_object
        self.show_chosen_object()
        self.context.actions("update_delete", objectID)
            
    
    def draw_query_objects(self):
        if isinstance(self.query_result, str):
            max_width = self.query_pad.getmaxyx()[1] - 1
            display_text = self.query_result[:max_width] if len(self.query_result) > max_width else self.query_result
            self.query_pad.addstr(0, 0, display_text)
        else:
            for doc in self.query_result:
                self.query_data.append(doc)
    
            for i, obj in enumerate(self.query_data):
                try:
                    formatted_doc = self.format_document(obj)
                    self.query_pad.addstr(i, 0, formatted_doc[:2900])
                except curses.error:
                    break
                    
    def format_document(self, doc):
        formatted_lines = []
        for key, value in doc.items():
            if key == '_id':
                formatted_lines.append(f"id: {value}")
            else:
                formatted_lines.append(f"{key}: {value}")
        return " | ".join(formatted_lines)
        
    
    def show_query_result(self):
        self.query_data = []

        max_y, max_x = self.stdscr.getmaxyx()
        
        win_width = min(70, max_x - 60)
        win_height = min(20, max_y - 6)
        
        query_rectangle_win = curses.newwin(win_height, win_width, 6, 60)
        query_rectangle_win.box()
        query_rectangle_win.refresh()

        self.query_pad = curses.newpad(200, 3000)
        self.query_pad.keypad(True)
        self.query_pad.leaveok(False)
        self.query_pad.clear()


    def show_chosen_object(self): #show single object in a query to modify it
        self.query_pad.clear()
        # Get terminal dimensions
        max_y, max_x = self.stdscr.getmaxyx()
        pad_right = min(max_x - 1, 120)
        pad_bottom = min(max_y - 1, 19)
        
        formatted_doc = self.format_document(self.query_data[self.selected_object])
        self.query_pad.addstr(self.y, 0, formatted_doc, self.REVERSED)
        self.query_pad.refresh(0, 0, 7, 62, pad_bottom, pad_right)



    
    def message(self, text):
        msgwin = curses.newwin(3, 60, 7,10)
        msgwin.box()
        msgwin.addstr(1,1,text)
        msgwin.refresh()
        time.sleep(2)  # Reduced from 4 to 2 seconds
        msgwin.clear()
        msgwin.refresh()

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        
        #to make more understandable
        self.BLACK_GREEN = curses.color_pair(1)
        self.REVERSED = curses.A_REVERSE

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.init_colors()
        self.selected_item = 0
        self.items = []