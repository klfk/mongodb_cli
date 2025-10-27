# mongodb cli oop - uml diagram

## class diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 app.py                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐         ┌─────────────────────────────────────────┐ │
│  │      context        │         │                app                      │ │
│  ├─────────────────────┤         ├─────────────────────────────────────────┤ │
│  │ - stdscr           │         │ - stdscr                               │ │
│  │ - win              │         │ - ui                                   │ │
│  │ - ui               │         │ - win                                  │ │
│  │ - actions          │         │ - context                              │ │
│  │ - dbclient         │         │ - current_menu                         │ │
│  │ - app              │         ├─────────────────────────────────────────┤ │
│  └─────────────────────┘         │ + actions(menu, objectid=none)        │ │
│                                  │ + run()                                │ │
│                                  │ + __init__(stdscr)                     │ │
│                                  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                ui.py                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                              ui                                         │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ - stdscr                                                               │ │
│  │ - selected_item                                                        │ │
│  │ - items[]                                                              │ │
│  │ - title                                                                │ │
│  │ - query_result                                                         │ │
│  │ - query_data[]                                                         │ │
│  │ - query_pad                                                            │ │
│  │ - black_green                                                          │ │
│  │ - reversed                                                             │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ + actions_receiver(win, action, key)                                   │ │
│  │ + key_sender(win)                                                      │ │
│  │ + draw_items(win, items, selected_item, title)                        │ │
│  │ + make_ui(stdscr, itemstotal)                                          │ │
│  │ + input_textbox(context, msg)                                          │ │
│  │ + query_result_behaviour()                                             │ │
│  │ + draw_query_objects()                                                 │ │
│  │ + format_document(doc)                                                 │ │
│  │ + show_query_result()                                                  │ │
│  │ + show_chosen_object()                                                 │ │
│  │ + message(text)                                                        │ │
│  │ + init_colors()                                                        │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              dbclient.py                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                            dbclient                                     │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ - myclient                                                             │ │
│  │ - mydb                                                                 │ │
│  │ - col                                                                  │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ + search(criteria)                                                     │ │
│  │ + update_one(filter_dict, update_dict)                                 │ │
│  │ + delete_one(filter_dict)                                              │ │
│  │ + create(data)                                                         │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                               menus.py                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           basemenu                                      │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ - context                                                              │ │
│  │ - win                                                                  │ │
│  │ - ui                                                                   │ │
│  │ - stdscr                                                               │ │
│  │ - actions                                                              │ │
│  │ - dbclient                                                             │ │
│  │ - attr_list[]                                                          │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ + move_by_int()                                                        │ │
│  │ + key_receiver(current_menu)                                           │ │
│  │ + input_attrs_loop()                                                   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                      ▲                                      │
│                                      │                                      │
│                     ┌────────────────┼────────────────┐                    │
│                     │                │                │                    │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │       main          │  │       search        │  │       create        │ │
│  ├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤ │
│  │ - name              │  │ - name              │  │ - name              │ │
│  │ - items[]           │  │ - items[]           │  │ - items[]           │ │
│  ├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤ │
│  │ + choose()          │  │ + reinitialize_menu()│  │ + enter_values()    │ │
│  └─────────────────────┘  │ + query_result_     │  └─────────────────────┘ │
│                           │   methods_combined() │                        │
│                           │ + ask_user()        │                        │
│                           │ + choose()          │                        │
│                           └─────────────────────┘                        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                         update_delete                                   │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ - name                                                                 │ │
│  │ - items[]                                                              │ │
│  │ - objectid                                                             │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │ + ask_user(msg)                                                        │ │
│  │ + choose()                                                             │ │
│  │ + restart_menu()                                                       │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

## relationships

app uses context                    : composition
app has ui                         : composition  
app has dbclient                   : composition
app has current_menu               : association

context contains all dependencies  : aggregation

basemenu is abstract parent        : inheritance
main extends basemenu              : inheritance  
search extends basemenu            : inheritance
create extends basemenu            : inheritance
update_delete extends basemenu     : inheritance

all menus use ui                   : dependency
all menus use dbclient             : dependency

## sequence diagram - create document flow

```
user -> app: select "create files"
app -> create: new create(context)
app -> create: key_receiver()
create -> create: enter_values()
create -> ui: input_textbox() (multiple times)
ui -> user: show input prompts
user -> ui: enter data
create -> dbclient: create(new_doc)
dbclient -> mongodb: insert_one()
create -> ui: message("document created!")
create -> app: actions("main")
app -> main: new main(context)
```

## sequence diagram - search and update flow

```
user -> app: select "search files"
app -> search: new search(context)
app -> search: key_receiver()
search -> ui: input_textbox()
user -> search: enter search criteria
search -> dbclient: search(query)
dbclient -> mongodb: find()
search -> ui: show_query_result()
ui -> user: display results
user -> ui: select document
ui -> app: actions("update_delete", objectid)
app -> update_delete: new update_delete(context, objectid)
update_delete -> ui: show update/delete menu
user -> update_delete: select operation
update_delete -> dbclient: update_one() or delete_one()
dbclient -> mongodb: execute operation
```

## data flow

```
mongodb database
    ↕
dbclient (pymongo wrapper)
    ↕  
menus (business logic)
    ↕
ui (presentation layer)
    ↕
user (terminal interface)
```

## file structure

```
mongodb_cli_oop/
├── app.py           | main application entry point
├── menus.py         | menu classes and navigation logic  
├── ui.py            | user interface and display logic
├── dbclient.py      | database operations wrapper
└── readme.md        | project documentation
```