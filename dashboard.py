from tkinter import* #for GUI application
from PIL import Image,ImageTk #to use jpg or gif images
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time

# Define a class named "IMS" for the Inventory Management System
class IMS:
    def __init__(self,root):
        # Set up the main window properties
        self.root=root
        self.root.geometry("1550x800+0+0")#provide screen size of dashboard: ht,wt,x-axis,y-axis
        self.root.title("Inventory Management System | Developed by Nima Tsering Tamang") # Set window title
        self.root.config(bg="white")
        
        # Load and resize the title logo
        original_image = Image.open("Images/logo1.png")
        resized_image = original_image.resize((30, 50))
        self.icon_title = ImageTk.PhotoImage(resized_image)
        
        # Create a title label with an image, text, and styling
        title = Label(self.root, text="Inventory Management System", compound="left", image= self.icon_title, font=("times new roman", 40, "bold"), bg="#D3D3D3", fg="black",anchor="w", padx=30)
        title.place(x=0, y=0, relwidth=1, height=70)
          

       # Create a "Logout" button
        btn_logout=Button(self.root, command=self.logout, text="Logout", font=("times new roman",15,"bold"), bg="yellow", cursor="hand2").place(x=1300, y=10, height=50, width=120)


        # Create a clock label
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t\t Date: DD-MM-YYYY\t\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#010c48", fg="white",)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

         # Load and resize the menu logo
        self.MenuLogo=Image.open("Images/menu.jpg")#menu pic
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

         # Create a left menu frame
        LeftMenu=Frame(self.root, bd=2, relief=RIDGE, bg="white")#frame
        LeftMenu.place(x=0, y=102, width=200, height=568)
        
         # Create labels and buttons for the menu
        lbl_menuLogo=Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)
        lbl_menu=Label(LeftMenu, text="Menu", font=("times new roman",20), bg="#009688").pack(side=TOP, fill=X)
        
         # Load and resize the side icon
        self.icon_side=Image.open("Images/side.png")#side icon
        self.icon_side=self.icon_side.resize((30,30))
        self.icon_side=ImageTk.PhotoImage(self.icon_side)
        
        # Create buttons for various menu options
        btn_employee=Button(LeftMenu, text="Employee", command= self.employee, image=self.icon_side, compound=LEFT, padx=15, anchor="w" , font=("times new roman",20,"bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_supplier=Button(LeftMenu, text="Supplier", command=self.supplier, image=self.icon_side, compound=LEFT, padx=15, anchor="w" , font=("times new roman",20,"bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_category=Button(LeftMenu, text="Category", command=self.category, image=self.icon_side, compound=LEFT, padx=15, anchor="w" , font=("times new roman",20,"bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_product=Button(LeftMenu, text="Product", command=self.product, image=self.icon_side, compound=LEFT, padx=15, anchor="w" , font=("times new roman",20,"bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)        
        btn_sales=Button(LeftMenu, text="Sales", command=self.sales, image=self.icon_side, compound=LEFT, padx=15, anchor="w" , font=("times new roman",20,"bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit=Button(LeftMenu, text="Exit", image=self.icon_side, compound=LEFT, padx=15, anchor="w" , font=("times new roman",20,"bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        # Create labels for displaying various statistics
        self.lbl_employee=Label(self.root, text="Total Employee\n[0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goundy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=160, height=150, width=300)
        
        self.lbl_supplier=Label(self.root, text="Total Supplier\n[0]", bd=5, relief=RIDGE, bg="#ff5722", fg="white", font=("goundy old style", 20, "bold"))
        self.lbl_supplier.place(x=700, y=160, height=150, width=300)

        self.lbl_category=Label(self.root, text="Total Category\n[0]", bd=5, relief=RIDGE, bg="#009688", fg="white", font=("goundy old style", 20, "bold"))
        self.lbl_category.place(x=1100, y=160, height=150, width=300)

        self.lbl_product=Label(self.root, text="Total Product\n[0]", bd=5, relief=RIDGE, bg="#607d8b", fg="white", font=("goundy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=400, height=150, width=300)
        
        self.lbl_sales=Label(self.root, text="Total Sales\n[0]", bd=5, relief=RIDGE, bg="#ffc107", fg="white", font=("goundy old style", 20, "bold"))
        self.lbl_sales.place(x=700, y=400, height=150, width=300)
        
         # Create a footer label
        lbl_footer = Label(self.root, text="Inventory Management System | Developed by Nima Tsering Tamang\n For any Technical Issue Contact: +9779861175350", font=("times new roman", 12), bg="#010c48", fg="white",)
        lbl_footer.pack(side=BOTTOM, fill=X)


        self.update_content()
#================================================================================================================================================================================================================================

    def employee(self):
        self.new_win=Toplevel(self.root)# Create a new Toplevel window
        self.new_obj=employeeClass(self.new_win) # Instantiate an employeeClass object within the new Toplevel window

    def supplier(self):
        self.new_win=Toplevel(self.root)# Create a new Toplevel window
        self.new_obj=supplierClass(self.new_win) # Instantiate an supplierClass object within the new Toplevel window

    def category(self):
        self.new_win=Toplevel(self.root)# Create a new Toplevel window
        self.new_obj=categoryClass(self.new_win) # Instantiate an categoryClass object within the new Toplevel window

    def product(self):
        self.new_win=Toplevel(self.root)# Create a new Toplevel window
        self.new_obj=productClass(self.new_win) # Instantiate an productClass object within the new Toplevel window

    def sales(self):
        self.new_win=Toplevel(self.root)# Create a new Toplevel window
        self.new_obj=salesClass(self.new_win) # Instantiate an salesClass object within the new Toplevel window

#===================================================================================================================================================================

    #function for updating every content
    
    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n[ {str(len(product))} ]')#len will be ALC to row 

            cur.execute("SELECT * FROM supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')#len will be ALC to row 

            cur.execute("SELECT * FROM category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Categories\n[ {str(len(category))} ]')#len will be ALC to row 

            cur.execute("SELECT * FROM employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))} ]')#len will be ALC to row 

            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales [{str(bill)}]')
        
            #update date and time 
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t\t Date: {str(date_)}\t\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)#update after every 2 milliSec
   
        except Exception as ex:
            messagebox.showerror('Error',f'Error due to : {str(ex)}', parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")        

       

# This block of code will only run if the script is executed directly, not when it's imported as a module.
if __name__=="__main__":
    root=Tk()# Create the main Tkinter window
    obj=IMS(root)# Create an instance of the IMS class
    root.mainloop()# Start the Tkinter event loop, make window open after execution

