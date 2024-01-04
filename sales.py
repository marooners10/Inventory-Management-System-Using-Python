from tkinter import* #for GUI application
from PIL import Image,ImageTk #to use jpg or gif images
from tkinter import ttk, messagebox 
import sqlite3 #for database
import os 

# Define a class named "employeeClass" for the Inventory Management System
class salesClass:
    def __init__(self,root):
        # Set up the main window properties
        self.root=root
        self.root.geometry("1310x625+220+130")#provide screen size of dashboard: ht,wt,x-axis,y-axis
        self.root.title("Inventory Management System | Developed by Nima Tsering Tamang") # Set window title
        self.root.config(bg="white")
        self.root.focus_force()#to highlight employee window 

#======================================================================
        #All Variables
        self.var_invoice=StringVar()
        self.bill_list=[]

        #title
        title = Label(self.root, text="View Customer Bills", font=("goudy old style",20, "bold"), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X, padx=10, pady=20)
        
        #Row1 Invoice number
        lbl_invoice=Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white").place(x=50, y=100)
        text_invoice=Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="lightyellow").place(x=160, y=100, width=180, height=28)
        
        #Row1 btn
        btn_search=Button(self.root, command=self.search, text="Search", font=("times new roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2").place(x=360, y=100, width=120, height=28)
        btn_clear=Button(self.root, command=self.clear, text="Clear", font=("times new roman", 15, "bold"), bg="lightgrey", cursor="hand2").place(x=500, y=100, width=120, height=28)
        #===============Bills List====================
        #frame for bill list
        sales_Frame=Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=170, width=250, height=410)

        #List view with scroll property
        scrolly=Scrollbar(sales_Frame, orient=VERTICAL)
        scrollx=Scrollbar(sales_Frame, orient=HORIZONTAL)
        self.sales_List=Listbox(sales_Frame, font=("goudy old style",15), bg="white", yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.sales_List.yview)
        scrollx.config(command=self.sales_List.xview)
        self.sales_List.pack(fill=BOTH, expand=1)

        #==================Bill Area=====================
        #frame for bill area
        bill_Frame=Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=360, y=170, width=500, height=410)

        #title
        title1 = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style",20), bg="#184a45", fg="white").pack(side=TOP, fill=X)

        #bill area with scroll property
        scrolly1=Scrollbar(bill_Frame, orient=VERTICAL)
        scrollx1=Scrollbar(bill_Frame, orient=HORIZONTAL)
        self.bill_area=Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly1.set, xscrollcommand=scrollx1.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.bill_area.yview)
        scrollx.config(command=self.bill_area.xview)
        self.bill_area.pack(fill=BOTH, expand=1)
        self.sales_List.bind("<ButtonRelease-1>", self.get_data)#bind sales_List with get_data function so that whenever sales_list's file is clicked it's detail get displayed and it's an event


        #Images
        self.bill_photo=Image.open("Images/cat1.jpg")
        self.bill_photo=self.bill_photo.resize((400,250))
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)
        
        lbl_image=Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=900, y=170)
        
        self.show()
        
    #==================================================================================
    def show(self):#to show the files name in sales_list
        del self.bill_list[:]
        self.sales_List.delete(0,END)
        #print(os.listdir('../IMS)) => shows files in IMS folder
        for i in os.listdir('bill'): 
            #print(i.split('.'), i.split('.')[-1]) => split the name and display extension only
            if i.split('.')[-1]=='txt':
                self.sales_List.insert(END,i) #takes complete file name
                self.bill_list.append(i.split('.')[0])#append all file names in bill_list 
                

    def get_data(self, ev):
        index_=self.sales_List.curselection()#to display the index of list whenever mouse in on sales_list 
        file_name=self.sales_List.get(index_)#getting data from file instead of index
        self.bill_area.delete('1.0',END)#delete prev data before displaying new for txt file
        fp=open(f'bill/{file_name}','r')#open file in read only mode
        for i in fp:
            self.bill_area.insert(END,i)#takes complete data from given file 
        fp.close()   


    def search(self):
        if self.var_invoice.get()=='':
            messagebox.showerror("Error","Invoice No. must be required.", parent=self.root)            
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')#open file in read only mode
                self.bill_area.delete('1.0',END)#delete prev data before displaying new for txt file
                for i in fp:
                    self.bill_area.insert(END,i)#takes complete data from given file 
                fp.close() 
            else:
                messagebox.showerror("Error","Invalid Invoice No.", parent=self.root)
         
    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)        

# This block of code will only run if the script is executed directly, not when it's imported as a module.
if __name__=="__main__":
    root=Tk()# Create the main Tkinter window
    obj=salesClass(root)# Create an instance of the employeeClass class
    root.mainloop()# Start the Tkinter event loop, make window open after execution
