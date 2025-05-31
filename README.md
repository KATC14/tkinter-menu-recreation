# tkinter-menu-recreation

wasn't happy with the commands/binds that tkinter.menu provided so I created my own menu using tkinter.Toplevel for drop down menus, tkinter.Frame for the base and parent of every Toplevel and tkitner.Label on the Frame

add_command and add_cascade return the label it creates incase more binding is wanted

## Drop down menu
root has bind `<FocusOut>` to remove context menu
<!--# example
```python
def test(event):
    print('state ', event.state)
    print('type  ', event.type)
    print('widget', event.widget)
    print('widget', event.widget.cget('text'))

root = tkinter.Tk()

dropdown = Dropdown(root)
dropdown.add_command(label='command', command=test)

newdrop = Dropdown(dropdown)
newdrop.add_command(label='command one', command=test)
newdrop.add_command(label='command two', command=test)
dropdown.add_cascade(label="cascade", menu=newdrop)

root.mainloop()
```

## menu recreation-->

root has bind `<Configure>` to remove cascades when moving window
it has to .grid on root to column and row 0

all the binds are `<Enter>`, `<Leave>` and `<Button-1>`

# example
```python
def test(event):
    print('state ', event.state)
    print('type  ', event.type)
    print('widget', event.widget)
    print('widget', event.widget.cget('text'))

root = tkinter.Tk()

menu = MainMenu(root)
menu.add_command(label='command', command=test)

newmenu = MainMenu(menu)
newmenu.add_command(label='command one', command=test)
newmenu.add_command(label='command two', command=test)
menu.add_cascade(label="cascade", menu=newmenu)

root.mainloop()
```
