import tkinter
from tkinter.ttk import *


class MainMenu(tkinter.Frame):
	def __init__(self, master, *args, **kwargs):

		if not isinstance(master, tkinter.Tk):
			master = tkinter.Toplevel(master, *args, **kwargs)
			master.overrideredirect(True)
			master.withdraw()

		super().__init__(master, *args, **kwargs)

		self.parent = master
		self.parent.grid_rowconfigure(0, weight=100)
		self.parent.grid_columnconfigure(0, weight=100)
		self.cascade_opened = False
		self.column = -1
		self.row    = -1
		self.config(bg='white')
		if not isinstance(self.parent, tkinter.Tk):
			self.config(bg='#f0f0f0', padx=18)
		self.grid(sticky='NEW', column=self.column+1, row=self.row+1)

	def _another_hover(self, event):
		# 8 is Leave
		# 7 is Enter
		evetype = int(event.type)
		widget = event.widget
		toplevel = None

		# Enter
		if   evetype == 7:
			self._remove_siblings(widget.master)
			widget.config(bg='#e5f3ff')
			widget.focus()
		# Leave
		elif evetype == 8:
			widget.config(bg='white')

		# Enter
		if evetype == 7 and self.cascade_opened:
			a = self.winfo_children()
			for i in a:
				if i.master == widget.master:
					for x in i.master.winfo_children():
						if isinstance(x, tkinter.Toplevel):
							toplevel = x
						elif isinstance(x, tkinter.Label) and toplevel:
							if widget.cget('text') == x.cget('text'):
								toplevel.wm_deiconify()
								toplevel.geometry(f"+{event.widget.winfo_rootx()}+{event.widget.winfo_rooty()+21}")
								break
					break
		if self.cascade_opened:
			widget = event.widget
			for i in self.winfo_children():
				if isinstance(i, tkinter.Label):
					if i == widget:
						i.config(bg='#cce8ff', relief='groove')
					else:
						i.config(bg='white', relief='flat')

	def _cascade_hover(self, event, menu):
		evetype = int(event.type)
		widget = event.widget
		menmas = menu.master

		# Enter
		if   evetype == 7:
			self._remove_siblings(menmas.master)
			menmas.wm_deiconify()
			menmas.geometry(f"+{event.widget.winfo_rootx()+widget.winfo_width()}+{event.widget.winfo_rooty()}")
			widget.config(bg='#0078d7')#0078d7
		# Leave
		elif evetype == 8:
			widget.config(bg='#f0f0f0')#f0f0f0

	def _command_hover(self, event):
		# 8 is Leave
		# 7 is Enter
		evetype = int(event.type)
		widget = event.widget
		# Leave
		if evetype == 8:
			if isinstance(self.parent, tkinter.Toplevel):
				widget.config(bg='#f0f0f0')#f0f0f0
			else:
				widget.config(bg='white')#white
		# Enter
		elif evetype == 7:
			self._remove_siblings(widget.master)

			for i in widget.master.winfo_children():
				if isinstance(i, tkinter.Label) and not isinstance(i.master.master, tkinter.Toplevel):
					i.config(bg='white', relief='flat')

			if isinstance(self.parent, tkinter.Toplevel):
				widget.config(bg='#0078d7')#0078d7
			else:
				widget.config(bg='#cce8ff')#cce8ff

	def _get_children(self, widget):
		alist = []
		a = [widget, ]
		while True:
			if not a:
				break
			a = a[0].winfo_children()
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
		b = None
		while True:
			b = a
			a = a.master
			if not a.master:
				if not alist:
					return [b, ]
				else:
					return alist
			elif not a:
				break
			else:
				alist.append(a)
		return alist

	def _remove_siblings(self, siblings):
		for i in siblings.winfo_children():
			if isinstance(i, tkinter.Toplevel):
				i.withdraw()
				for x in self._get_children(i):
					x.withdraw()

	def _do_command(self, event, command):
		widget = event.widget
		widmas = widget.master.master
		topmost = self._get_masters(self)
		topmost[-1].cascade_opened = False

		for i in topmost[-1].winfo_children():
			if not isinstance(i, tkinter.Toplevel):
				i.config(bg='white', relief='flat')
	
		# removes all open toplevels
		if isinstance(widmas, tkinter.Toplevel):
			widmas.withdraw()
			for i in topmost:
				if isinstance(i, tkinter.Toplevel):
					i.withdraw()

		command(event)

	def _open_menu(self, event, menu):
		widget = event.widget
		menmas = menu.master

		if isinstance(self.parent, tkinter.Toplevel):
			self.cascade_opened = True
			menmas.wm_deiconify()
			menmas.geometry(f"+{event.widget.winfo_rootx()+widget.winfo_width()}+{event.widget.winfo_rooty()}")
		else:
			if menmas.winfo_viewable():
				self.cascade_opened = False
				menmas.withdraw()
				widget.config(bg='white', relief='flat')
			else:
				self.cascade_opened = True
				menmas.wm_deiconify()
				menmas.geometry(f"+{widget.winfo_rootx()}+{widget.winfo_rooty()+21}")
				widget.config(bg='#cce8ff', relief='groove')

	def _menu_lose_focus(self, event):
		self.cascade_opened = False
		self._remove_siblings(event.widget)
		for i in self.winfo_children():
			if not isinstance(i, tkinter.Toplevel):
				i.config(bg='white', relief='flat')

	def add_cascade(self, label, menu, *args, **kwargs):
		label = self.add_command(label=label, *args, **kwargs)
		label.bind("<Enter>", lambda e: self._another_hover(e))
		label.bind("<Leave>", lambda e: self._another_hover(e))
		self.bind("<FocusOut>", self._menu_lose_focus)

		if isinstance(label.master.master, tkinter.Toplevel):
			label.bind("<Enter>", lambda e: self._cascade_hover(e, menu))
			label.bind("<Leave>", lambda e: self._cascade_hover(e, menu))
		else:
			label.bind("<Button-1>", lambda e: self._open_menu(e, menu))
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

class _Application():
	def __init__(self):
		root = tkinter.Tk()
		root.geometry('200x50')
		tkinter.Label(root, text='label on root').grid(sticky='S', column=0, row=1)

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
		print('widget', event.widget.cget('text'))
		event.widget.config(text='text changed!')
		print('new text', event.widget.cget('text'))
		print()

if __name__ == '__main__':
	_Application()
