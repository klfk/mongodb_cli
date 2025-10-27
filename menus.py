import sys

class BaseMenu:
    def move_by_int(self): # some day...
        pass

    def key_receiver(self, current_menu):
        self.current_menu = current_menu
        if self.name == "create":
            should_go_to_main = self.enter_values()
            # Always go to main menu after create process (whether completed or canceled)
            self.actions("main")
            return
        while True:
            key = self.ui.key_sender(self.win)
            if key == "q" or key == "Q": 
                sys.exit()
            elif key == "KEY_UP" or key == "KEY_DOWN":
                self.ui.actions_receiver(self.win, "move", key)
            elif key.isdigit():
                self.move_by_int()
            elif key == "\n":  # Enter key
                self.selected_item = self.ui.actions_receiver(self.win, "choose", None)
                self.choose()
                return
    
    def input_attrs_loop(self):
        attr_list = ['name', 'art', 'jahr', 'regisseur', 'schauspieler', 'rating', 'min_alter', 'bemerkungen']
        input_list = []
        for i in attr_list:
            input = self.ui.input_textbox(self.context, f"please type value for: {i} (or .exit to cancel)")
            if input == ".exit":
                return None
            input_list.append(input)
        return input_list
    def __init__(self, context):
        self.context = context
        self.win = context.win
        self.ui = context.ui
        self.stdscr = context.stdscr
        self.actions = context.actions
        self.dbclient = context.dbclient

        self.attr_list = ['name', 'art', 'jahr', 'regisseur', 'schauspieler', 'rating', 'min_alter', 'bemerkungen']

class Main(BaseMenu):
    def choose(self):
        if self.selected_item == 0:
            self.actions("search")
        elif self.selected_item == 1:
            self.actions("create")
        elif self.selected_item == 2:
            sys.exit()

    def __init__(self, context):
        super().__init__(context)
        self.context = context
        self.name = "main"
        self.items = ["1 : search files", "2 : create files", "3 : exit"]
        self.ui.items = self.items
        self.ui.draw_items(context.win, self.items, 0, " main menu ")


