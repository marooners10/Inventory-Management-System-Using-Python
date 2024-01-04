from tkinter import* #for GUI application
from PIL import Image,ImageTk #to use jpg or gif images
from tkinter import ttk, messagebox
import sqlite3

# Define a class named "productClass" for the Inventory Management System
class productClass:
    def __init__(self,root):
        # Set up the main window properties
        self.root=root
        self.root.geometry("1310x625+220+130")#provide screen size of dashboard: ht,wt,x-axis,y-axis
        self.root.title("Inventory Management System | Developed by Nima Tsering Tamang") # Set window title
        self.root.config(bg="white")
        self.root.focus_force()#to highlight employee window 

        #========================================
        #Variables
        self.var_searchby=StringVar()#for option
        self.var_searchtxt=StringVar()#for text
       
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        self.cat_list=[]#for fetching category data
        self.sup_list=[]#for fetching supplier data
        self.fetch_cat_sup()

        #Frame
        product_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=600)

        #title
        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style",18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)
        
        #Row1
        lbl_category = Label(product_Frame, text="Category", font=("goudy old style",15), bg="white").place(x=30, y=60)

        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat, values=self.cat_list, state='readonly', justify=CENTER, font=("goudy old style",15))
        cmb_cat.place(x=150,y=60, width=200)
        cmb_cat.current(0)#select as permanent option


        #Row2
        lbl_supplier = Label(product_Frame, text="Supplier", font=("goudy old style",15), bg="white").place(x=30, y=120)
        
        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=("goudy old style",15))
        cmb_sup.place(x=150,y=120, width=200)
        cmb_sup.current(0)#select as permanent option
        
        #Row3
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style",15), bg="white").place(x=30, y=180)
        
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=160, y=190, width=200)
        
        #Row4
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style",15), bg="white").place(x=30, y=240)

        txt_price = Entry(self.root, textvariable=self.var_price, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=160, y=250, width=200)
        
        #Row5
        lbl_qty = Label(product_Frame, text="Quantity", font=("goudy old style",15), bg="white").place(x=30, y=300)

        txt_qty = Entry(self.root, textvariable=self.var_qty, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=160, y=310, width=200)
        
        #Row6
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style",15), bg="white").place(x=30, y=360)
        
        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("goudy old style",15))
        cmb_status.place(x=150,y=360, width=200)
        cmb_status.current(0)#select as permanent option


        #buttons
        btn_add=Button(product_Frame, text="Save", command=self.add, font=("goudy old style",15), bg="#2196f3", fg="white", cursor="hand2").place(x=10, y=460, width=100, height=40)
        btn_update=Button(product_Frame, text="Update", command=self.update, font=("goudy old style",15), bg="#4caf50", fg="white", cursor="hand2").place(x=120, y=460, width=100, height=40)
        btn_delete=Button(product_Frame, text="Delete", command= self.delete, font=("goudy old style",15), bg="#f44336", fg="white", cursor="hand2").place(x=230, y=460, width=100, height=40)
        btn_clear=Button(product_Frame, text="Clear", command=self.clear, font=("goudy old style",15), bg="#607d8b", fg="white", cursor="hand2").place(x=340, y=460, width=100, height=40)

        #Search Frame
        SearchFrame=LabelFrame(self.root, text="Search Products", font=("goudy old style",12,"bold"), bd=3, relief=RIDGE, bg="white")
        SearchFrame.place(x=550, y=10, width=700, height=80)

        #options inside search frame
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby, values=("Select","Category","Supplier","Name"), state='readonly', justify=CENTER, font=("goudy old style",15))
        cmb_search.place(x=25,y=10, width=180)
        cmb_search.current(0)#select as permanent option

        #search box
        txt_search=Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style",15), bg="lightyellow").place(x=240, y=10)

        #search btn
        btn_search=Button(SearchFrame, text="Search", command=self.search, font=("goudy old style",15), bg="#4caf50", fg="white", cursor="hand2").place(x=500, y=9, width=150, height=28)

