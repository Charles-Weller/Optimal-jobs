from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.messagebox import showinfo
import os
import sqlite3
import tkinter as tk

conn = sqlite3.connect("NEADataBase.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS User
                (UserID integer PRIMARY KEY AUTOINCREMENT,
                Name text,
                Email text,
                Age integer,
                Admin Integer,
                Username text,
                Password text)
                """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Job
                (JobID integer PRIMARY KEY AUTOINCREMENT,
                CompanyName text,
                JobTitle text,
                Location text,
                Hours integer,
                Pay integer,
                Age integer,
                JobDescription text,
                ExtraInformation text,
                UserID integer)
                """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Favourites
                (FavouriteID integer PRIMARY KEY AUTOINCREMENT,
                JobID integer,
                UserID integer)
                """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Applicants
                (ApplicantID integer PRIMARY KEY AUTOINCREMENT,
                JobID integer,
                UserID integer)
                """)


class Login_Window():
    def __init__(self,master):
        ##----Creating window----##
        self.master = master
        self.master.geometry("300x250")
        self.master.title("Login page")
        
        ##---Lables on window---##
        self.Username = Label(self.master,text = "Username:")
        self.Username.place(x=0, y=130)
        
        self.Password = Label(self.master,text = "Password:")
        self.Password.place(x=0, y=160)
        
        self.LoginLable1 = Label(self.master,text = "Enter login details:")
        self.LoginLable1.place(x=0, y=100)
        
        ##---Input boxs for Username---##
        self.UsernameInput = Entry(self.master, bd=3)
        self.UsernameInput.place(x=75, y=130)
        ##---Input boxs for Passcode---###
        self.PasswordInput = Entry(self.master, bd=3, show="*")
        self.PasswordInput.place(x=75, y=160)

        ##---Logo---##
        photo = PhotoImage(file = "Company logo.png")
        self.Logo = Label(image = photo)
        self.Logo.image = photo
        self.Logo.place(x=40, y=40)
        
        ##---Quit button---##
        self.QuitB = Button(self.master, text = "Exit", foreground = "red", command = self.LoginConfirmExit) 
        self.QuitB.place(x=215, y=190)
        
        ##---Sign in button---##
        self.Sign_inB = Button(self.master, text = "Sign in", command = self.InputValidation)
        self.Sign_inB.place(x=215, y=140)
        
        ##---Create account buttom---##
        self.Create_AccountB = Button(self.master, text = "Create account", command = self.GotToCreateAccount)
        self.Create_AccountB.place(x=120, y=190)

    def LoginConfirmExit(self):##---Checks with the user if they want to quit the application---##
        ConfirmExit = askyesno("Confirm Quit","Do you want to close this application?")
        if ConfirmExit == True:
            self.master.destroy()

    def InputValidation(self):##---Checks if the the user inputs are correct---##
        Username = self.UsernameInput.get()
        Password = self.PasswordInput.get()

        if Username == "" or Password == "":
            self.SignInInputBoxFullWarning = Label(self.master,text = "Fill all entry boxes", foreground = "red")
            self.SignInInputBoxFullWarning.place(x=100, y=100)
            
        elif len(Username) <6:
            self.SignInUsernameWarning = Label(self.master, text = "Minimum 6 characters for username", foreground = "red")
            self.SignInUsernameWarning.place(x=100, y=100)

        elif len(Password) <6:
            self.SignInPasswordWarning = Label(self.master, text = "Minimum 6 characters for Password", foreground = "red")
            self.SignInPasswordWarning.place(x=100, y=100)

        else:
            self.ValidateSignInDetails(Username, Password)
            
    def ValidateSignInDetails(self, Username, Password):##---Checks to see in the username and password are correct---##
        try:
            cursor.execute("SELECT Password, UserID FROM User WHERE Username = (?)", (Username,))
            conn.commit()
            DatabaseVaue = cursor.fetchall()
            Dencryption = self.Dencryption(DatabaseVaue[0][0])
            if Dencryption == Password:
                global UserID
                UserID = DatabaseVaue[0][1]

                self.SignIn()
            else:
                self.LoginWarning() 
        except:
            self.LoginWarning()

    def LoginWarning(self):##---user to print warnings to say that the username or password are correct---##
        self.SignInLoginWarning = Label(self.master, text = "Username or Password is incorrect", foreground = "red")
        self.SignInLoginWarning.place(x=100, y=100)

    def SignIn(self):##---Used to open/call the "Main" page when validation is passed---##
        root = Toplevel(self.master)
        GUI = Main_Window(root)

    def GotToCreateAccount(self):##---Used to open/call the "Create account" page when Create account button is passed---##
        root1 = Toplevel(self.master)
        GUI = Create_Account_Window(root1)

    def AccountHasBeenCreated():##--- Used to display to the user that there account have been made---##
        Login_Window.AccontHasBeenMade = Label(text = "Your Account has been created")
        Login_Window.AccontHasBeenMade.place(x=100, y=100)

    def Dencryption(self, OriginalValue):##---Used to Decryped the password pulled form the data base---##
      EncryptedString = ""
      shift = 5
      for ch in OriginalValue:
        Value = ord(ch) - shift
        FinalValue = chr(Value)
        EncryptedString += FinalValue
      return EncryptedString

