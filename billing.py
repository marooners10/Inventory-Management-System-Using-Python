from tkinter import* #for GUI application
from PIL import Image,ImageTk #to use jpg or gif images
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile #generate temp file which is use to store bill

# Define a class named "billClass" for the Inventory Management System
class billClass:
    def __init__(self,root): 
        # Set up the main window properties
        self.root=root
        self.root.geometry("1550x800+0+0")#provide screen size of dashboard: ht,wt,x-axis,y-axis
        self.root.title("Inventory Management System | Developed by Nima Tsering Tamang") # Set window title
        self.root.config(bg="white")
        self.cart_list=[]#to update the cart according to quantity's input
        self.chk_print=0
        
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


#===============All_Product_Frame===========================
    
        ProductFrame=Frame(self.root ,bd=4, relief=RIDGE, bg="White")
        ProductFrame.place(x=6, y=120, width=420, height=650)

        pTitle=Label(ProductFrame, text="All Products", font=("goudy old style",20,"bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)
        #==================MiniProductFrame1========================================        
        #Product Search Frame
        self.var_search=StringVar()#for entry field
        MiniProductFrame1=Frame(ProductFrame, bd=2, relief=RIDGE, bg="white")
        MiniProductFrame1.place(x=2, y=42, width=408, height=90)

        lbl_search=Label(MiniProductFrame1, text="Search Product | By Name ", font=("times new roman",15,"bold"), bg="white", fg="green").place(x=2, y=5)        
         
        lbl_name=Label(MiniProductFrame1, text="Product Name ", font=("times new roman",15,"bold"), bg="white").place(x=5, y=45)               
        txt_search=Entry(MiniProductFrame1, textvariable=self.var_search, font=("times new roman",15), bg="lightyellow").place(x=138, y=45, width=150, height=30)        
        btn_search=Button(MiniProductFrame1, command=self.search, text="Search", font=("goudy old style",15), bg="#2196f3", fg="white", cursor="hand2").place(x=300, y=44, width=95, height=30)        
        btn_show_all=Button(MiniProductFrame1, command=self.show, text="Show All", font=("goudy old style",15), bg="#083531", fg="white", cursor="hand2").place(x=300, y=10, width=95, height=30)        

        #==========================MiniProductFrame2=======================================
        MiniProductFrame2=Frame(ProductFrame, bd=3, relief=RIDGE)
        MiniProductFrame2.place(x=2, y=152, width=408, height=465)

        # Create vertical and horizontal scrollbars for the Treeview
        scrolly=Scrollbar(MiniProductFrame2, orient=VERTICAL)        
        scrollx=Scrollbar(MiniProductFrame2, orient=HORIZONTAL)

        # Create a Treeview widget for displaying employee details
        self.productTable=ttk.Treeview(MiniProductFrame2, columns=("pid","name","price","qty","status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)#place bottom scrollbar
        scrolly.pack(side=RIGHT, fill=Y)#place side scrollbar to right
        scrollx.config(command=self.productTable.xview)#make scrollx work
        scrolly.config(command=self.productTable.yview)#make scrolly work 

        # Set column headings for the Treeview
        self.productTable.heading("pid", text="Product Id")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="Quantity")
        self.productTable.heading("status", text="Status")
        
        # Configure the Treeview to show only headings
        self.productTable["show"]="headings"

        # Set column widths for the Treeview
        self.productTable.column("pid", width=80)
        self.productTable.column("name", width=110)
        self.productTable.column("price", width=110)
        self.productTable.column("qty", width=60)
        self.productTable.column("status", width=90)
        
        
        # Pack the Treeview to fill the available space and expand
        self.productTable.pack(fill=BOTH, expand=1)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)#setting event to get get_data function after releasing button. Use to fetch data from table 
        lbl_note=Label(ProductFrame, text="Note: 'Enter 0 Quantity to remove product from the Cart.'", font=("goudy old style",12), anchor='w', bg="white", fg="red").pack(side=BOTTOM, fill=X)
                       
#=============================Customer-Frame==================================================================
        self.var_cname=StringVar()#var to store customer's name
        self.var_contact=StringVar()#var to store customer's contact
        CustomerFrame=Frame(self.root ,bd=4, relief=RIDGE, bg="White")
        CustomerFrame.place(x=450, y=120, width=600, height=80)

        cTitle=Label(CustomerFrame, text="Customer Details", font=("goudy old style",15,"bold"), bg="lightgray").pack(side=TOP, fill=X)

        lbl_name=Label(CustomerFrame, text="Customer Name", font=("times new roman",15), bg="white").place(x=5, y=40)               
        txt_name=Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman",15), bg="lightyellow").place(x=140, y=40, width=180)        
        
        lbl_contact=Label(CustomerFrame, text="Phone No. ", font=("times new roman",15), bg="white").place(x=340, y=40)               
        txt_contact=Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman",15), bg="lightyellow").place(x=430, y=40, width=155)        

#===================Calculator AND Cart Frame=========================================================================

        Cal_Cart_Frame=Frame(self.root ,bd=4, relief=RIDGE, bg="White")
        Cal_Cart_Frame.place(x=450, y=230, width=600, height=415)

        #Calculator Frame
        self.var_cal_input=StringVar()
        Cal_Frame=Frame(Cal_Cart_Frame, bd=12, relief=RIDGE, bg="white")
        Cal_Frame.place(x=5, y=13, width=300, height=380)

        txt_cal_input=Entry(Cal_Frame, textvariable=self.var_cal_input, font=("arial", 13, "bold"), width=29, bd=11, relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)#row and column wise, 1 row=4 column

        #calculator btn
        btn_7=Button(Cal_Frame, text="7", font=('arial', 15, 'bold'), command=lambda: self.get_input(7), bd=5, width=4, pady=15, cursor='hand2').grid(row=1, column=0 )
        btn_8=Button(Cal_Frame, text="8", font=('arial', 15, 'bold'), command=lambda: self.get_input(8), bd=5, width=4, pady=15, cursor='hand2').grid(row=1, column=1 )
        btn_9=Button(Cal_Frame, text="9", font=('arial', 15, 'bold'), command=lambda: self.get_input(9), bd=5, width=4, pady=15, cursor='hand2').grid(row=1, column=2 )
        btn_sum=Button(Cal_Frame, text="+", font=('arial', 15, 'bold'), command=lambda: self.get_input('+'), bd=5, width=4, pady=15, cursor='hand2').grid(row=1, column=3 )
        
        btn_4=Button(Cal_Frame, text="4", font=('arial', 15, 'bold'), command=lambda: self.get_input(4),bd=5, width=4, pady=15, cursor='hand2').grid(row=2, column=0 )
        btn_5=Button(Cal_Frame, text="5", font=('arial', 15, 'bold'), command=lambda: self.get_input(5), bd=5, width=4, pady=15, cursor='hand2').grid(row=2, column=1 )
        btn_6=Button(Cal_Frame, text="6", font=('arial', 15, 'bold'), command=lambda: self.get_input(6), bd=5, width=4, pady=15, cursor='hand2').grid(row=2, column=2 )
        btn_sub=Button(Cal_Frame, text="-", font=('arial', 15, 'bold'), command=lambda: self.get_input('-'), bd=5, width=4, pady=15, cursor='hand2').grid(row=2, column=3 )
        
        btn_1=Button(Cal_Frame, text="1", font=('arial', 15, 'bold'), command=lambda: self.get_input(1), bd=5, width=4, pady=15, cursor='hand2').grid(row=3, column=0 )
        btn_2=Button(Cal_Frame, text="2", font=('arial', 15, 'bold'), command=lambda: self.get_input(2), bd=5, width=4, pady=15, cursor='hand2').grid(row=3, column=1 )
        btn_3=Button(Cal_Frame, text="3", font=('arial', 15, 'bold'), command=lambda: self.get_input(3), bd=5, width=4, pady=15, cursor='hand2').grid(row=3, column=2 )
        btn_mul=Button(Cal_Frame, text="*", font=('arial', 15, 'bold'), command=lambda: self.get_input('*'), bd=5, width=4, pady=15, cursor='hand2').grid(row=3, column=3 )
        
        btn_0=Button(Cal_Frame, text="0", font=('arial', 15, 'bold'), command=lambda: self.get_input(0), bd=5, width=4, pady=15, cursor='hand2').grid(row=4, column=0 )
        btn_c=Button(Cal_Frame, text="C", font=('arial', 15, 'bold'), command=self.clear_cal, bd=5, width=4, pady=15, cursor='hand2').grid(row=4, column=1 )
        btn_eq=Button(Cal_Frame, text="=", font=('arial', 15, 'bold'), command=self.perform_cal, bd=5, width=4, pady=15, cursor='hand2').grid(row=4, column=2 )
        btn_div=Button(Cal_Frame, text="/", font=('arial', 15, 'bold'), command=lambda: self.get_input('/'), bd=5, width=4, pady=15, cursor='hand2').grid(row=4, column=3 )
        



        #=======================================================
        #Cart Frame
        Cart_Frame=Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        Cart_Frame.place(x=310, y=13, width=280, height=380)

        self.cartTitle=Label(Cart_Frame, text="Cart \t Total Product: [0]", font=("goudy old style",15,"bold"), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)
        
        # Create vertical and horizontal scrollbars for the Treeview
        scrolly=Scrollbar(Cart_Frame, orient=VERTICAL)        
        scrollx=Scrollbar(Cart_Frame, orient=HORIZONTAL)

        # Create a Treeview widget for displaying employee details
        self.cartTable=ttk.Treeview(Cart_Frame, columns=("pid","name","price","qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)#place bottom scrollbar
        scrolly.pack(side=RIGHT, fill=Y)#place side scrollbar to right
        scrollx.config(command=self.cartTable.xview)#make scrollx work
        scrolly.config(command=self.cartTable.yview)#make scrolly work 

        # Set column headings for the Treeview
        self.cartTable.heading("pid", text="Product Id")
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Quantity")
        
        # Configure the Treeview to show only headings
        self.cartTable["show"]="headings"

        # Set column widths for the Treeview
        self.cartTable.column("pid", width=70)
        self.cartTable.column("name", width=100)
        self.cartTable.column("price", width=70)
        self.cartTable.column("qty", width=60)
        
        
        # Pack the Treeview to fill the available space and expand
        self.cartTable.pack(fill=BOTH, expand=1)
        self.cartTable.bind("<ButtonRelease-1>", self.get_data_cart)#setting event to get get_data function after releasing button 

        #=====================================================================
        #Add Cart Widgets Frame
        self.var_pid=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        Add_CartWidgetsFrame=Frame(self.root ,bd=4, relief=RIDGE, bg="White")
        Add_CartWidgetsFrame.place(x=450, y=665, width=600, height=105)

        lbl_p_name=Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman",15), bg="white").place(x=35, y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame, textvariable=self.var_name, font=("times new roman",15), bg="lightyellow", state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman",15), bg="white").place(x=268, y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman",15), bg="lightyellow", state='readonly').place(x=250, y=35, width=150, height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman",15), bg="white").place(x=470, y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman",15), bg="lightyellow").place(x=450, y=35, width=130, height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman",15,"bold"), bg="white")
        self.lbl_inStock.place(x=5, y=65)

        btn_clear_cart=Button(Add_CartWidgetsFrame, command=self.clear_cart, text="Clear", font=('times new roman', 15, "bold"), bg="lightgray", cursor="hand2").place(x=250, y=65, width=120, height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame, command=self.add_update_cart, text="Add | Update Cart", font=('times new roman', 15, "bold"), bg="orange", cursor="hand2").place(x=400, y=65, width=180, height=30)

