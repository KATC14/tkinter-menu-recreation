import tkinter
from tkinter.ttk import *


class MainMenu(tkinter.Frame):
	def __init__(self, master, isdropdown=False, *args, **kwargs):

		if isinstance(master, tkinter.Frame) or isdropdown:
			label = tkinter.Label(master, bg='white')
			master = tkinter.Toplevel(label, bg='#f0f0f0', *args, **kwargs)
			master.overrideredirect(True)
			master.withdraw()

		super().__init__(master, *args, **kwargs)

		self.parent = master
		self.parent.grid_rowconfigure(0, weight=1)
		self.parent.grid_columnconfigure(0, weight=1)
		self.cascade_opened = False
		self.column = -1
		self.row    = -1
		self.config(bg='white')
		if not isinstance(self.parent, tkinter.Tk):
			self.config(bg='#f0f0f0')
		self.grid(sticky='NEW', column=self.column+1, row=self.row+1)

	def _another_hover(self, event):
		# 8 is Leave
		# 7 is Enter
		evetype = int(event.type)
		widget = event.widget
		toplevel = widget.winfo_children()[0]

		# Enter
		if   evetype == 7:
			self._remove_siblings(widget.master)
			widget.config(bg='#e5f3ff')#e5f3ff
			widget.focus()
		# Leave
		elif evetype == 8:
			widget.config(bg='white', relief='flat')

		if evetype == 7 and self.cascade_opened:
			widget.config(bg='#cce8ff', relief='groove')
			toplevel.wm_deiconify()
			toplevel.geometry(f"+{event.widget.winfo_rootx()}+{event.widget.winfo_rooty()+21}")

	def _cascade_hover(self, event):
		evetype = int(event.type)
		widget = event.widget
		toplevel = widget.winfo_children()[0]

		# Enter
		if   evetype == 7:
			self._remove_siblings(widget.master)
			toplevel.wm_deiconify()
			toplevel.geometry(f"+{event.widget.winfo_rootx()+widget.winfo_width()}+{event.widget.winfo_rooty()}")
			widget.config(bg='#0078d7')#0078d7
		# Leave
		elif evetype == 8:
			widget.config(bg='#f0f0f0')#f0f0f0

	def _command_hover(self, event):
		# 8 is Leave
		# 7 is Enter
		evetype = int(event.type)
		widget = event.widget

		# Enter
		if   evetype == 7:
			self._remove_siblings(widget.master)
			if isinstance(self.parent, tkinter.Toplevel):
				widget.config(bg='#0078d7')#0078d7
			else:
				widget.config(bg='#e5f3ff')#e5f3ff
		# Leave
		elif evetype == 8:
			if isinstance(self.parent, tkinter.Toplevel):
				widget.config(bg='#f0f0f0')#f0f0f0
			else:
				widget.config(bg='white')

	def _get_children(self, widget):
		alist = []
		a = [widget, ]
		while True:
			if not a:
				break
			a = a[-1].winfo_children()
			for i in a:
				if isinstance(i, tkinter.Frame):
					a = [i, ]
				elif isinstance(i, tkinter.Toplevel):
					a = [i, ]
					alist.append(i)
		return alist

	def _get_masters(self, widget):
		alist = []
		a = widget
		while True:
			a = a.master
			if not a: break
			if not isinstance(a, tkinter.Tk):
				alist.append(a)
		return alist

	def _remove_siblings(self, widget):
		for i in widget.winfo_children():
			if isinstance(i, tkinter.Toplevel):
				i.withdraw()
			for x in self._get_children(i):
				x.withdraw()

	def _do_command(self, event, command):
		widget = event.widget
		for i in self._get_masters(widget):
			if isinstance(i, tkinter.Toplevel):
				i.withdraw()

		command(event)

	def _open_menu(self, event):
		widget = event.widget
		toplevel = widget.winfo_children()[0]

		# opens nested cascade
		if isinstance(self.parent, tkinter.Toplevel):
			self.cascade_opened = True
			toplevel.wm_deiconify()
			toplevel.geometry(f"+{event.widget.winfo_rootx()+widget.winfo_width()}+{event.widget.winfo_rooty()}")
		else:
			if toplevel.winfo_viewable():
				self.cascade_opened = False
				toplevel.withdraw()
				widget.config(bg='white', relief='flat')
			else:
				self.cascade_opened = True
				toplevel.wm_deiconify()
				toplevel.geometry(f"+{widget.winfo_rootx()}+{widget.winfo_rooty()+21}")
				widget.config(bg='#cce8ff', relief='groove')

	def _menu_lose_focus(self, event):
		self.cascade_opened = False
		self._remove_siblings(event.widget)

	def add_cascade(self, label, menu, *args, **kwargs):
		text = label
		label = menu.master.master
		label.config(text=text, *args, **kwargs)
		label.bind("<Enter>", lambda e: self._another_hover(e))
		label.bind("<Leave>", lambda e: self._another_hover(e))
		self.bind("<FocusOut>", self._menu_lose_focus)
		self.master.bind("<Configure>", lambda e: self._remove_siblings(self))

		label.bind("<Button-1>", self._open_menu)

		if isinstance(self.parent, tkinter.Toplevel):
			label.bind("<Enter>", self._cascade_hover)
			label.bind("<Leave>", self._cascade_hover)
			label.config(width=10, bg='#f0f0f0')
			self.row += 1
		else:
			self.column += 1

		column = self.column + 1 if self.column < 0 else self.column
		row    = self.row    + 1 if self.row    < 0 else self.row

		label.grid(sticky='nsew', column=column, row=row)
		return label

	def add_command(self, label=None, command=None, *args, **kwargs):
		label = tkinter.Label(self, text=label, bg='white', *args, **kwargs)
		label.bind("<Enter>", self._command_hover)
		label.bind("<Leave>", self._command_hover)

		if isinstance(self.parent, tkinter.Toplevel):
			self.row += 1
			if self.column >= 0:
				self.column -= 1
			self.config(borderwidth=2, relief='groove')
			label.config(bg='#f0f0f0')
		else:
			self.column += 1

		column = self.column + 1 if self.column < 0 else self.column
		row    = self.row    + 1 if self.row    < 0 else self.row

		label.grid(sticky='nsew', column=column, row=row)

		if command:
			label.bind('<Button-1>', lambda e: self._do_command(e, command))
		return label