class Create_Account_Window():
    def __init__(self,master):
        ##---creating window---## 
        self.master = master
        self.master.geometry("315x370")
        self.master.title("Create account")
        
        ##---Lables on window---##
        self.Username = Label(self.master,text = "Username:")
        self.Username.place(x=0, y=130)
        
        self.Password = Label(self.master,text = "Password:")
        self.Password.place(x=0, y=160)
        
        self.Name = Label(self.master,text = "Name:")
        self.Name.place(x=0, y=190)
        
        self.Email = Label(self.master,text = "Email:")
        self.Email.place(x=0, y=220)
        
        self.Age = Label(self.master,text = "Age:")
        self.Age.place(x=0, y=250)
        
        self.AdminCode = Label(self.master,text = "Admin code:")
        self.AdminCode.place(x=0, y=280)

        self.AccountDeltails= Label(self.master,text = "Enter account detailes:")
        self.AccountDeltails.place(x=0, y=100)
        
        ##---Logo---##
        photo = PhotoImage(file = "Company logo.png")
        self.Logo = Label(master, image = photo)
        self.Logo.image = photo
        self.Logo.place(x=40, y=40)

        ##---Input boxs for Username---##
        self.UsernameInput = Entry(self.master, bd=3)
        self.UsernameInput.place(x=75, y=130)
        ##---Input boxs for Password---##
        self.PasswordInput = Entry(self.master, bd=3, show="*")
        self.PasswordInput.place(x=75, y=160)
        ##---Input boxs for First name---##
        self.NameInput = Entry(self.master, bd=3,)
        self.NameInput.place(x=75, y=190)
        ##---Input boxs for Email---##
        self.EmailInput = Entry(self.master, bd=3,)
        self.EmailInput.place(x=75, y=220)
        ##---Input boxs for Age--##
        self.AgeInput = Entry(self.master, bd=3,)
        self.AgeInput.place(x=75, y=250)

        ##---Close page button---##
        self.ClosePageB = Button(self.master, text = "Return to login", foreground = "red", command = self.CreateAccountConfirmExit)
        self.ClosePageB.place(x=215, y=310)
        ##---Create account button---##
        self.Sign_inB = Button(self.master, text = "Create account", command = self.InputValidation)
        self.Sign_inB.place(x=215, y=140)
        ##---Amin account tick boxes---##
        self.AdminAccountTickBox = Checkbutton(self.master,command = self.AdminEnteryOption)
        self.AdminAccountTickBox.place(x=70, y=280)

        ##---Class veriables---##
        self.AdminAccountChosen = 0
        self.AccountCreated = False

    def CreateAccountConfirmExit(self):##---Checks with the user if they want quit the application---##
        ConfirmExit = askyesno("Close page", "Do you want to return to the login page?")
        if ConfirmExit == True:
            self.master.destroy()

    def AdminEnteryOption(self):##---Gives the user the option is enter the admin code---##
        self.AdminAccountChosen = 1
        self.AdminAccountTickBox.destroy()

        #Input for Admin code
        self.AdminCodeInput = Entry(self.master, bd=3,)
        self.AdminCodeInput.place(x=75, y=280)
        

    def InputValidation(self):##---Checks if the the user inputs are correct---##
        Username = self.UsernameInput.get()
        Password = self.PasswordInput.get()
        Name = self.NameInput.get()
        Email = self.EmailInput.get()
        Age = self.AgeInput.get()
        AdminChosen = self.AdminAccountChosen
        if AdminChosen == 1:
            AdminInput = self.AdminCodeInput.get()
        
        if Name == "" or Email == "" or Username == "" or Password == "" or Age == "" :
            self.CreateAccountInputBoxFullWarning = Label(self.master, text = "Username is taken", foreground = "red")
            self.CreateAccountInputBoxFullWarning.place(x=125,y=100)
            
        elif AdminChosen == 1 and AdminInput == "":
            self.CreateAccountInputBoxFullWarning2 = Label(self.master, text = "Fill all entry boxes", foreground = "red")
            self.CreateAccountInputBoxFullWarning2.place(x=125,y=100)
            
        elif len(Username) <6:
            self.CreateAccountUsernameWarning = Label(self.master, text = "Minimum 6 characters for username", foreground = "red")
            self.CreateAccountUsernameWarning.place(x=125, y=100)
                
        elif len(Password) <6:
            self.CreateAccountPasswordWarning = Label(self.master, text = "Minimum 6 characters for password", foreground = "red")
            self.CreateAccountPasswordWarning.place(x=125, y=100)

        elif "@" in Email == False:
            self.CreateAccountEmailWarning = Label(self.master, text = "Email not valid", foreground = "red")
            self.CreateAccountEmailWarning.place(x=125, y=100)

        elif Age.isnumeric() == False:
            self.CreateAccountAgeWarning = Label(self.master, text = "Age should only consist of numbers", foreground = "red")
            self.CreateAccountAgeWarning.place(x=125, y=100)

        elif AdminChosen == 1 and AdminInput != "EGTHM06":
            self.CreateAccountAdminCodeWarning = Label(self.master, text = "Admin code is incorrect", foreground = "red")
            self.CreateAccountAdminCodeWarning.place(x=125, y=100)
                         
        elif self.CheckAccuntDetailsTaken(Username) == True:
            self.CreateAccountDetailsTakenWarning = Label(self.master, text = "Username is taken", foreground = "red")
            self.CreateAccountDetailsTakenWarning.place(x=125, y=100)

        else:
            self.SaveAccountDetails(Username, Password, Name, Email, Age)
            
                            
    def CheckAccuntDetailsTaken(self, Username):##---Checks if the username is taken---## 
        cursor.execute("SELECT Username FROM User WHERE Username = (?)", (Username,))
        conn.commit()
        DatabaseVaue = cursor.fetchall()
        if len(DatabaseVaue) == 1:
            return True


    def SaveAccountDetails(self, Username, Password, Name, Email, Age):##---Saves account details to the database---##
        EncryptedPassword = self.Encryption(Password)
        cursor.execute("INSERT INTO User(Name, Email, Age, Admin, Username, Password) VALUES (?, ?, ?, ?, ?, ?)", (Name, Email, Age, self.AdminAccountChosen, Username, EncryptedPassword))
        conn.commit()
        Login_Window.AccountHasBeenCreated()
        self.master.destroy()

    def Encryption(self, OriginalValue):##---Used to encrypt the password before it is saved to the data base---##
      EncryptedString = ""
      shift = 5
      for ch in OriginalValue:
        Value = ord(ch) + shift
        FinalValue = chr(Value)
        EncryptedString += FinalValue
      return EncryptedString 

