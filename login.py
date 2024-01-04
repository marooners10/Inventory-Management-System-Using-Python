from tkinter import* #For GUI application
from PIL import Image,ImageTk #to use jpg or gif images, PIL=pillow lib
from tkinter import messagebox
import time
import sqlite3
import os
import smtplib #use simple mail transfer protocal
import time
import email_pass 


class Login_system:
    def __init__(self,root):
        # Set up the main window properties
        self.root=root
        self.root.geometry("1550x800+0+0")#provide screen size of dashboard: ht,wt,x-axis,y-axis
        self.root.title("Inventory Management System | Developed by Nima Tsering Tamang") # Set window title
        self.root.config(bg="white")
        
        self.opt=''

        # Load and resize the title logo
        original_image = Image.open("Images/logo1.png")
        resized_image = original_image.resize((30, 50))
        self.icon_title = ImageTk.PhotoImage(resized_image)
        
        # Create a title label with an image, text, and styling
        title = Label(self.root, text="Inventory Management System", compound="left", image= self.icon_title, font=("times new roman", 40, "bold"), bg="#D3D3D3", fg="black",anchor="w", padx=30)
        title.place(x=0, y=0, relwidth=1, height=70)
          

       # Create a "Logout" button
        btn_logout=Button(self.root, text="Logout", font=("times new roman",15,"bold"), bg="yellow", cursor="hand2").place(x=1300, y=10, height=50, width=120)


        # Create a clock label
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t\t Date: DD-MM-YYYY\t\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#010c48", fg="white",)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

         # Load and resize the menu logo
        self.MenuLogo=Image.open("Images/menu.jpg")#menu pic
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
#=====================================================================================================================================================================================
        
        #==================Image=======================
        self.phone_image=ImageTk.PhotoImage(file='Images/phone.jpg')
        self.lbl_PhoneImage=Label(self.root, image=self.phone_image, bd=0).place(x=170, y=140)
    
    
        #==================Login-Frame=============================
        self.employee_id=StringVar()
        self.password=StringVar()   

        login_frame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        login_frame.place(x=720, y=175, width=350, height=450)

        loginTitle=Label(login_frame, text='Login System', font=('Elephant', 30,'bold'), bg='white').pack(fill=X)
     

        lbl_user=Label(login_frame, text='Employee ID', font=('Andalus',15), bg="white", fg="#767171").place(x=67, y=100)
        txt_username=Entry(login_frame, textvariable=self.employee_id, font=('times new roman',15), bg='#ECECEC').place(x=68, y=140, width=200) 
        
        lbl_password=Label(login_frame, text='Password', font=('Andalus',15), bg="white", fg="#767171").place(x=68, y=190)
        txt_password=Entry(login_frame, textvariable=self.password, show='*', font=('times new roman',15), bg='#ECECEC').place(x=68, y=230, width=200) 
    
        # Create a login button
        btn_login=Button(login_frame, command=self.login, text="log In", font=("Arial Rounded MT Bold",15), bg="#00B0F0", activebackground='#00B0F0', fg='white', activeforeground='white', cursor="hand2").place(x=68, y=290, height=30, width=200)

        hr=Label(login_frame, bg="lightgray").place(x=68, y=360, width=200, height=2)
        or_=Label(login_frame,text='OR', fg="lightgray", bg='white', font=('times new roman', 15, 'bold')).place(x=150, y=345)

        btn_forget=Button(login_frame, command=self.forget_password, text="Forget Password?", font=("times new roman",13), bg="white", activebackground='white', fg='#00759E', activeforeground='#00759E', cursor="hand2", bd=0).place(x=110, y=390)


        #==================SignUp-Frame=============================
        #signup_frame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        #signup_frame.place(x=720, y=640, width=350, height=50)

        #lbl_reg=Label(signup_frame,text="Don't have an account ?", font=('times new roman', 13), bg='white').place(x=66, y=13)

        #btn_signup=Button(signup_frame, text="Sign Up", font=("times new roman",13), bg="white", activebackground='white', fg='#00759E', activeforeground='#00759E', cursor="hand2", bd=0).place(x=230, y=11)
 
#=============================Images Animation===================================================================================================
        self.im1=Image.open("Images/1.jpg")
        self.im1=self.im1.resize((400,250))
        self.im1=ImageTk.PhotoImage(self.im1)

        self.im2=Image.open("Images/2.jpg")
        self.im2=self.im2.resize((400,250))
        self.im2=ImageTk.PhotoImage(self.im2)
        
        self.im3=Image.open("Images/3.jpg")
        self.im3=self.im3.resize((400,250))
        self.im3=ImageTk.PhotoImage(self.im3)
        
        self.lbl_change_img=Label(self.root, bg="white")
        self.lbl_change_img.place(x=312, y=220, width=270, height=479)
 
        self.update_date()
        self.animate()
        
        
 