class Search(BaseMenu):


    def reinitialize_menu(self):
        self.ui.draw_items(self.context.win, self.items, 0, "search menu") 

    def query_result_methods_combined(self, query_result):
        self.ui.show_query_result()
        self.ui.query_result = query_result
        self.ui.draw_query_objects()
        self.ui.query_result_behaviour()

    def ask_user(self, criteria, msg):
        user_input = self.ui.input_textbox(self.context, msg)
        if user_input == ".exit":
            return None
        query = {}
        query[criteria] = {"$regex": user_input, "$options": "i"}
        try:
            query_result = list(self.dbclient.search(query))
            if not query_result:
                query_result = "no results matching the criteria"
            self.query_result_methods_combined(query_result)
        except Exception as e:
            self.ui.message(f"search error: {str(e)}")

    def choose(self):
        if self.selected_item == 0:
            self.ask_user("name", "please enter name")
        elif self.selected_item == 1:
            self.ask_user("jahr", "please enter the year")
        elif self.selected_item == 2:
            self.ask_user("art", "please enter the genre")
        elif self.selected_item == 3:
            user_input = self.ui.input_textbox(self.context, "enter your filters in a dictionary format. example: name:inception")
            if user_input == ".exit":
                return
            try:
                if ":" in user_input:
                    parts = user_input.split(":", 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        query = {key: {"$regex": value, "$options": "i"}}
                    else:
                        raise ValueError("invalid format")
                else:
                    query = eval(user_input)
                    if not isinstance(query, dict):
                        raise ValueError("must be a dictionary")
                        
                query_result = list(self.dbclient.search(query))
                if not query_result:
                    query_result = "no results matching the criteria"
                self.query_result_methods_combined(query_result)
            except Exception as e:
                self.ui.message(f"invalid syntax: {str(e)}")
        elif self.selected_item == 4:
            self.actions("main")

    def __init__(self, context):
        super().__init__(context)
        self.context = context
        self.name = "search"
        self.items = ["1 : search by name", "2 : search by year", "3 : search by genre", "4 : custom criteria", "5 : back"]
        self.ui.items = self.items
        self.ui.draw_items(self.context.win, self.items, 0, "search menu")
        self.actions = context.actions

        self.dbclient = context.dbclient

class Create(BaseMenu):
    def ask_user(self, msg):
        user_input = self.ui.input_textbox(self.context, msg)
        query = {}
        return user_input
    def enter_values(self):
        user_vals = self.input_attrs_loop()
        if user_vals is None:
            return False
        if user_vals:
            new_doc = {}
            for i, attr in enumerate(self.attr_list):
                if user_vals[i] and user_vals[i] != "":
                    new_doc[attr] = user_vals[i]
            if new_doc:
                try:
                    self.dbclient.create(new_doc)
                    self.ui.message("document created!")
                except Exception as e:
                    self.ui.message(f"error creating document: {str(e)}")
            else:
                self.ui.message("no data entered, document not created")
        else:
            self.ui.message("no data entered, document not created")
        return True
    def __init__(self, context):
        super().__init__(context)
        self.context = context
        self.name = "create"
        self.items = ["creating new document..."]
        self.ui.items = self.items
        self.ui.draw_items(context.win, self.items, 0, "create menu")
        self.actions = context.actions


class Update_Delete(BaseMenu):
    def ask_user(self, msg):
        attrs_msg = f"available attributes: {', '.join(self.attr_list)}"
        self.ui.message(attrs_msg)
        
        user_input = self.ui.input_textbox(self.context, msg)
        if user_input == ".exit":
            return None

        if user_input in self.attr_list:
            return user_input
        else:
            self.ui.message("invalid attr name, try again")
            return None
    
    def choose(self):
        if self.selected_item == 0:
            attr=self.ask_user("please enter the attr to update")
            if attr:
                new_value = self.ui.input_textbox(self.context, f"new value for {attr}: ")
                if new_value and new_value != ".exit":
                    try:
                        from bson import ObjectId
                        self.dbclient.update_one({"_id": ObjectId(self.objectID)}, {"$set": {attr: new_value}})
                        self.ui.message("updated!")
                    except Exception as e:
                        self.ui.message(f"error updating: {str(e)}")
            return  # Return to restart the menu
           
        elif self.selected_item == 1:
            user_vals = self.input_attrs_loop()
            if user_vals is None:
                return
            if user_vals:
                update_doc = {}
                for i, attr in enumerate(self.attr_list):
                    if user_vals[i] and user_vals[i] != "":
                        update_doc[attr] = user_vals[i]
                if update_doc:
                    try:
                        from bson import ObjectId
                        self.dbclient.update_one({"_id": ObjectId(self.objectID)}, {"$set": update_doc})
                        self.ui.message("updated all!")
                    except Exception as e:
                        self.ui.message(f"error updating: {str(e)}")
                else:
                    self.ui.message("no data entered")
            return  # Return to restart the menu
        elif self.selected_item == 2:
            attr=self.ask_user("please enter attr to delete")
            if attr:
                try:
                    from bson import ObjectId
                    self.dbclient.update_one({"_id": ObjectId(self.objectID)}, {"$unset": {attr: ""}})
                    self.ui.message("deleted attr!")
                except Exception as e:
                    self.ui.message(f"error deleting attr: {str(e)}")
            return  # Return to restart the menu
        elif self.selected_item == 3:
            confirm = self.ui.input_textbox(self.context, "type DELETE to confirm: ")
            if confirm == "DELETE":
                try:
                    from bson import ObjectId
                    self.dbclient.delete_one({"_id": ObjectId(self.objectID)})
                    self.ui.message("object deleted!")
                    self.actions("search")
                    return
                except Exception as e:
                    self.ui.message(f"error deleting object: {str(e)}")
        elif self.selected_item == 4:
            self.actions("search")
            return
            
    def restart_menu(self):
        self.ui.draw_items(self.context.win, self.items, 0, "update/delete menu")

    def __init__(self, context, objectID):
        super().__init__(context)
        self.context = context
        self.name = "update_delete"
        self.items = ["1 : update one attr", "2 : update all attrs", "3 : delete one attr", "4 : delete object", "5 : back"]
        self.ui.items = self.items
        self.ui.draw_items(context.win, self.items, 0, "update/delete menu")
        self.actions = context.actions
        
        self.objectID = objectID

 