class Main_Window():
    def __init__(self,master):
       ##---creating window---##
        self.master = master
        self.master.geometry("880x520")
        self.master.title("Home page")

        ##---Values uesd for methords---##
        self.HTLcheckbox_var = BooleanVar()
        self.LTHcheckbox_var = BooleanVar()
        self.ApplicantDetailsList = []
        
        ##---Lables on window---##
        self.Search = Label(self.master,text = "Search:")
        self.Search.place(x=185, y=265)

        self.CurrentUserLogedIn = Label(self.master, text = "Loged in as:")
        self.CurrentUserLogedIn.place(x=0, y=10)

        self.UserName = Label(self.master, text = self.GetUserName())
        self.UserName.place(x=70, y=10)

        self.ApplicationName = Label(self.master, text = "OPTIMAL JOB", font=('Times', 20))
        self.ApplicationName.place(x=320, y=0)
                                        
        ##---Input box---##
        self.SearchInput = Entry(self.master,width = 20, bd=3)
        self.SearchInput.place(x=250, y=265)
        
        ##---Upload job button---##
        self.AddJobB = Button(self.master, text = "Upload job",height=2, width=13, command = self.GoToUploadJob)
        self.AddJobB.place(x=180, y=410)
        ##---View applicat button---##
        self.ViewJobB = Button(self.master, text = "View applicants'",height=2, width=13, command = self.ShowApplicants)
        self.ViewJobB.place(x=290, y=310)
        ##---Delete job button---##
        self.DeleteJobB = Button(self.master, text = "Delete job",height=2, width=13, command = self.DeleteJobCommand)
        self.DeleteJobB.place(x=290, y=410) 
        ##---Favourite job button---##
        self.FavouriteJobB = Button(self.master, text = "Favourite job",height=2, width=13, command = self.FavouriteJob)
        self.FavouriteJobB.place(x=180, y=360)        
        ##---Apply to job button---##
        self.AddJobB = Button(self.master, text = "Apply to job",height=2, width=13, command = self.ApplyToJob)
        self.AddJobB.place(x=180, y=310)
        ##---Show Favourites button---##
        self.FavouriteJobB = Button(self.master, text = "View favourites'",height=2, width=13, command = self.ShowFavouriteJobs)
        self.FavouriteJobB.place(x=290, y=360)     
        ##---Quit button---##
        self.Quit = Button(self.master, text = "Return to login",height=2, width=13, foreground = "red", command = self.MainPageExit) 
        self.Quit.place(x=15, y=460)
        ##---Filter button---##
        self.DropDownB = Button(self.master, text = "Filter",height=2, width=13, command = self.Filter)
        self.DropDownB.place(x=15, y=360)
        ##---Refresh tree view button---##
        self.RefreshTree = Button(self.master, text = "Refresh tree",height=2, width=13, command = self.RefreshTree)
        self.RefreshTree.place(x=290, y=460)
        ##---View Extrainformation button---##
        self.ShowExtraInformation = Button(self.master, text = "Extra information",height=2, width=13, command = self.DisplayExtrainformation)
        self.ShowExtraInformation.place(x=180, y=460)
        ##---Save applicants button---##
        self.SaveApplicants = Button(self.master, text = "Save applicants",height=2, width=13, command = self.SaveApplicantsToFile)
        self.SaveApplicants.place(x=15, y=410)
        
        ##---Highest to lowerst tick boxes---##
        self.HighToLowTickBox = Checkbutton(self.master, text="Highest to lowerst", variable = self.HTLcheckbox_var)
        self.HighToLowTickBox.place(x=15, y=305)
        ##---Lowest to highest tick boxes---##
        self.LowToHighTickBox = Checkbutton(self.master, text = "Lowest to highest", variable = self.LTHcheckbox_var)
        self.LowToHighTickBox.place(x=15, y=325)
        
        ##---Options for dropdown---##
        OPTIONS = [
        'Company name',
        'Age requirement',
        'Location (postcode)',
        'Hours',
        'Pay (per hour)'
        ]

        ##---Creation of the dropdown---##
        self.MainPageDropdown = StringVar(master)
        self.MainPageDropdown.set("Filter")
        self.DropDown = OptionMenu(master, self.MainPageDropdown, *OPTIONS)
        self.DropDown.place(x=15, y=275)
        
        
        ##---The "Main" tree view---##
        # The "Main" tree being declared 
        self.MainTree = ttk.Treeview(self.master,)
        
        # Adding columns to the "Main" tree view 
        self.MainTree["columns"] = ("0", "1", "2","3","4","5")
        self.MainTree.column("#0", anchor = W, width = 120)
        self.MainTree.column("#1", anchor = W, width = 120)
        self.MainTree.column("#2", anchor = W, width = 80)
        self.MainTree.column("#3", anchor = W, width = 80)
        self.MainTree.column("#4", anchor = W, width = 80)
        self.MainTree.column("#5", anchor = W, width = 80)
        self.MainTree.column("#6", anchor = W, width = 280)
        
        # Setting the column headers for the "Main" tree view
        self.MainTree.heading("#0", text="Company name")
        self.MainTree.heading("#1", text="Job title")
        self.MainTree.heading("#2", text="Location")
        self.MainTree.heading("#3", text="Hours")
        self.MainTree.heading("#4", text="Pay")
        self.MainTree.heading("#5", text="Age")
        self.MainTree.heading("#6", text="Job description")

        # Creating the "Main" tree scrollbar
        self.scrollbar = Scrollbar(self.master, orient="vertical", command=self.MainTree.yview) 
        self.MainTree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=845, y=30, height=225)
        
        # Placing the "Main" tree view on the window
        self.MainTree.place(x=0, y=30)

        ##---Adding data to Main tree---##
        self.AddindDataToMainTree()

        ##---Calling the "SecondaryTreeView" methord to make the "Secondary" tree---##
        self.SecTree = self.SecondaryTreeView(0)


    def SecondaryTreeView(self, SecTOption):##---Creates and adding data to the "Secondary" tree view---##
        # The "Secondary" tree being declared 
        SecondaryTree = ttk.Treeview(self.master,)
        
        # Add columns to the "Secondary" tree view 
        SecondaryTree["columns"] = ("0", "1")
        SecondaryTree.column("#0", anchor = W, width = 145)
        SecondaryTree.column("#1", anchor = W, width = 145)
        SecondaryTree.column("#2", anchor = W, width = 145)

        # Setting the column headers for the "Secondary" tree
        if SecTOption == 0:
            SecondaryTree.heading("#0", text= "")
            SecondaryTree.heading("#1", text= "")
            SecondaryTree.heading("#2", text= "")
            
        elif SecTOption == 1:
            SecondaryTree.heading("#0", text= "Job title")
            SecondaryTree.heading("#1", text= "Company name")
            SecondaryTree.heading("#2", text= "Job description")

        elif SecTOption == 2:
            SecondaryTree.heading("#0", text= "Job title")
            SecondaryTree.heading("#1", text= "Applicant name")
            SecondaryTree.heading("#2", text= "Contact details")


        # Creating the scrollbar for the "Secondary" tree
        Secondaryscrollbar = Scrollbar(self.master, orient="vertical", command=SecondaryTree.yview)
        SecondaryTree.configure(yscroll=Secondaryscrollbar.set)
        Secondaryscrollbar.place(x=845, y=275, height=225)

        
        # Placing the "Secondary" tree view on the window
        SecondaryTree.place(x=405, y = 275)

        # Adding data to the "Secondary" tree
        if SecTOption == 1:
            try:
                for row in self.SecondaryTree.get_children():
                    self.SecondaryTree.delete(row)
            except:
                pass
            
            try:
                cursor.execute("SELECT FavouriteID FROM Favourites WHERE UserID = (?)", (UserID,))
                Jobs = cursor.fetchall()
                NumberOfJobs = len(Jobs)
            
                cursor.execute("SELECT JobID FROM Favourites WHERE UserID = (?)", (UserID,))
                conn.commit()
                value = cursor.fetchall()

                for i in range (0,NumberOfJobs):
                  value_JobId = value[i][0]
                  cursor.execute("SELECT JobTitle, CompanyName, JobDescription FROM Job WHERE JobID = (?)", (value_JobId,))
                  conn.commit()
                  values = cursor.fetchall()
              
                  for row in values:
                      SecondaryTree.insert("",0,text=row[0], values=(row[1],row[2]))
                    
            except:
                pass
            
        elif SecTOption == 2: 
            try:
                for row in self.SecondaryTree.get_children():
                    SecondaryTree.delete(row)
            except:
                pass
            
            try:
                cursor.execute("SELECT ApplicantID FROM Applicants WHERE UserID = (?)", (UserID,))
                Jobs = cursor.fetchall()
                NumberOfJobs = len(Jobs)
            
                cursor.execute("SELECT JobID FROM Applicants WHERE UserID = (?)", (UserID,))
                conn.commit()
                value = cursor.fetchall()

                for i in range (0,NumberOfJobs):
                  value_JobId = value[i][0]

                  cursor.execute("""SELECT Job.JobTitle, User.Name, User.Email
                                    FROM  Job
                                    INNER JOIN User ON User.UserID = Job.UserID
                                    WHERE JobID = (?)""", (value_JobId,))
                  conn.commit()
                  values = cursor.fetchall()

                  try:
                      ApplicantDetails = (values[0][0] + " ",values[0][1] + "  ",values[0][2] + "   "+ "\n")
                      self.ApplicantDetailsList.append(ApplicantDetails)

                  except:
                      pass

                  for row in values:
                      SecondaryTree.insert("",0,text=row[0], values=(row[1],row[2]))
                    
            except:
                pass
        return SecondaryTree
        
    def GetUserName(self):##---Finds the name of the user that is currnly logged in---##
        cursor.execute("SELECT Name FROM User WHERE UserID = (?)", (UserID,))
        conn.commit()
        DatabaseVaue = cursor.fetchall()
        return DatabaseVaue

    def Filter(self):##---Filters what data is being recived from the database or the way data is is displayed---## 
        if self.HTLcheckbox_var == True and self.LTHcheckbox_var == True:
            self.MainTickWarning = Label(self.master, text = "Only a single filter option can be selected", foreground = "red")                                           
            self.MainTickWarning.place(x=185, y=290)

        else:
            DropDownOption = self.MainPageDropdown.get()

        
    def GoToUploadJob(self):##---Open/call the "Upload Job" page---##
        root5 = Toplevel(self.master)
        GUI = Upload_Job_Window(root5)

    def AddindDataToMainTree(self):##---Adds data to the "Main" tree--##
        try:
            cursor.execute("SELECT MAX(JobID) FROM Job")
            NumberOfJobs = cursor.fetchall()
            for i in NumberOfJobs:
                NumberOfJobIDs = (i[0]+1)

            for i in range (1,NumberOfJobIDs):
              cursor.execute("SELECT CompanyName, JobTitle, Location, Hours , Pay, Age, JobDescription, JobID FROM Job WHERE jobID = (?)", (i,))
              conn.commit()
              value = cursor.fetchall()
              for row in value:
                  self.MainTree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7]))

        except:
            pass

    def RefreshTree(self):##---Redisplays the data on the main tree---## 
        self.AddindDataToMainTree()

    def SelectedJob(self):##---Gathers the job which the user has selected on the "Main" tree---## 
        try:
            curItem = self.MainTree.focus()
            Selected = self.MainTree.item(curItem)
            value = Selected.get("values")
            JobID = value[6]
            return JobID
        
        except:
            self.MainTickWarning = Label(self.master,  text = "Job has not been selected", foreground = "red")                                           
            self.MainTickWarning.place(x=180, y=290)
         

    def DeleteJobCommand(self):##---Deletes the job the user has selected---##
        AdminCheck = self.CheckIfAdmin()
        Selected = self.SelectedJob()

        cursor.execute("SELECT UserID FROM Job WHERE jobID = (?)", (Selected,))
        conn.commit()
        DataValue = cursor.fetchall()
        
        if AdminCheck == 1 or DataValue[0][0] == UserID:
            cursor.execute("DELETE FROM job WHERE JobID = (?)", (Selected,))
            cursor.execute("DELETE FROM Favourites WHERE JobID = (?)", (Selected,))
            cursor.execute("DELETE FROM Applicants WHERE JobID = (?)", (Selected,))
            conn.commit            

            selected_job = self.MainTree.selection()[0]
            self.MainTree.delete(selected_job)

        else:
            self.DeleteWarning.Label(self.master, text = "This is not your job lising.")
            self.DeleteWarning.place(x=100, y=100)
            
    def ShowFavouriteJobs(self):##---Displays the users favourites on the "Secondary" tree---##
        self.SecondaryTreeView(1)

    def ShowApplicants(self):##---Displays the users favourites on the "Secondary" tree---##
        self.SecondaryTreeView(2)
        
    def FavouriteJob(self):##---Favourite the job which has been selected by the user---##
        Selected = self.SelectedJob()
        cursor.execute("INSERT INTO Favourites(UserID, JobID) VALUES (?, ?)", (UserID, Selected,))
        conn.commit()

    def ApplyToJob(self):##---Apply the job which has been selected by the user---##
        Selected = self.SelectedJob()
        cursor.execute("INSERT INTO Applicants(UserID, JobID) VALUES (?, ?)", (UserID, Selected,))
        conn.commit()

    def DisplayExtrainformation(self):##---Displayes the extra information which the user has selected---##
        Selected = self.SelectedJob()
        cursor.execute("SELECT ExtraInformation FROM Job WHERE jobID = (?)", (Selected,))
        conn.commit()
        value = cursor.fetchall()
        showinfo(title = "Extra Information", message = (value[0][0]))

    def JobHasBeenCreated(self):##---Informs the user that job has been created---##
        Main_Window.JobHasBeenMade = Label(self.master, text = "Your job listing has been created")
        Main_Window.JobHasBeenMade.place(x=185, y=290)

    def CheckIfAdmin(self):
        cursor.execute("SELECT Admin FROM User WHERE UserID = (?)", (UserID,))
        conn.commit()
        DatabaseVaue = cursor.fetchall()
        return DatabaseVaue[0][0]
    
    def MainPageExit(self):##---Checks with the user if they want quit---##
        ConfirmExit = askyesno("Closing page","Do you want to return to the login page?")
        if ConfirmExit == True:
            self.master.destroy()

    def SaveApplicantsToFile(self):
        FileName = "Applicants.txt"
        file = open(FileName, "w")
        for i in range (0,len(self.ApplicantDetailsList)):
            file.writelines(self.ApplicantDetailsList[i])
        file.close
    
