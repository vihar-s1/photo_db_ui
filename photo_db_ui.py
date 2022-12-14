import psycopg2
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PIL.ImageTk import PhotoImage
import requests

DATABASE = 'db_project'
USER = "postgres"
PASSWORD = "admin"
HOST = "127.0.0.1"
PORT = "5432"
CONN = None 
CURSOR = None


PADX, PADY = 5, 5
FONT = ('courier new', 12, 'bold')
FONT_HEADER = ('courier new', 20, 'bold')
FRAME_BG = '#808080'
BUTTON_BG, BUTTON_FG = '#000000', '#ffffff'
CELL_BG = ('#707070', "#b0b0b0")
ROOT_W, ROOT_H = 1000, 700


def CONNECT():
    global CONN, CURSOR
    try:
        CONN = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        CURSOR = CONN.cursor()
        return True
    except:
        return False

class FrontEnd:
    def __init__(self, rootWin: tk.Tk) -> None:
        self.__root = rootWin
        self.__root.geometry(f"{ROOT_W}x{ROOT_H}")
        self.__root.config(bg=FRAME_BG)
        
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        self.__mainFrame = tk.Frame(self.__root, padx=12*PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        tk.Label(self.__headerFrame, text="Connect To Database", font=FONT_HEADER, bg=FRAME_BG).grid()
        
        tk.Label(self.__mainFrame, text="HOST", font=FONT, bg=FRAME_BG).grid(padx=PADX, pady=PADY, row=0, column=0)
        self.__db_ip = tk.Text(self.__mainFrame, height=2, width=30)
        self.__db_ip.grid(row=0, column=1, padx=PADX, pady=PADY)
        
        tk.Label(self.__mainFrame, text="PORT", font=FONT, bg=FRAME_BG).grid(padx=PADX, pady=PADY, row=1, column=0)
        self.__db_port = tk.Text(self.__mainFrame, height=2, width=30)
        self.__db_port.grid(row=1, column=1, padx=PADX, pady=PADY)
        
        connectButton = tk.Button(self.__mainFrame, text="Connect", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, padx=PADX)
        connectButton.bind("<Button-1>", self.__connectWrapper(True) )
        connectButton.grid(row=2, column=0, padx=PADX, pady=PADY)
        
        defaultButton = tk.Button(self.__mainFrame, text="Default", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, padx=PADX)
        defaultButton.bind("<Button-1>", self.__connectWrapper(False) )
        defaultButton.grid(row=2, column=1, padx=PADX, pady=PADY)
    
    
    def __connectWrapper(self, manualHOST):
        return lambda Button: self.__connect(manualHOST)
        
    def __connect(self, manualHOST: bool):
        global HOST, PORT
        if manualHOST:
            host = self.__db_ip.get(1.0, 'end-1c')
            port = self.__db_port.get(1.0, 'end-1c')
        else:
            host, port = HOST, PORT
        
        if not CONNECT():
            messagebox.showerror('Connection Error', f'Could not connect to the database:({DATABASE}) on {host}:{port} !!')
            return
        else:
            messagebox.showinfo('Connection Successful', f'Connected to the database:({DATABASE}) on {host}:{port} !!')
            HOST = host
            PORT = port
        
        self.__mainWindow()
        
    
    def __mainWindow(self):
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, bg=FRAME_BG, padx=PADX, pady=PADY)
        self.__headerFrame.pack()
        self.__mainFrame = tk.Frame(self.__root, bg=FRAME_BG, padx=12*PADX, pady=PADY)
        self.__mainFrame.pack()
        
        tk.Label(self.__headerFrame, text="Main Window", padx=PADX, pady=PADY, font=FONT_HEADER, bg=FRAME_BG
            ).grid(row=0, column=0)

        tk.Button(self.__mainFrame, text="user login", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__userLogin
                  ).grid(row=0, column=0 ,padx=PADX, pady=PADY)
        
        tk.Button(self.__mainFrame, text="admin login", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__adminLogin
                  ).grid(row=1, column=0,padx=PADX, pady=PADY)
    
    
    def __logout(self):
        try:
            self.__loggedInAdmin.clear()
        except:
            try:
                self.__loggedInUser.clear()
            except:
                pass
        self.__mainWindow()
       
       
    def __adminLogin(self):
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        
        tk.Label(self.__headerFrame, text="Admin Login Page", padx=PADX, pady=PADY, font=FONT_HEADER, bg=FRAME_BG
            ).grid(row=0, column=0)
        
        self.__mainFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        tk.Label(
            self.__mainFrame, text='Username / Email ID', padx=PADX, pady=PADY, font=FONT, bg=FRAME_BG
            ).grid(row=0, column=0, padx=PADX, pady=PADY)
        
        self.__loginID = tk.Text(self.__mainFrame, height=2, width=30)
        self.__loginID.grid(row=0, column=1, padx=PADX, pady=PADY)
        
        tk.Label(
            self.__mainFrame, text='password', padx=PADX, pady=PADY, font=FONT, bg=FRAME_BG
            ).grid(row=1, column=0, padx=PADX, pady=PADY)
    
        self.__password = tk.Text(self.__mainFrame, height=2, width=30)
        self.__password.grid(row=1, column=1, padx=PADX, pady=PADY)
        
        tk.Button(self.__mainFrame, text="Back", font=FONT, padx=PADX, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__logout
                  ).grid(row=2, column=0, padx=PADX, pady=PADY)
        
        tk.Button(self.__mainFrame, text="Login", font=FONT, padx=PADX, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__adminVerify
                  ).grid(row=2, column=1, padx=PADX, pady=PADY)
     
    
    def __adminVerify(self):
        loginID = self.__loginID.get(1.0, 'end-1c').strip()
        password = self.__password.get(1.0, 'end-1c').strip()
        
        CURSOR.execute(
            f'''SELECT * FROM photo_db.t_admin 
                WHERE ("email_id" LIKE \'{loginID}\' OR "username" LIKE \'{loginID}\') AND "password" LIKE \'{password}\'
                ''')
        
        data = CURSOR.fetchall()
        if not data:
            messagebox.showwarning('Warning', 'No Data Found!!')
        elif len(data) > 1:
            messagebox.showerror('Invalid Query Acessing', 'Multiple Entries Returned!! Enter Proper Information')
        else:
            data = data[0]
            self.__loggedInAdmin = {'email':data[0], 'username':data[1], 'first_name':data[2], 'last_name':data[3]}
            self.__setUpAdmin()
            
            
    def __setUpAdmin(self):
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        
        tk.Label(self.__headerFrame, text=f"Welcome {self.__loggedInAdmin['first_name']}", font=FONT_HEADER, bg=FRAME_BG).grid()
        
        tk.Button(self.__headerFrame, text="log out", font=FONT, padx=PADX, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__logout
                  ).grid(row=0, column=1)
        
        self.__mainFrame = tk.Frame(self.__root, padx=10*PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        tk.Button(self.__mainFrame, text="Check Subscription Plans", 
                                            font=FONT, padx=PADX, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__subscriptionPlans
                    ).grid(row=0, column=0, padx=PADX, pady=PADY)
        
    
    def __userLogin(self):
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        
        tk.Label(self.__headerFrame, text="User Login Page", padx=PADX, pady=PADY, font=FONT_HEADER, bg=FRAME_BG
            ).grid(row=0, column=0)
        
        self.__mainFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        tk.Label(
            self.__mainFrame, text='Username / Email ID', padx=PADX, pady=PADY, font=FONT, bg=FRAME_BG
            ).grid(row=0, column=0, padx=PADX, pady=PADY)
        
        self.__loginID = tk.Text(self.__mainFrame, height=2, width=30)
        self.__loginID.grid(row=0, column=1, padx=PADX, pady=PADY)
        
        tk.Label(
            self.__mainFrame, text='password', padx=PADX, pady=PADY, font=FONT, bg=FRAME_BG
            ).grid(row=1, column=0, padx=PADX, pady=PADY)
    
        self.__password = tk.Text(self.__mainFrame, height=2, width=30)
        self.__password.grid(row=1, column=1, padx=PADX, pady=PADY)
        
        tk.Button(self.__mainFrame, text="Back", font=FONT, padx=PADX, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__logout
                  ).grid(row=2, column=0, padx=PADX, pady=PADY)
        tk.Button(self.__mainFrame, text="Login", font=FONT, padx=PADX, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__userVerify
                  ).grid(row=2, column=1, padx=PADX, pady=PADY)
     
    
    def __userVerify(self):
        loginID = self.__loginID.get(1.0, 'end-1c').strip()
        password = self.__password.get(1.0, 'end-1c').strip()
        
        CURSOR.execute(
            f'''SELECT * FROM photo_db.t_users
                WHERE ("email_id" LIKE \'{loginID}\' OR "username" LIKE \'{loginID}\') AND "password" LIKE \'{password}\'
                ''')
        
        data = CURSOR.fetchall()
        if not data:
            messagebox.showwarning('Warning', 'No Data Found!!')
        elif len(data) > 1:
            messagebox.showerror('Invalid Query Acessing', 'Multiple Entries Returned!! Enter Proper Information')
        else:
            data = data[0]            
            self.__loggedInUser = {'email':data[0], 'username':data[1], 'first_name':data[2], 'last_name':data[3], 'plan_id':data[5]}
            
            CURSOR.execute(f'''SELECT T2."user_types"
                            FROM photo_db.t_subscription_plan T1
                            INNER JOIN photo_db.t_plan_type T2   
                            ON T1."plan_type" = T2."type_code" AND T1."plan_id" = {self.__loggedInUser['plan_id']}
                            ''')
            self.__user_style = CURSOR.fetchall()[0][0]
            self.__setUpUser()
                        
            
    def __setUpUser(self):
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        
        tk.Label(self.__headerFrame, text=f"Welcome {self.__loggedInUser['first_name']}", font=FONT_HEADER, bg=FRAME_BG).grid()
        
        tk.Button(self.__headerFrame, text="log out", font=FONT, padx=PADX, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__logout
                  ).grid(row=0, column=1)
        
        self.__mainFrame = tk.Frame(self.__root, padx=10*PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        if self.__user_style == 'photographers':
            CURSOR.execute(f"""
                           SELECT "image_id","image" 
                           FROM photo_db.t_image 
                           WHERE "owner" LIKE '{self.__loggedInUser['email']}'
                               AND "image_id" NOT IN (SELECT "image_id" FROM photo_db.t_recycle_bin);
                           """)
            data = CURSOR.fetchall()

            for i in range(len(data)):
                    button = tk.Button(self.__mainFrame, text=data[i][1], padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG)
                    button.bind("<Button-1>", self.__openLinkWrapper(1, data[i][1]))
                    button.grid(row=i, column=0, columnspan=2, padx=PADX, pady=PADY)
                    buttonDel = tk.Button(self.__mainFrame, text="Delete", padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG)
                    buttonDel.bind("<Button-1>", self.__deleteImageWrapper(data[i][0]))
                    buttonDel.grid(row=i, column=2, padx=PADX, pady=PADY)
                    
            tk.Button(self.__mainFrame, text="Insert Image", padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__insertImage
                      ).grid(row=len(data), column=0)
            tk.Button(self.__mainFrame, text="Check Bin", padx=PADX, font=FONT, bg=BUTTON_BG, fg= BUTTON_FG, command=self.__checkBin
                      ).grid(row=len(data), column=1)
                            
        elif self.__user_style == 'designers':
            CURSOR.execute(f"""SELECT T1.\"album_id\", T1.\"album_name\"
                               FROM photo_db.t_albums T1 
                               NATURAL JOIN photo_db.t_designer_edits T2
                               WHERE T2.email_id LIKE '{self.__loggedInUser['email']}';""")
            data = CURSOR.fetchall()
            
            for i in range(len(data)):
                    button = tk.Button(self.__mainFrame, text=data[i][1], padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG)
                    button.bind("<Button-1>", self.__openAlbumWrapper(data[i][0]))
                    button.grid(row=i, column=0, padx=PADX, pady=PADY)
                
        else:
            if self.__user_style == 'combo plan':
                data = ['photographer', 'designer']
            else:
                data = ['viewer']
            tk.Label(self.__mainFrame, text= f"You are a {' and '.join(data)}.", font=FONT_HEADER, bg=FRAME_BG).grid(row=0, column=0)
            
        
    
    def __openLinkWrapper(self, commandID, link):
        return lambda Button: self.__openLink(commandID, link)
    
    def __openAlbumWrapper(self, link):
        return lambda Button: self.__openAlbum(link)
    
    def __deleteImageWrapper(self, image_id):
        return lambda Button: self.__deleteImage(image_id)
    
        
    def __openLink(self, commandID, link):
        response = requests.get(link)
        if response.status_code:
            with open('temp.png', 'wb') as fp:
                fp.write(response.content)
                fp.close()
                
            self.__headerFrame.destroy()
            self.__mainFrame.destroy()
            self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
            self.__headerFrame.pack()
            self.__mainFrame = tk.Frame(self.__root, padx=10*PADX, pady=PADY, bg=FRAME_BG)
            self.__mainFrame.pack()
        
        self.__displayImg = PhotoImage(Image.open('temp.png'))
        tk.Label(self.__headerFrame, text=link, font=FONT, bg=FRAME_BG).grid()
        tk.Label(self.__mainFrame, image=self.__displayImg).grid(row=0, column=0, padx=PADX, pady=PADY)
        if commandID == 1:
            tk.Button(self.__mainFrame, text="Back", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__setUpUser).grid(row=1, column=0, padx=PADX, pady=PADY)
        else: # commandID == 2
            tk.Button(self.__mainFrame, text="Back", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__checkBin).grid(row=1, column=0, padx=PADX, pady=PADY)
    
    
    def __openAlbum(self, link):
        CURSOR.execute(f"""
                        SELECT T2."image"
                        FROM  photo_db.t_album_contains T1
                        NATURAL JOIN photo_db.t_image T2
                        WHERE T1.album_id = {link}
                            """)
        data = CURSOR.fetchall()
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        self.__mainFrame = tk.Frame(self.__root, padx=10*PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        CURSOR.execute(f'SELECT "album_name" FROM photo_db.t_albums WHERE "album_id" = {link}')
        album_name = CURSOR.fetchone()[0]
        tk.Label(self.__headerFrame, text=f"Album: {album_name}", font=FONT_HEADER, bg=FRAME_BG).grid(padx=PADX, pady=PADY)
        
        for i in range(len(data)):
                button = tk.Button(self.__mainFrame, text=data[i][0], padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG)
                button.bind("<Button-1>", self.__openAlbumLinkWrapper(link, data[i][0]))
                button.grid(row=i, column=0, padx=PADX, pady=PADY)
        
        tk.Button(self.__mainFrame, text="Back", padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__setUpUser
                  ).grid(row=len(data), column=0, padx=PADX, pady=PADY)
        
    
    def __insertImage(self):
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        self.__mainFrame = tk.Frame(self.__root, padx=10*PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        tk.Label(self.__headerFrame, text="Insert New Image" , padx=PADX, font=FONT_HEADER, bg=FRAME_BG).grid()
        
        tk.Label(self.__mainFrame, text="Image URL", padx=PADX, font=FONT, bg=FRAME_BG).grid(row=0, column=0)
        self.__imageURL = tk.Text(self.__mainFrame, height=2, width=30)
        self.__imageURL.grid(row=0, column=1, columnspan=2, pady=PADY)
        
        tk.Label(self.__mainFrame, text="Location", padx=PADX, font=FONT, bg=FRAME_BG).grid(row=1, column=0)
        self.__location = tk.Text(self.__mainFrame, height=2, width=30)
        self.__location.grid(row=1, column=1, columnspan=2, pady=PADY)
        
        tk.Label(self.__mainFrame, text="Device Type", padx=PADX, font=FONT, bg=FRAME_BG).grid(row=2, column=0)
        self.__deviceType = tk.Text(self.__mainFrame, height=2, width=30)
        self.__deviceType.grid(row=2, column=1, columnspan=2, pady=PADY)
        
        tk.Label(self.__mainFrame, text="Visibility", padx=PADX, font=FONT, bg=FRAME_BG).grid(row=3, column=0)
        self.__visibility = tk.BooleanVar(self.__root)
        tk.Radiobutton(self.__mainFrame, text="Public", variable=self.__visibility, value=True, bg='light grey', font=FONT
                       ).grid(row=3, column=1, padx=PADX, pady=PADY)
        tk.Radiobutton(self.__mainFrame, text="Private", variable=self.__visibility, value=False, bg='light grey', font=FONT
                       ).grid(row=3, column=2, padx=PADX, pady=PADY)
        
        tk.Button(self.__mainFrame, text="Back", padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__setUpUser
                  ).grid(row=4, column=1, padx=PADX)
        tk.Button(self.__mainFrame, text="Insert", padx=PADX, font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, command=self.__addData
                  ).grid(row=4, column=2, padx=PADX)
    
    def __addData(self):
        imageURL = self.__imageURL.get(1.0, 'end-1c')
        location = self.__location.get(1.0, 'end-1c')
        device_type = self.__deviceType.get(1.0, 'end-1c')
            
        if not imageURL:
            messagebox.showerror('Empty Input', "Please provide an image URL!")
            return
        try:
            if requests.get(imageURL).status_code != 200:
                raise Exception
        except:
            messagebox.showerror('Invalid URL', "Please enter a valid accessible image URL")
            return
        
        VALUES = f"(\'{imageURL}\'," + ('null' if not location else f"\'{location}\'") 
        VALUES = VALUES + ',' + ('null' if not device_type else f"\'{device_type}\'")
        VALUES = VALUES + ',' + f"{self.__visibility.get()}," + f'\'{self.__loggedInUser["email"]}\'' + ")"
        
        print(VALUES)
        
        CURSOR.execute(f"INSERT INTO photo_db.t_image(\"image\", \"location\", \"device_type\", \"visibility\", \"owner\") VALUES {VALUES}")
        CONN.commit()
        messagebox.showinfo("insertion query","image inserted successfully!!")
        self.__setUpUser()
        
    
    def __deleteImage(self, image_id):
        if messagebox.askokcancel("Delete Image", "Are you sure you want to delete the image?"):
            CURSOR.execute(f"DELETE FROM photo_db.t_image WHERE \"image_id\" = {image_id};")
            CONN.commit()
            
            messagebox.showinfo(f'Image ID: {image_id}', "Image Deleted Successfully!!")
        self.__setUpUser()
    
    
    def __checkBin(self):
        self.__mainFrame.destroy()
        self.__headerFrame.destroy()
        
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        tk.Label(self.__headerFrame, text="Recycle Bin", font=FONT_HEADER, bg=FRAME_BG, padx=PADX).grid()
        self.__mainFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()

        CURSOR.execute(f"""
                       SELECT "image"
                       FROM photo_db.t_image
                       NATURAL JOIN photo_db.t_recycle_bin
                       WHERE "owner" LIKE '{self.__loggedInUser['email']}'
                       """)
        
        data = CURSOR.fetchall()
        
        if not data:
            tk.Label(self.__mainFrame, text="No Deleted Images", font=FONT_HEADER, bg=FRAME_BG).grid(row=0, column=0)
        else:
            for i in range(len(data)):
                imageButton = tk.Button(self.__mainFrame, text=data[i], font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, padx=PADX)
                imageButton.bind("<Button-1>", self.__openLinkWrapper(2, data[i][0]))
                imageButton.grid(row=i, column=0, padx=PADX, pady=PADY)
            
        tk.Button(self.__mainFrame, text="Back", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, padx=PADX, command=self.__setUpUser
                    ).grid(row=(len(data))+1, column=0, padx=PADX, pady=PADY)
        
        
    def __openAlbumLinkWrapper(self, album, album_image):
        return lambda Button: self.__openAlbumLink(album, album_image)
    
    def __openAlbumLink(self, album_id, album_image):
        response = requests.get(album_image)
        if response.status_code:
            with open('temp.png', 'wb') as fp:
                fp.write(response.content)
                fp.close()
                
            self.__headerFrame.destroy()
            self.__mainFrame.destroy()
            self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
            self.__headerFrame.pack()
            self.__mainFrame = tk.Frame(self.__root, padx=10*PADX, pady=PADY, bg=FRAME_BG)
            self.__mainFrame.pack()
        
        CURSOR.execute(f'SELECT "album_name" FROM photo_db.t_albums WHERE "album_id" = {album_id};')
        album_name = CURSOR.fetchall()[0][0]
        
        self.__displayImg = PhotoImage(Image.open('temp.png'))
        tk.Label(self.__headerFrame, text=f"Album Name: {album_name}", font=FONT_HEADER, bg=FRAME_BG).grid(row=0, column=0)
        tk.Label(self.__headerFrame, text=album_image, font=FONT_HEADER, bg=FRAME_BG).grid(row=1, column=0)
        tk.Label(self.__mainFrame, image=self.__displayImg).grid(row=0, column=0, padx=PADX, pady=PADY)
        backButton = tk.Button(self.__mainFrame, text="Back", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG)
        backButton.grid(row=1, column=0, padx=PADX, pady=PADY)
        backButton.bind("<Button-1>", self.__openAlbumWrapper(album_id))
    
        
    def __subscriptionPlans(self):        
        self.__headerFrame.destroy()
        self.__mainFrame.destroy()
        self.__headerFrame = tk.Frame(self.__root, padx=PADX, pady=PADY, bg=FRAME_BG)
        self.__headerFrame.pack()
        self.__mainFrame = tk.Frame(self.__root, padx=10*PADX, pady=PADY, bg=FRAME_BG)
        self.__mainFrame.pack()
        
        CURSOR.execute("SELECT * FROM photo_db.t_subscription_plan")
        data = CURSOR.fetchall()
        
        tk.Label(self.__headerFrame, text="Current Subscription Plans", font=FONT_HEADER, bg=FRAME_BG).grid()
        
        tk.Label(self.__mainFrame, text="Plan ID", font=FONT, bg=CELL_BG[0], width=10).grid(row=0, column=0, padx=PADX)
        tk.Label(self.__mainFrame, text="Cost (Rs.)", font=FONT, bg=CELL_BG[0], width=12).grid(row=0, column=1, padx=PADX)
        tk.Label(self.__mainFrame, text="Storage Limit (GB)", font=FONT, bg=CELL_BG[0], width=19).grid(row=0, column=2, padx=PADX)
        tk.Label(self.__mainFrame, text="Album Limit", font=FONT, bg=CELL_BG[0], width=15).grid(row=0, column=3, padx=PADX)
        tk.Label(self.__mainFrame, text="Album Edit Limit", font=FONT, bg=CELL_BG[0], width=17).grid(row=0, column=4, padx=PADX)
        tk.Label(self.__mainFrame, text="Plan Type", font=FONT, bg=CELL_BG[0], width=10).grid(row=0, column=5, padx=PADX)
        tk.Label(self.__mainFrame, text="Managed By", font=FONT, bg=CELL_BG[0], width=35).grid(row=0, column=6, padx=PADX)
        tk.Label(self.__mainFrame, text="Duration (Months)", font=FONT, bg=CELL_BG[0], width=17).grid(row=0, column=7, padx=PADX)
        
        for i in range(len(data)):
            tk.Label(self.__mainFrame, text=data[i][0], font=FONT, bg=CELL_BG[(i+1)%2], width=10).grid(row=(i+1), column=0, padx=PADX)
            tk.Label(self.__mainFrame, text=data[i][1], font=FONT, bg=CELL_BG[(i+1)%2], width=12).grid(row=(i+1), column=1, padx=PADX)
            tk.Label(self.__mainFrame, text=data[i][2], font=FONT, bg=CELL_BG[(i+1)%2], width=19).grid(row=(i+1), column=2, padx=PADX)
            tk.Label(self.__mainFrame, text=data[i][3], font=FONT, bg=CELL_BG[(i+1)%2], width=15).grid(row=(i+1), column=3, padx=PADX)
            tk.Label(self.__mainFrame, text=data[i][4], font=FONT, bg=CELL_BG[(i+1)%2], width=17).grid(row=(i+1), column=4, padx=PADX)
            tk.Label(self.__mainFrame, text=data[i][5], font=FONT, bg=CELL_BG[(i+1)%2], width=10).grid(row=(i+1), column=5, padx=PADX)
            tk.Label(self.__mainFrame, text=data[i][6], font=FONT, bg=CELL_BG[(i+1)%2], width=35).grid(row=(i+1), column=6, padx=PADX)
            tk.Label(self.__mainFrame, text=data[i][7], font=FONT, bg=CELL_BG[(i+1)%2], width=17).grid(row=(i+1), column=7, padx=PADX)
        
        tk.Button(self.__mainFrame, text="Back", font=FONT, bg=CELL_BG[(len(data)+1)%2], command=self.__setUpAdmin
                  ).grid(row=(len(data)+1), column=0, columnspan=8, padx=PADX, pady=PADY)
     
    
    def run(self):
        self.__root.mainloop()
        

if __name__  == "__main__":
    ui = FrontEnd(tk.Tk(className='Photo Dump UI'))
    ui.run()
    CONN.close()