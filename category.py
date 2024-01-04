from tkinter import* #for GUI application
from PIL import Image,ImageTk #to use jpg or gif images
from tkinter import ttk, messagebox
import sqlite3

# Define a class named "employeeClass" for the Inventory Management System
class categoryClass:
    def __init__(self,root):
        # Set up the main window properties
        self.root=root
        self.root.geometry("1310x625+220+130")#provide screen size of dashboard: ht,wt,x-axis,y-axis
        self.root.title("Inventory Management System | Developed by Nima Tsering Tamang") # Set window title
        self.root.config(bg="white")
        self.root.focus_force()#to highlight employee window 

        #Variables
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #title
        title = Label(self.root, text="Manage Product Category", font=("goudy old style",20, "bold"), bg="#0f4d7d", fg="white").place(x=100, y=10, width=1100, height=30)

        #Row1
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style",15,"bold"), bg="white").place(x=100, y=60)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=315, y=60, width=250)

        #button
        btn_add = Button(self.root, text="Add", command=self.add, font=("goudy old style",15), bg="#4caf50", fg="white", cursor="hand2").place(x=610, y=59, width=100, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style",15), bg="red", fg="white", cursor="hand2").place(x=730, y=59, width=100, height=28)
        
        
        #====TreeView====
        # Create a frame for the category details
        cat_Frame=Frame(self.root, bd=3, relief=RIDGE)
        cat_Frame.place(x=0, y=400, relwidth=1, height=224)

        # Create vertical and horizontal scrollbars for the Treeview
        scrolly=Scrollbar(cat_Frame, orient=VERTICAL)        
        scrollx=Scrollbar(cat_Frame, orient=HORIZONTAL)

        # Create a Treeview widget for displaying employee details
        self.categoryTable=ttk.Treeview(cat_Frame, columns=("cid","name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)#place bottom scrollbar
        scrolly.pack(side=RIGHT, fill=Y)#place side scrollbar to right
        scrollx.config(command=self.categoryTable.xview)#make scrollx work
        scrolly.config(command=self.categoryTable.yview)#make scrolly work 

        # Set column headings for the Treeview
        self.categoryTable.heading("cid", text="Category ID")
        self.categoryTable.heading("name", text="Name")
        
        
        # Configure the Treeview to show only headings
        self.categoryTable["show"]="headings"

        # Set column widths for the Treeview
        self.categoryTable.column("cid", width=50)
        self.categoryTable.column("name", width=810)
        
        
        # Pack the Treeview to fill the available space and expand
        self.categoryTable.pack(fill=BOTH, expand=1)
        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)#setting event to get get_data function after clicking data in datbase 
        

        #Images
        self.im1=Image.open("Images/cat.jpg")
        self.im1=self.im1.resize((500,270))
        self.im1=ImageTk.PhotoImage(self.im1)
        
        self.lbl_im1=Label(self.root, image=self.im1, bd=2, relief=RAISED)
        self.lbl_im1.place(x=100, y=120)

        self.im2=Image.open("Images/cat1.jpg")
        self.im2=self.im2.resize((500,270))
        self.im2=ImageTk.PhotoImage(self.im2)
        
        self.lbl_im2=Label(self.root, image=self.im2, bd=2, relief=RAISED)
        self.lbl_im2.place(x=695, y=120)

        self.show()

    #==================================================================================================================
    #Adding data into database
    def add(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            if self.var_name.get()=="" :
                messagebox.showerror("Error", "Category name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                       messagebox.showerror("Error","Category already present, please try different.", parent=self.root)    
                else:
                    cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully.", parent=self.root)
                    self.show()           
                                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 



    #For Showing Detail
    def show(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
                cur.execute("SELECT * FROM category")
                rows=cur.fetchall()
                self.categoryTable.delete(*self.categoryTable.get_children())
                for row in rows:
                    self.categoryTable.insert('', END, values=row)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 


    #to display database data into entry box
    def get_data(self, ev):
        f=self.categoryTable.focus()
        content= (self.categoryTable.item(f))
        row=content['values']
        
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])  


    #for deleting data in database
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error", "Please select Category Name from list", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                       messagebox.showerror("Error","Error, please try again", parent=self.root)    
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()                     
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
                     
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


# This block of code will only run if the script is executed directly, not when it's imported as a module.
if __name__=="__main__":
    root=Tk()# Create the main Tkinter window
    obj=categoryClass (root)# Create an instance of the employeeClass class
    root.mainloop()# Start the Tkinter event loop, make window open after execution