class Upload_Job_Window():
    def __init__(self, master):
        ##---creating window---##
        self.master = master
        self.master.geometry("270x300")
        self.master.title("Upload a job")
        
        ##---Variables---##
        self.ExtraInformationSelected = 0

        ##---Lables on window---##
        self.EnterDetails = Label(self.master, text = "Enter job details:")
        self.EnterDetails.place(x=0, y=0)
        
        self.CompanyName = Label(self.master,text = "Company name:")
        self.CompanyName.place(x=0, y=25)
        
        self.JobTitle = Label(self.master,text = "Job title:")
        self.JobTitle.place(x=0, y=55)
        
        self.AgeRequirement = Label(self.master,text = "Age requirement:")
        self.AgeRequirement.place(x=0, y=85)
        
        self.Location = Label(self.master,text = "Location (postcode):")
        self.Location.place(x=0, y=115)
        
        self.Hours = Label(self.master,text = "Hours:")
        self.Hours.place(x=0, y=145)
        
        self.Pay = Label(self.master,text = "Pay (per hour):")
        self.Pay.place(x=0, y=175)
        
        self.JobDescription = Label(self.master,text = "Job description:")
        self.JobDescription.place(x=0, y=205)
        
        self.ExtraInformation = Label(self.master, text = "Extra information:")
        self.ExtraInformation.place(x=0, y=235)

        ##---Input boxs for Company name---##
        self.CompanyNameInput = Entry(self.master, bd=3)
        self.CompanyNameInput.place(x=115, y=25)
        ##---Input boxs for Job title---##
        self.JobTitleInput = Entry(self.master, bd=3)
        self.JobTitleInput.place(x=115, y=55)
        ##---Input boxs for Age requirement---##
        self.AgeRequirementInput = Entry(self.master, bd=3)
        self.AgeRequirementInput.place(x=115, y=85)
        ##---Input boxs for Location---##
        self.LocationInput = Entry(self.master, bd=3)
        self.LocationInput.place(x=115, y=115)
        ##---Input boxs for Hours---##
        self.HoursInput = Entry(self.master, bd=3)
        self.HoursInput.place(x=115, y=145)
        ##---Input boxs for Pay---##
        self.PayInput = Entry(self.master, bd=3)
        self.PayInput.place(x=115, y=175)
        ##---Input boxs for Job description---##
        self.JobDescriptionInput = Entry(self.master, bd=3)
        self.JobDescriptionInput.place(x=115, y=205)

        ##---Upload job button---##
        self.UploasdJobB = Button(self.master, text = "Upload job", command = self.InputValidation)
        self.UploasdJobB.place(x=115, y=270)
        ##---Close page button---##
        self.ClosePageB = Button(self.master, text = "Close page", foreground="red", command = self.master.destroy)
        self.ClosePageB.place(x=195, y=270)

        ##---Extra infermation tick boxes---##
        self.ExtraInformtionTickBox = Checkbutton(self.master,command = self.ExtraInformationEnteryOption)
        self.ExtraInformtionTickBox.place(x=110, y=235)
        
    def InputValidation(self):##---Checks if the the user inputs are correct---##
        CompanyName = self.CompanyNameInput.get()
        JobTitle = self.JobTitleInput.get()
        AgeRequirement = self.AgeRequirementInput.get()
        Location = self.LocationInput.get()
        Hours = self.HoursInput.get()
        Pay = self.PayInput.get()
        JobDescription = self.JobDescriptionInput.get()
        if self.ExtraInformationSelected == 1:
            self.ExtraInformation = self.ExtraInformationInput.get()


        if CompanyName == "" or JobTitle == "" or AgeRequirement == "" or Location == "" or Hours == "" or Pay == "" or JobDescription == "":
            self.MainPageCreateAccountWarning = Label(self.master, text = "£ is not needed for Pay", foreground = "red")
            self.MainPageCreateAccountWarning.place(x=90,y=0)
            
        elif self.ExtraInformationSelected == 1 and self.ExtraInformation == "":
            self.MainPageExtraInformationSelectedWarning = Label(self.master, text = "Fill all entry boxes", foreground = "red")
            self.MainPageExtraInformationSelectedWarning.place(x=90, y=0)
            
        elif AgeRequirement.isnumeric() == False:
            self.MainPageUploadJobAgeRequirementWarning = Label(self.master, text = "Use numbers only for age", foreground = "red")
            self.MainPageUploadJobAgeRequirementWarning.place(x=90, y=0)

        elif " " in Location:
            self.MainPageUploadLocationWarning = Label(self.master, text = "postcode shouldn't have a space", foreground = "red")
            self.MainPageUploadLocationWarning.place(x=90, y=0)

        elif Hours.isnumeric() == False: 
            self.MainPageUploadHoursWarning = Label(self.master, text = "Use numbers only for hours", foreground = "red")
            self.MainPageUploadHoursWarning.place(x=90, y=0)

        elif "£" in Pay: 
            self.MainPageUploadPayWarning = Label(self.master, text = "£ is not needed for Pay", foreground = "red")
            self.MainPageUploadPayWarning.place(x=115, y=0)

        elif Pay.isnumeric() == False: 
            self.MainPageUploadPayWarning2 = Label(self.master, text = "Use numbers only for pay", foreground = "red")
            self.MainPageUploadPayWarning2.place(x=115, y=0)

        else:
            self.UploadJob(CompanyName, JobTitle, AgeRequirement, Location, Hours, Pay, JobDescription)

        
    def UploadJob(self, CompanyName, JobTitle, AgeRequirement, Location, Hours, Pay, JobDescription):##---Saves job information to the database---##
        if self.ExtraInformationSelected == 1:
            EInformation = self.GetExtraInformation()
        else:
            EInformation = "NULL"

        cursor.execute("INSERT INTO Job(CompanyName, JobTitle, Location, Hours, Pay, Age, JobDescription, ExtraInformation, UserID) VALUES (?, ?, ?, ?, ?, ? ,? ,? ,?)", (CompanyName, JobTitle, Location, Hours, Pay, AgeRequirement, JobDescription, EInformation, UserID))
        conn.commit()
        
        Main_Window.JobHasBeenCreated(self.master)
        self.master.destroy()

    def ExtraInformationEnteryOption(self):##---Gives the user the option is enter the extra information---##
        self.ExtraInformationSelected = 1 
        self.ExtraInformtionTickBox.destroy()
        
        # Input boxs for Extra information:
        self.ExtraInformationInput = Entry(self.master, bd=3)
        self.ExtraInformationInput.place(x=115, y=235)


    def GetExtraInformation(self):##---Gets the entry in the extra inforation input box---##
        return self.ExtraInformationInput.get()
        
def main():
    root = Tk()
    app = Login_Window(root)
    root.mainloop()

if __name__=="__main__":
    main()
    
