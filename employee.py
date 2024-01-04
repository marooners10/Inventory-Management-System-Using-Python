from tkinter import* #for GUI application
from PIL import Image,ImageTk #to use jpg or gif images
from tkinter import ttk, messagebox
import sqlite3

# Define a class named "employeeClass" for the Inventory Management System
class employeeClass:
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
        
        self.var_emp_id=StringVar()#id
        self.var_gender=StringVar()#gender
        self.var_contact=StringVar()#contact
        self.var_name=StringVar()#name
        self.var_dob=StringVar()#dob
        self.var_doj=StringVar()#doj
        self.var_email=StringVar()#email
        self.var_pass=StringVar()#password
        self.var_utype=StringVar()#userType
        self.var_salary=StringVar()#salary
                
        
        #Search Frame
        SearchFrame=LabelFrame(self.root, text="Search Employee", font=("goudy old style",12,"bold"), bd=3, relief=RIDGE, bg="white")
        SearchFrame.place(x=360, y=20, width=600, height=70)

        #options inside search frame
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby, values=("Select","Email","Name","Contact"), state='readonly', justify=CENTER, font=("goudy old style",15))
        cmb_search.place(x=10,y=10, width=180)
        cmb_search.current(0)#select as permanent option

        #search box
        txt_search=Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style",15), bg="lightyellow").place(x=200, y=10)

        #search btn
        btn_search=Button(SearchFrame, text="Search", command=self.search, font=("goudy old style",15), bg="#4caf50", fg="white", cursor="hand2").place(x=433, y=9, width=150, height=28)

        #title
        title = Label(self.root, text="Employee Details", font=("goudy old style",15), bg="#0f4d7d", fg="white").place(x=100, y=100, width=1100)

        #Contents
        #Row1
        lbl_empid = Label(self.root, text="Emp ID", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style",15), bg="white", fg="black").place(x=500, y=150)
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style",15), bg="white", fg="black").place(x=900, y=150)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=200, y=150, width=200)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender, values=("Select","Male","Female","Others"), state='readonly', justify=CENTER, font=("goudy old style",15))
        cmb_gender.place(x=600, y=150, width=200)
        cmb_gender.current(0)#select as permanent option
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=1000, y=150, width=200)
    
        #Row2
        lbl_name = Label(self.root, text="Name", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=200)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style",15), bg="white", fg="black").place(x=500, y=200)
        lbl_doj = Label(self.root, text="D.O.J", font=("goudy old style",15), bg="white", fg="black").place(x=900, y=200)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=200, y=200, width=200)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=600, y=200, width=200)        
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=1000, y=200, width=200)

        #Row3
        lbl_email = Label(self.root, text="Email", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=250)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style",15), bg="white", fg="black").place(x=500, y=250)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style",15), bg="white", fg="black").place(x=900, y=250)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=200, y=250, width=200)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=600, y=250, width=200)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype, values=("Admin","Employee"), state='readonly', justify=CENTER, font=("goudy old style",15))
        cmb_utype.place(x=1000, y=250, width=200)
        cmb_utype.current(0)#admin as permanent option


        #Row4
        lbl_address = Label(self.root, text="Address", font=("goudy old style",15), bg="white", fg="black").place(x=100, y=300)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style",15), bg="white", fg="black").place(x=500, y=300)

        self.txt_address = Text(self.root, font=("goudy old style",15), bg="lightyellow", fg="black")
        self.txt_address.place(x=200, y=300, width=250, height=50)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style",15), bg="lightyellow", fg="black").place(x=600, y=300, width=200)


        #buttons
        btn_add=Button(self.root, text="Save", command=self.add, font=("goudy old style",15), bg="#2196f3", fg="white", cursor="hand2").place(x=500, y=350, width=110, height=28)
        btn_update=Button(self.root, text="Update", command=self.update, font=("goudy old style",15), bg="#4caf50", fg="white", cursor="hand2").place(x=620, y=350, width=110, height=28)
        btn_delete=Button(self.root, text="Delete", command= self.delete, font=("goudy old style",15), bg="#f44336", fg="white", cursor="hand2").place(x=740, y=350, width=110, height=28)
        btn_clear=Button(self.root, text="Clear", command=self.clear, font=("goudy old style",15), bg="#607d8b", fg="white", cursor="hand2").place(x=860, y=350, width=110, height=28)