#=============================Billing Area============================================================================================================================================================
        
        billFrame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=1085, y=120, width=430, height=500)

        bTitle=Label(billFrame, text="Customer Bill Area", font=("goudy old style",20,"bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)

        #Setting scroll bar in right side of customer bill area along with text area        
        scrolly=Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area=Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)


        #========================================================================
        #Billing buttons
        billMenuFrame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=1085, y=630, width=430, height=140)

        self.lbl_amt=Label(billMenuFrame, text="Bill Amount", font=('goudy old style', 13, "bold"), bd=2, relief=RIDGE , bg="#3f51b5", fg="white")
        self.lbl_amt.place(x=5, y=6, width=130, height=70)

        self.lbl_discount=Label(billMenuFrame, text="Discount\n[5%]", font=('goudy old style', 13, "bold"), bd=2, relief=RIDGE , bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=148, y=6, width=130, height=70)

        self.lbl_net_pay=Label(billMenuFrame, text="Net Pay", font=('goudy old style', 13, "bold"), bd=2, relief=RIDGE , bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=290, y=6, width=130, height=70)

        btn_print=Button(billMenuFrame, command=self.print_bill, text="Print", cursor="hand2", font=('goudy old style', 15, "bold"), bd=2, relief=RIDGE , bg="lightgreen", fg="white")
        btn_print.place(x=5, y=80, width=130, height=50)

        btn_clear=Button(billMenuFrame, command=self.clear_all, text="Clear All", cursor="hand2", font=('goudy old style', 15, "bold"), bd=2, relief=RIDGE , bg="gray", fg="white")
        btn_clear.place(x=148, y=80, width=130, height=50)

        btn_generate=Button(billMenuFrame, command=self.generate_bill, text="Generate Bill", cursor="hand2", font=('goudy old style', 15, "bold"), bd=2, relief=RIDGE , bg="#009688", fg="white")
        btn_generate.place(x=290, y=80, width=130, height=50)
        