#==============Product Details==============================================================================================================================================================================
        ## Create a frame for the product details
        p_Frame=Frame(self.root, bd=3, relief=RIDGE)
        p_Frame.place(x=550, y=105, width=700, height=500)

        # Create vertical and horizontal scrollbars for the Treeview
        scrolly=Scrollbar(p_Frame, orient=VERTICAL)        
        scrollx=Scrollbar(p_Frame, orient=HORIZONTAL)

        # Create a Treeview widget for displaying employee details
        self.product_table=ttk.Treeview(p_Frame, columns=("pid","category","supplier","name","price","qty","status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)#place bottom scrollbar
        scrolly.pack(side=RIGHT, fill=Y)#place side scrollbar to right
        scrollx.config(command=self.product_table.xview)#make scrollx work
        scrolly.config(command=self.product_table.yview)#make scrolly work 

        # Set column headings for the Treeview
        self.product_table.heading("pid", text="Product ID")
        self.product_table.heading("category", text="Category")
        self.product_table.heading("supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("status", text="Status")
        
        
        # Configure the Treeview to show only headings
        self.product_table["show"]="headings"

        # Set column widths for the Treeview
        self.product_table.column("pid", width=80)
        self.product_table.column("category", width=110)
        self.product_table.column("supplier", width=110)
        self.product_table.column("name", width=90)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)
        
        
        # Pack the Treeview to fill the available space and expand
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)#setting event to get get_data function after releasing button 
        
        self.show()
        
#===========================================================================================================
    #Fetching data from other table
    
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")#setting list as empty if there is nothing
        self.sup_list.append("Empty")#setting list as empty if there is nothing
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]#delete empty data
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("SELECT name FROM supplier")
            sup=cur.fetchall()
            
            if len(sup):
                del self.sup_list[:]#delete empty data
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 


   
#======================Buttons Function=======================
     #Adding data into database
    def add(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_sup.get()=="Empty" or self.var_name.get()=="":
                messagebox.showerror("Error", "All fields are required.", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE category=? and supplier=? and name=?", (self.var_cat.get(),self.var_sup.get(),self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                       messagebox.showerror("Error","This Product is already present, please try different.", parent=self.root)    
                else:
                    cur.execute("Insert into product (category,supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",(
                                                self.var_cat.get(),
                                                self.var_sup.get(),             
                                                self.var_name.get(),
                                                self.var_price.get(),
                                                self.var_qty.get(),
                                                self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully.", parent=self.root)
                    self.show()           
                                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 
            

    #For Showing Detail
    def show(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
                cur.execute("SELECT * FROM product")
                rows=cur.fetchall()
                self.product_table.delete(*self.product_table.get_children())
                for row in rows:
                    self.product_table.insert('', END, values=row)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 

    
    #to display database data into entry box
    def get_data(self, ev):
        f=self.product_table.focus()
        content= (self.product_table.item(f))
        row=content['values']
        
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])             
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])
         
    
    #Update data into database
    def update(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Please select product from list.", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                       messagebox.showerror("Error","Invalid Product ID.", parent=self.root)    
                else:
                    cur.execute("Update product set category=?,supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                                                self.var_cat.get(),
                                                self.var_sup.get(),             
                                                self.var_name.get(),
                                                self.var_price.get(),
                                                self.var_qty.get(),
                                                self.var_status.get(),
                                                self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully.", parent=self.root)
                    self.show()           
                                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 
            
            
    #for deleting data in database
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error", "Please select product from the list.", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                       messagebox.showerror("Error","Invalid Product ID.", parent=self.root)    
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()                     
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()
                     
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
          
          
    #For clearing data
    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")             
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()
          

    #for searching data in database
    def search(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By Option.", parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search Input Must Be Required.", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE {} LIKE ?".format(self.var_searchby.get()), ('%' + self.var_searchtxt.get() + '%',))
                rows=cur.fetchall()
                if len(rows)!=0:    
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found.", parent=self.root)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 




# This block of code will only run if the script is executed directly, not when it's imported as a module.
if __name__=="__main__":
    root=Tk()# Create the main Tkinter window
    obj=productClass(root)# Create an instance of the productClass class
    root.mainloop()# Start the Tkinter event loop, make window open after execution