#============================================================================================================================================================================================
        #Employee Details
        ## Create a frame for the employee details
        emp_Frame=Frame(self.root, bd=3, relief=RIDGE)
        emp_Frame.place(x=0, y=400, relwidth=1, height=224)

        # Create vertical and horizontal scrollbars for the Treeview
        scrolly=Scrollbar(emp_Frame, orient=VERTICAL)        
        scrollx=Scrollbar(emp_Frame, orient=HORIZONTAL)

        # Create a Treeview widget for displaying employee details
        self.EmployeeTable=ttk.Treeview(emp_Frame, columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)#place bottom scrollbar
        scrolly.pack(side=RIGHT, fill=Y)#place side scrollbar to right
        scrollx.config(command=self.EmployeeTable.xview)#make scrollx work
        scrolly.config(command=self.EmployeeTable.yview)#make scrolly work 

        # Set column headings for the Treeview
        self.EmployeeTable.heading("eid", text="EMPLOYEE ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="Joining Date")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")
        
        # Configure the Treeview to show only headings
        self.EmployeeTable["show"]="headings"

        # Set column widths for the Treeview
        self.EmployeeTable.column("eid", width=80)
        self.EmployeeTable.column("name", width=110)
        self.EmployeeTable.column("email", width=110)
        self.EmployeeTable.column("gender", width=90)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)
        
        # Pack the Treeview to fill the available space and expand
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)#setting event to get get_data function after releasing button 
        
        self.show()
#===========================================================================================================

    #Adding data into database
    def add(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            if self.var_emp_id.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error", "Employee ID and Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                       messagebox.showerror("Error","This Employee Id is already assigned, please try different.", parent=self.root)    
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                                self.var_emp_id.get(),
                                                self.var_name.get(),             
                                                self.var_email.get(),
                                                self.var_gender.get(),
                                                self.var_contact.get(),
                                                self.var_dob.get(),
                                                self.var_doj.get(),
                                                self.var_pass.get(),
                                                self.var_utype.get(),
                                                self.txt_address.get('1.0',END),
                                                self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully.", parent=self.root)
                    self.show()           
                                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 
            

    #For Showing Detail
    def show(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
                cur.execute("SELECT * FROM employee")
                rows=cur.fetchall()
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                for row in rows:
                    self.EmployeeTable.insert('', END, values=row)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 

    
    #to display database data into entry box
    def get_data(self, ev):
        f=self.EmployeeTable.focus()
        content= (self.EmployeeTable.item(f))
        row=content['values']
        
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])             
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])
        
    
    #Update data into database
    def update(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            if self.var_emp_id.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error", "Employee ID and Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                       messagebox.showerror("Error","Invalid Employee ID.", parent=self.root)    
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                                                self.var_name.get(),             
                                                self.var_email.get(),
                                                self.var_gender.get(),
                                                self.var_contact.get(),
                                                self.var_dob.get(),
                                                self.var_doj.get(),
                                                self.var_pass.get(),
                                                self.var_utype.get(),
                                                self.txt_address.get('1.0',END),
                                                self.var_salary.get(),
                                                self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully.", parent=self.root)
                    self.show()           
                                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 
            
            
    #for deleting data in database
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error", "Employee ID and Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                       messagebox.showerror("Error","Invalid Employee ID.", parent=self.root)    
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()                     
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()
                     
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
          
          
    #For clearing data
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")             
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
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
                cur.execute("SELECT * FROM employee WHERE {} LIKE ?".format(self.var_searchby.get()), ('%' + self.var_searchtxt.get() + '%',))
                rows=cur.fetchall()
                if len(rows)!=0:    
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found.", parent=self.root)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 

        

           
# This block of code will only run if the script is executed directly, not when it's imported as a module.
if __name__=="__main__":
    root=Tk()# Create the main Tkinter window
    obj=employeeClass(root)# Create an instance of the employeeClass class
    root.mainloop()# Start the Tkinter event loop, make window open after execution
