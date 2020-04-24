import tkinter as tk
from tkinter import filedialog, Text
from tkinter.messagebox import showinfo
import os, socket

root = tk.Tk(className='RapiShare 1.0')
root.geometry("500x600")
root.resizable(False,False)
myFiles=[]


def startUp():
	#to run when the app is started
	if selectFile['state'] and sendFile['state'] == tk.NORMAL:
		selectFile['state']=tk.DISABLED
		sendFile['state']=tk.DISABLED
	else:
		selectFile['state']=tk.NORMAL
		sendFile['state']=tk.NORMAL

def chooseFiles():
	#to select file
	for widget in frame.winfo_children():
		widget.destroy()
	filename = filedialog.askopenfilename(initialdir='/', title='Select File',
		filetypes =(("allfiles","*.*"),("allfiles", "*.*")))
	myFiles.append(filename)
	for file in myFiles:
		myFile = tk.Label(frame,text=file,bg='#0779e4')
		myFile.pack()


def sendingFile():
	for file in myFiles:
		tempfile=str(file).split("/",1)[1]
		fFile = str(tempfile).split('.',1)[0]
		showinfo("Successfull ",fFile+" Sent Successfully")

		

def switch():
	#to disable some buttons
	if joinConnection['state'] and createConnection['state']== tk.NORMAL:
		joinConnection['state']=tk.DISABLED
		createConnection['state']=tk.DISABLED
		selectFile['state']=tk.NORMAL
		sendFile['state']=tk.NORMAL

	else:
		joinConnection['state']=tk.NORMAL
		createConnection['state']=tk.NORMAL
def startConn():
	#for starting a connection as a server
	switch()

	s = socket.socket()
	host = socket.gethostname()
	port = 5002
	s.bind((host,port))
	s.listen(1)
	showinfo('Host Name','Host Name:'+host)
	conn,addr = s.accept()
	showinfo('Conected',str(addr)+' Has connected')

	for myf in myFiles:
		file = open(myf,'rb')
		file_data = file.read(1024)
		conn.send(file_data)
		sendingFile()

def join_form():
	root2 = tk.Tk(className="Host and File")
	root2.geometry("500x250")
	root2.resizable(False,False)


	def rec_details():
		s = socket.socket()
		rec_details.theHost=host_input.get()
		port = 5002
		s.connect((rec_details.theHost,port))
		showinfo('Connected', 'Connected...')
		newFilenaming()
		

	frame2 = tk.Frame(root2,bg="#30475e")
	frame2.place(relwidth=1,relheight=1)

	host_id= tk.Label(frame2,text='Host ID:')
	host_id.place(y=50,x=30)

	host_input = tk.Entry(frame2,width=40)
	host_input.place(y=50,x=130)

	submit_form = tk.Button(frame2,text='Submit',width=10, command=rec_details)
	submit_form.place(y=150,x=130)

	cancelEntry = tk.Button(frame2,text='Cancel',width=10,command=root2.quit)
	cancelEntry.place(y=150,x=295)

	root2.mainloop()
def newFilenaming():
	root3 = tk.Tk()
	root3.geometry("500x200")
	root3.resizable(False,False)

	def rec_name():
		s = socket.socket()
		myHost=rec_details.theHost
		port = 5002
		s.connect((myHost,port))
		mynewFile=file_input.get()
		file = open(mynewFile,'wb')
		file_data = s.recv(1024)
		
		file.write(file_data)
		file.close()
		showinfo('Recieved','File Recieved')

	frame3 = tk.Frame(root3,bg="#30475e")
	frame3.place(relwidth=1,relheight=1)

	new_fileName= tk.Label(frame3,text='New File Name:')
	new_fileName.place(y=100,x=30)

	file_input = tk.Entry(frame3,width=40)
	file_input.place(y=100,x=130)

	submit_form1 = tk.Button(frame3,text='Submit',width=10, command=rec_name)
	submit_form1.place(y=150,x=130)

	cancelEntry1 = tk.Button(frame3,text='Cancel',width=10,command=root3.quit)
	cancelEntry1.place(y=150,x=295)

def joinConn():
	#to join a connection as a client
	switch()
	join_form()

createConnection = tk.Button(root,text='Start Connection',bg='#30475e', fg='white',width=20,padx=10, pady=5, command=startConn )
createConnection.pack()

joinConnection = tk.Button(root,text='Join Connection',bg='#30475e', fg='white',width=20,padx=10, pady=5 ,command=joinConn)
joinConnection.pack()


canvas = tk.Canvas(root, height=400, width=400, bg='#30475e')
canvas.pack()

frame = tk.Frame(root,bg='white')
frame.place(relwidth=0.8,relheight=0.6, relx=0.1, rely=0.15)

selectFile = tk.Button(root,text="SelectFile",bg='#30475e', fg='white',width=20,padx=10, pady=5 , command=chooseFiles)
selectFile.pack	()

sendFile = tk.Button(root,text="SendFile",bg='#30475e', fg='white',width=20,padx=10, pady=5, command=sendingFile)
sendFile.pack()

startUp()

logo = tk.Label(root,text='This is a Melusi Gumbi Product')
logo.pack()
root.mainloop()