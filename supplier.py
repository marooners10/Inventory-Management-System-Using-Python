from tkinter import* #for GUI application
from PIL import Image,ImageTk #to use jpg or gif images
from tkinter import ttk, messagebox
import sqlite3

# Define a class named "employeeClass" for the Inventory Management System
class supplierClass:
    def __init__(self,root):
        # Set up the main window properties
        self.root=root
        self.root.geometry("1310x625+220+130")#provide screen size of dashboard: ht,wt,x-axis,y-axis
        self.root.title("Inventory Management System | Developed by Nima Tsering Tamang") # Set window title
        self.root.config(bg="white")
        self.root.focus_force()#to highlight employee window 
        
        #====================================
        #All Variable
        self.var_searchby=StringVar()#id
        self.var_searchtxt=StringVar()#id
        
        self.var_sup_invoice=StringVar()#id
        self.var_contact=StringVar()#contact
        self.var_name=StringVar()#name
                
    
        #options inside search frame
        lbl_search=Label(self.root,text="Search By Invoice No.",bg="white", font=("goudy old style",15))
        lbl_search.place(x=600,y=60)

        #search box
        txt_search=Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style",15), bg="lightyellow").place(x=800, y=60)

        #search btn
        btn_search=Button(self.root, text="Search", command=self.search, font=("goudy old style",15), bg="#4caf50", fg="white", cursor="hand2").place(x=1030, y=59, width=150, height=28)

        #title
        title = Label(self.root, text="Supplier Details", font=("goudy old style",20, "bold"), bg="#0f4d7d", fg="white").place(x=100, y=10, width=1100, height=30)

        #Contents
        #Row1
        lbl_supplier_invoice = Label(self.root, text="Invoice No.", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=60)
        
        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=220, y=60, width=200)
            
        #Row2
        lbl_name = Label(self.root, text="Name", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=110)
        
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=220, y=110, width=200)
        
        #Row3
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=160)
        
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=220, y=160, width=200)
        

        #Row4
        lbl_desc = Label(self.root, text="Description", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=210)
        
        self.txt_desc = Text(self.root, font=("goudy old style",15), bg="lightyellow", fg="black")
        self.txt_desc.place(x=220, y=210, width=500, height=100)
        

        #buttons
        btn_add=Button(self.root, text="Save", command=self.add, font=("goudy old style",15), bg="#2196f3", fg="white", cursor="hand2").place(x=220, y=350, width=110, height=28)
        btn_update=Button(self.root, text="Update", command=self.update, font=("goudy old style",15), bg="#4caf50", fg="white", cursor="hand2").place(x=340, y=350, width=110, height=28)
        btn_delete=Button(self.root, text="Delete", command= self.delete, font=("goudy old style",15), bg="#f44336", fg="white", cursor="hand2").place(x=460, y=350, width=110, height=28)
        btn_clear=Button(self.root, text="Clear", command=self.clear, font=("goudy old style",15), bg="#607d8b", fg="white", cursor="hand2").place(x=580, y=350, width=110, height=28)

        #====TreeView====
        # Create a frame for the employee details
        emp_Frame=Frame(self.root, bd=3, relief=RIDGE)
        emp_Frame.place(x=0, y=400, relwidth=1, height=224)

        # Create vertical and horizontal scrollbars for the Treeview
        scrolly=Scrollbar(emp_Frame, orient=VERTICAL)        
        scrollx=Scrollbar(emp_Frame, orient=HORIZONTAL)

        # Create a Treeview widget for displaying employee details
        self.supplierTable=ttk.Treeview(emp_Frame, columns=("invoice","name","contact","desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)#place bottom scrollbar
        scrolly.pack(side=RIGHT, fill=Y)#place side scrollbar to right
        scrollx.config(command=self.supplierTable.xview)#make scrollx work
        scrolly.config(command=self.supplierTable.yview)#make scrolly work 

        # Set column headings for the Treeview
        self.supplierTable.heading("invoice", text="Invoice No.")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        
        # Configure the Treeview to show only headings
        self.supplierTable["show"]="headings"

        # Set column widths for the Treeview
        self.supplierTable.column("invoice", width=80)
        self.supplierTable.column("name", width=110)
        self.supplierTable.column("contact", width=110)
        self.supplierTable.column("desc", width=90)
        
        
        # Pack the Treeview to fill the available space and expand
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)#setting event to get get_data function after releasing button 
        
        self.show()
#===========================================================================================================

    #Adding data into database
    def add(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            if self.var_sup_invoice.get()=="" :
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                       messagebox.showerror("Error","This Invoice No. is already assigned, please try different.", parent=self.root)    
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                                self.var_sup_invoice.get(),
                                                self.var_name.get(),             
                                                self.var_contact.get(),
                                                self.txt_desc.get('1.0',END),                                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully.", parent=self.root)
                    self.show()           
                                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 
            

    #For Showing Detail
    def show(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
                cur.execute("SELECT * FROM supplier")
                rows=cur.fetchall()
                self.supplierTable.delete(*self.supplierTable.get_children())
                for row in rows:
                    self.supplierTable.insert('', END, values=row)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 

    
    #to display database data into entry box
    def get_data(self, ev):
        f=self.supplierTable.focus()
        content= (self.supplierTable.item(f))
        row=content['values']
        
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])             
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])
        
        
    
    #Update data into database
    def update(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            if self.var_sup_invoice.get()=="": 
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                       messagebox.showerror("Error","Invalid Invoice No..", parent=self.root)    
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                                                self.var_name.get(),             
                                                self.var_contact.get(),
                                                self.txt_desc.get('1.0',END),
                                                self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully.", parent=self.root)
                    self.show()           
                                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 
            
            
    #for deleting data in database
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                       messagebox.showerror("Error","Invalid Invoice No..", parent=self.root)    
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()                     
                        messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                        self.clear()
                     
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
          
          
    #For clearing data
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")             
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()
          

    #for searching data in database
    def search(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. Must Be Required.", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row !=None:    
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found.", parent=self.root)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 

        

           
# This block of code will only run if the script is executed directly, not when it's imported as a module.
if __name__=="__main__":
    root=Tk()# Create the main Tkinter window
    obj=supplierClass(root)# Create an instance of the employeeClass class
    root.mainloop()# Start the Tkinter event loop, make window open after execution