#======================Footer=================================================================================
        footer=Label(self.root, text="For any Technical Issue contact: 98611xxxxx", font=("times new roman", 14, "bold"), bg="#4d636d", fg="white", bd=0).pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()
#==================================Calculator Functions==============================================================================================================================================
    #for calculator input
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum) #take input then convert into string then display
    #for claculator clear
    def clear_cal(self):
        self.var_cal_input.set('')
    #for claculator calculation
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))  
#=================================================================================

    #Fetching data from product table
    def show(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
                cur.execute("SELECT pid,name,price,qty,status FROM product WHERE status='Active'")
                rows=cur.fetchall()
                self.productTable.delete(*self.productTable.get_children())
                for row in rows:
                    self.productTable.insert('', END, values=row)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 


    #for searching data in database from product table
    def search(self):
        con= sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search Input Must Be Required.", parent=self.root)
            else:
                cur.execute("SELECT pid, name, price, qty, status FROM product WHERE name LIKE ? AND status='Active'", ('%' + self.var_search.get() + '%',))
                rows=cur.fetchall()
                if len(rows)!=0:    
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found.", parent=self.root)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 


    #to display database data into entry box
    def get_data(self, ev):
        f=self.productTable.focus()
        content= (self.productTable.item(f))
        row=content['values']
        
        self.var_pid.set(row[0])
        self.var_name.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')#setting default quantity 1 
        
#to display cart data into entry box
    def get_data_cart(self, ev):
        f=self.cartTable.focus()
        content= (self.cartTable.item(f))
        row=content['values']
        
        #pid, name, price, qty, stock
        self.var_pid.set(row[0])
        self.var_name.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        self.var_qty.set(row[3])#setting default quantity 1 

  
    #to update the cart
    def add_update_cart(self):
        if self.var_pid.get()=='':
           messagebox.showerror("Error","Please select product from the list", parent=self.root) 
        elif self.var_qty.get()=='':
            messagebox.showerror("Error","Quantity is Required", parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()) :
            messagebox.showerror("Error","Invalid Quantity", parent=self.root)

        else:
            #price_cal=int(self.var_qty.get()) * float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()

            cart_data=[self.var_pid.get(), self.var_name.get(), price_cal, self.var_qty.get(), self.var_stock.get() ]
            
            #=========update cart===========
            #if pid is repeated then update else add the qty
            # But whenever qty == 0 then pop that item from list
            present='no'
            index_=-1
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
               op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update| Remove from the Cart List", parent=self.root)
               if op==True:
                   if self.var_qty.get()=="0":
                       self.cart_list.pop(index_)
                   else:
                       #pid, name, price, qty, stock
                       #self.cart_list[index_][2]=price_cal #price
                       self.cart_list[index_][3]=self.var_qty.get()#qty
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()
    
    #bill_update:
    def bill_updates(self):
        self.bill_amt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            #pid, name, price, qty, stock
            self.bill_amt=self.bill_amt + (float(row[2])*int(row[3]))
        
        self.discount= (self.bill_amt * 5)/100
        self.net_pay=self.bill_amt - self.discount
        self.lbl_amt.config(text=f"Bill Amt.(Rs.)\n{str(self.bill_amt)}")
        self.lbl_net_pay.config(text=f"Net Pay(Rs.)\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")#to update total product
    
    
    #to show cart detail 
    def show_cart(self):
        try:
            
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
             self.cartTable.insert('', END, values=row)
    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",  parent=self.root) 

    #==================================================================================   
    #for generating billing function:
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error", f"Customer Details are required",  parent=self.root) 
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please add product to the cart",  parent=self.root) 
        else:
            #=====bill top part======
            self.bill_top()
            #=====bill middle part======
            self.bill_middle()
            #=====bill buttom part======
            self.bill_buttom()
            
            #open the txt file in customer_bill_area in sales file.
            fp=open(f'bill/{str(self.invoice)}.txt','w')#open bill in write mode
            fp.write(self.txt_bill_area.get('1.0',END))#write data of bill area from 1.0 to END and save
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/saved in Backend ", parent=self.root)
            self.chk_print=1
    
    #for bill top part
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No.: 98********, Kathmandu,Nepal
\n{str("=" *50)} 
 Customer Name: {self.var_cname.get()}
 Phone No.: {self.var_contact.get()}
 Bill No.: {str(self.invoice)}\t\t\t
 Date: {str(time.strftime("%d/%m/%Y"))}
\n{str("=" *50)}
 Product Name:\t\t\tQuantity:\t\tPrice:
{ str("=" *50)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
    
    #for bill buttom part
    def bill_buttom(self):
        bill_buttom_temp=f'''
\n{ str("=" *50)}
 Bill Amount\t\t\t\t  Rs.{self.bill_amt }
 Discount\t\t\t\t  Rs.{self.discount}
 Net Pay\t\t\t\t  Rs.{self.net_pay}
{ str("=" *50)}       
        '''
        self.txt_bill_area.insert(END,bill_buttom_temp)


    #for middle bill part    
    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                #pid,name,price,qty,stock
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
             
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t    "+row[3]+"\t    Rs."+price)

                #update qty in product table
                cur.execute('Update product set qty=?, status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)
    
    #for clearing cart input sector
    def clear_cart(self):
        #pid, name, price, qty, stock
        self.var_pid.set('')
        self.var_name.set('')
        self.var_price.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
        self.var_qty.set('')# 

    def clear_all(self):
        del self.cart_list[:]#clear cart list
        self.var_cname.set('')#clear customer's name
        self.var_contact.set('')#clear customer's contact
        self.txt_bill_area.delete('1.0',END)#delete txt_bill_area
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")#total product will be 0
        self.var_search.set('')#search setting empty
        self.clear_cart()#clear cart
        self.show()#show product treeview
        self.show_cart()#since firstly cart_list is called so initially cart will be empty after this call 
        self.chk_print=0
    
    #update date and time 
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t\t Date: {str(date_)}\t\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)#update after every 2 milliSec
    
    
    #print bill
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing", parent=self.root)
            #===========Printing==============
            # Create a temporary text file
            file_descriptor, new_file_path = tempfile.mkstemp('.txt')
            # Write content to the file
            with open(new_file_path, 'w') as file:
                file.write(self.txt_bill_area.get('1.0', 'end'))
            # Close the file descriptor
            os.close(file_descriptor)
            # Open the file for printing
            os.startfile(new_file_path, 'print')
        else:
            messagebox.showerror("Error","Please generate bill first to print receipt", parent=self.root)

    #logout
    def logout(self):
        self.root.destroy()
        os.system("python login.py")
            
# This block of code will only run if the script is executed directly, not when it's imported as a module.
if __name__=="__main__":
    root=Tk()# Create the main Tkinter window
    obj=billClass(root)# Create an instance of the billClass class
    root.mainloop()# Start the Tkinter event loop, make window open after execution