#========================================Functions=====================================================================================================================================================
        #update date and time 
    def update_date(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t\t Date: {str(date_)}\t\t\t Time: {str(time_)}")
        self.lbl_clock.after(200, self.update_date)#update after every 2 milliSec


    # def login(self): with username and password admin
    #     if self.employee_id.get()=="" or self.password.get()=="":
    #         messagebox.showerror('Error','All Fields are required', parent=self.root)
    #     elif self.employee_id.get()!="admin" and self.password.get()!="admin":
    #         messagebox.showerror('Error','Invalid Username or Password.\nPlease try again', parent=self.root)
    #     else:
    #         messagebox.showinfo("Information",f"Welcome to your Inventory Management System")
        
    def login(self):
        con=sqlite3.connect(database=r'ims.db')    
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error','All Fields are required', parent=self.root)
            else:
                cur.execute("SELECT utype FROM employee where eid=? AND pass=?",(self.employee_id.get(), self.password.get()))
                user=cur.fetchone()
            if user is None:
                messagebox.showerror('Error','Invalid Employee ID or Password', parent=self.root)
            else:
                if user[0]=='Admin':
                    self.root.destroy()
                    os.system("python dashboard.py") 
                else:
                    self.root.destroy()
                    os.system("python billing.py") 
    
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)
    
    
    def forget_password(self):
        con=sqlite3.connect(database=r'ims.db')    
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error','Employee ID is required', parent=self.root)
            else:
                cur.execute("SELECT email FROM employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
            if email is None:
                messagebox.showerror('Error','Invalid Employee ID.\n Please try again', parent=self.root)
            else:
                #=====================Reset Password Window===========================
                self.var_otp=StringVar()
                self.var_newPassword=StringVar()
                self.var_confirmPassword=StringVar()
                chk=self.send_email(email[0])#call send_email_function
                if chk=='fail':
                    messagebox.showerror('Error','Connection Error, Please try again', parent=self.root)
                else:
                    self.forget_window=Toplevel(self.root)#create new window for password reset 
                    self.forget_window.title("Inventory Management System | Password Reset")
                    self.forget_window.geometry('400x380+550+230')
                    self.forget_window.focus_force()

                    title1=Label(self.forget_window, text="RESET PASSWORD", font=('goudy old style',15,"bold"), fg="white", bg="#3f51b5").pack(fill=X, side=TOP)
                    lbl_reset= Label(self.forget_window, text="Please enter OPT sent on Registered Email:", font=("times new roman", 15)).place(x=20, y=50)
                    txt_reset=Entry(self.forget_window, textvariable=self.var_otp, font=("times new roman", 13), bg="lightyellow").place(x=20, y=90, width=250, height=30)
                    self.btn_reset=Button(self.forget_window, command=self.validate_otp, text="SUBMIT", font=("times new roman", 13), bg="lightblue", activebackground="lightblue", cursor="hand2")
                    self.btn_reset.place(x=280, y=87, width=100, height=30)

                    lbl_newPassword= Label(self.forget_window, text="New Password:", font=("times new roman", 15)).place(x=20, y= 133)
                    txt_newPassword=Entry(self.forget_window, textvariable=self.var_newPassword, font=("times new roman", 13), bg="lightyellow").place(x=20, y=170, width=250, height=30)
                    
                    lbl_confirmPassword= Label(self.forget_window, text="Confirm Password:", font=("times new roman", 15)).place(x=20, y= 213)
                    txt_confirmPassword=Entry(self.forget_window, textvariable=self.var_confirmPassword, font=("times new roman", 13), bg="lightyellow").place(x=20, y=250, width=250, height=30)

                    self.btn_update=Button(self.forget_window, command=self.update_newPassword, text="UPDATE", state=DISABLED, font=("times new roman", 13), bg="lightblue", activebackground="lightblue", cursor="hand2")
                    self.btn_update.place(x=150, y=310, width=100, height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)
               

             
     #Animating function
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_img.config(image=self.im)
        self.lbl_change_img.after(5000, self.animate)
    
    #for otp generstor and password change 
    def send_email(self, to_):
        s=smtplib.SMTP('smtp.gmail.com',587)#host,port
        s.starttls()#for security purpose from hacking
        
        #call email and pass var from email_pass.py
        email_=email_pass.email_
        pass_=email_pass.pass_
        
        s.login(email_, pass_)
        
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))#generate otp

        subj='IMS-Reset Password OTP'
        msg=f'Dear user,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'
        msg="Subject: {}\n\n{}".format(subj,msg)
        s.sendmail(email_, to_, msg)#send otp mail to user
        chk=s.ehlo()#check if message is send or not
        if chk[0]==250:
            return 'success'
        else:
            return 'fail'
        
    #for checking generated OTP
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror('Error','Invalid OTP, Please try again', parent=self.forget_window)
            
    #update new password
    def update_newPassword(self):
        if self.var_newPassword.get()=="" or self.var_confirmPassword.get()=="":
            messagebox.showerror("Error","Password is required", parent=self.forget_window)
        elif self.var_newPassword.get()!=self.var_confirmPassword.get():
            messagebox.showerror("Error","New Password & Confirm Password must be same", parent=self.forget_window)
        else:
            con=sqlite3.connect(database=r'ims.db')    
            cur=con.cursor()
            try:
                cur.execute("UPDATE employee SET pass=? WHERE eid=?",(self.var_newPassword.get(), self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated successfully", parent=self.forget_window)
                self.forget_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}", parent=self.root)

            
            
        
          


        
           
            
root=Tk()# Create the main Tkinter window
obj=Login_system(root)# Create an instance of the Login_system class
root.mainloop()# Start the Tkinter event loop, make window open after execution

 