class Dropdown(MainMenu):
	def __init__(self, master, *args, **kwargs) -> None:
		super().__init__(master, True, *args, **kwargs)
		master.bind('<Button-3>', self._open_menu)
		self.master.bind('<FocusOut>', self._remove_dropdown)
	def _remove_dropdown(self, event):
		widget = event.widget
		widget.withdraw()
		self._remove_siblings(widget)
	def _open_menu(self, event):
		self.master.wm_deiconify()
		self.master.geometry(f"+{event.x_root}+{event.y_root}")
		self.master.focus()

class _Application():
	def __init__(self):
		root = tkinter.Tk()
		root.geometry('200x50')
		tkinter.Label(root, text='label on root').grid(sticky='S', column=0, row=1)

		dropdown = Dropdown(root)
		dropdown.add_command(label='command', command=self.test)

		newdrop = Dropdown(dropdown)
		newdrop.add_command(label='command one', command=self.test)
		newdrop.add_command(label='command two', command=self.test)
		dropdown.add_cascade(label="cascade", menu=newdrop)
	
		menu = MainMenu(root)
		menu.add_command(label='one', command=self.test)

		newmenu = MainMenu(menu)
		newmenu.add_command(label='two', command=self.test)
		newmenu.add_command(label='three', command=self.test)
		menu.add_cascade(label="misc", menu=newmenu)

		nest = MainMenu(newmenu)
		nest.add_command(label='four', command=self.test)
		nest.add_command(label='five', command=self.test)
		newmenu.add_cascade(label="nest", menu=nest)

		nest2 = MainMenu(newmenu)
		nest2.add_command(label='six', command=self.test)
		nest2.add_command(label='seven', command=self.test)
		newmenu.add_cascade(label="nest 2", menu=nest2)

		nest3 = MainMenu(nest2)
		nest3.add_command(label='eight', command=self.test)
		nest3.add_command(label='nine', command=self.test)
		nest2.add_cascade(label="nest nest", menu=nest3)

		nest4 = MainMenu(nest3)
		nest4.add_command(label='ten', command=self.test)
		nest4.add_command(label='eleven', command=self.test)
		nest3.add_cascade(label="nest nest nest", menu=nest4)


		one = MainMenu(menu)
		one.add_command(label='12', command=self.test)
		one.add_command(label='13', command=self.test)
		menu.add_cascade(label="misc 2", menu=one)

		two = MainMenu(one)
		two.add_command(label='14', command=self.test)
		two.add_command(label='15', command=self.test)
		one.add_cascade(label="tsen", menu=two)

		three = MainMenu(one)
		three.add_command(label='16', command=self.test)
		three.add_command(label='17', command=self.test)
		one.add_cascade(label="tsen 2", menu=three)

		four = MainMenu(three)
		four.add_command(label='18', command=self.test)
		four.add_command(label='19', command=self.test)
		three.add_cascade(label="tsen tsen", menu=four)

		five = MainMenu(four)
		five.add_command(label='20', command=self.test)
		five.add_command(label='21', command=self.test)
		four.add_cascade(label="tsen tsen tsen", menu=five)
		four.add_command(label='22', command=self.test)


		a = MainMenu(menu)
		a.add_command(label='23', command=self.test)
		a.add_command(label='24', command=self.test)
		menu.add_cascade(label="misc 3", menu=a)

		b = MainMenu(a)
		b.add_command(label='25', command=self.test)
		b.add_command(label='26', command=self.test)
		a.add_cascade(label="tsen", menu=b)

		c = MainMenu(a)
		c.add_command(label='27', command=self.test)
		c.add_command(label='28', command=self.test)
		a.add_cascade(label="tsen 2", menu=c)

		d = MainMenu(c)
		d.add_command(label='29', command=self.test)
		d.add_command(label='30', command=self.test)
		c.add_cascade(label="tsen tsen", menu=d)

		e = MainMenu(d)
		e.add_command(label='31', command=self.test)
		e.add_command(label='32', command=self.test)
		d.add_cascade(label="tsen tsen tsen", menu=e)
		menu.add_command(label='33', command=self.test)

		root.mainloop()

	def test(self, event):
		#print(event.keycode)
		#print(event.keycode)
		#print(event.keysym_num)
		#print(event.keysym)
		print('state ', event.state)
		print('type  ', event.type)
		print('widget', event.widget)
		print('master', event.widget.master.master.master)
		print('widget', event.widget.cget('text'))
		event.widget.config(text='text changed!')
		print('new text', event.widget.cget('text'))
		print()

if __name__ == '__main__':
	_Application()
