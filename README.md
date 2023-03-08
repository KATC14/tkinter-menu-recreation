# tkinter-menu-recreation

wasnt happy with the commands/binds that tkinter.menu provided so I created my own menu using tkinter.Toplevel for drop down menus, tkinter.Frame for the base and parent of every Toplevel and tkitner.Label on the Frame

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
