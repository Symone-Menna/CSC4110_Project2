##BEGIN CODE

from datetime import datetime
import json
import csv
import re       
import os.path
import PIL
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk


class Bar:
    employee = ""
    # pass these variable names to makeOrder() second argument
    old_fashioned = {'whiskey':2,'bitters':0.1,'sugarCube':1,'orangeTwist':1}
    margarita = {'tequila':2,'cointreau':1,'limeJuice':1}
    cosmo = {'gin':1,'campari':1,'sweetVermouth':1}
    negroni = {'gin':1,'campari':1,'sweetVermouth':1}
    moscow_mule = {'vodka':2,'gingerBeer':6,'limeJuice':0.5}
    martini = {'vodka':3,'dryVermouth':0.5,'olive':2}
    mojito = {'rum':2,'limeJuice':0.75,'simpleSyrup':0.5}    

    #opens the json file and removes the quantity specified in recipe dictionary
    def removeInventory(self, recipe):
        inventory = {}
        with open("inventory.json", 'r') as file:
            inventory = json.load(file)
        for i in recipe.keys():
            inventory[i] = round(inventory[i] - recipe[i], 2)
        with open("inventory.json", "w") as file:
            file.write(json.dumps(inventory, indent = 4))

    def filterEntry(s):
        filt = re.compile("[^a-zA-Z_ ]+")
        if filt.search(s):
            return False
        else:
            return True

    # opens the json file and adds the value parameter to the json entry with the specified key pair
    def addInventory(self, key, value):
        key.replace(" ","_")
        with open("inventory.json", 'r') as file:
            inventory = json.load(file)
        inventory[key] = inventory[key] + value
        print(key +" added to inventory")
        with open("inventory.json", "w") as file:
            file.write(json.dumps(inventory, indent = 4))

    # interacts with the csv file to track server, time, and order that was placed
    def logOrder(self,drink,drinkDict):
        with open('barLog.csv', 'a', newline='') as file:
            writer_object = csv.writer(file)
            writer_object.writerow([self.employee,datetime.now(),drink,drinkDict])
            file.close()

    def printInventory(self):
        with open("inventory.json", 'r') as file:
            inventory = json.load(file)
        keys = dict.keys(inventory)
        for item in keys:
            print(str(item) + ":" + str(inventory[item]))

    #checks the inventory and prints to the console with messages currently
    def checkInventory(self,recipe):
        inventory = {}
        with open("inventory.json", 'r') as file:
            inventory = json.load(file)
        for i in recipe.keys():
            if inventory[i] < recipe[i]:
                print("Insufficient inventory available!")
                return False
            elif inventory[i] < 6 * recipe[i]:
                print("Low inventory, replenish soon")
        return True

    # pass the name of the drink to the function as a string, and the Bar object dictionary with the same key.
    def makeOrder(self,drink,drinkDict):
        if self.checkInventory(drinkDict):
            self.logOrder(drink,drinkDict)
            self.removeInventory(drinkDict)
            print(drink + " order made")
            return True
        return False

    # trigger off of tkinter button before orders are placed to maintain an open session for the selected server
    def logOn(self,name): 
        print("Hello " + name)
        self.employee = name





#tkinter main loop
def tkmain():
    #object for class bar
    barObj = Bar()


    #create tkinter window
    root = tk.Tk()
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    #open window dimention
    root.geometry('350x500')
    root.maxsize(894, 670)
    root.minsize(350,500)
    root.title("BEAR-ly Sober")
    root.iconbitmap("bearicon.ico")

    #image background
    bg = tk.PhotoImage(file="background.png")
    canvasRoot = tk.Canvas(root, width = 500, heigh = 500)
    canvasRoot.pack(fill = "both", expand = True)
    #canvasRoot.create_image(0,0, image = bg, anchor = "nw")
    

        
    #function for main menu page
    def mainMenu():
        mainMenu = tk.Toplevel(root)
        mainMenu.title("Main Menu")
        mainMenu.geometry("300x300")
        mainMenu.maxsize(894, 670)
        mainMenu.minsize(350,500)
        mainMenu.iconbitmap("bearicon.ico")

        #photo background
        canvas = tk.Canvas(mainMenu, width = 600, height = 500)
        canvas.pack(fill = "both", expand = True)
        #canvas.create_image(0,0, image = bg, anchor = "nw")

        #add inventory button
        adb = ttk.Button(mainMenu,text="Add Inventory", command = addInventoryWindow, style="Accent.TButton").place(x=120, y=150)

        #Veiw Inventory button
        qdb = ttk.Button(mainMenu,text="View Inventory", command = viewInventoryWindow, style="Accent.TButton").place(x=120, y=200)

        #Make drink button
        mdb = ttk.Button(mainMenu,text="Make Drink", command = makeDrinkWindow, style="Accent.TButton").place(x=125, y=250)

        titleLabel = ttk.Label(
            mainMenu,
            text="Welcome",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        titleLabel.place(x=125, y=100)

        leave = ttk.Button(mainMenu,text="Exit", command=Close)
        leave.place(x=125,y=400)




    #funtion for add inventory window
    def addInventoryWindow():
        addInventory = tk.Toplevel(root)
        addInventory.title("Add Inventory")
        addInventory.geometry("600x500")
        addInventory.maxsize(894, 670)
        addInventory.minsize(350,500)
        addInventory.iconbitmap("bearicon.ico")

        #photo background
        canvas = tk.Canvas(addInventory, width = 600, height = 500)
        canvas.pack(fill = "both", expand = True)
        #canvas.create_image(0,0, image = bg, anchor = "nw")

        ingredientVal = tk.StringVar()
        quantityVal = tk.StringVar()
       

        #create entry boxes
        ingredient = ttk.Entry(addInventory, textvariable = ingredientVal)
        quantity = ttk.Entry(addInventory, textvariable = quantityVal)
        
        canvas.create_window(250,100, window=ingredient)
        canvas.create_window(250,150, window=quantity)
       
        #create labels
        example = tk.Label(addInventory, text="Example Format",bg = "black", fg = "white")
        canvas.create_window(367,65, window=example)
        labelIngredient = tk.Label(addInventory, text="Ingredient",bg = "black", fg = "white")
        canvas.create_window(130,100, window=labelIngredient)
        ingredientEx = tk.Label(addInventory, text="whiskey",bg = "black", fg = "white")
        canvas.create_window(360,100, window=ingredientEx)
        labelQuantity = tk.Label(addInventory, text="Quantity",bg = "black", fg = "white")
        canvas.create_window(130,150, window=labelQuantity)
        quantityEx = tk.Label(addInventory, text="oz",bg = "black", fg = "white")
        canvas.create_window(350,150, window=quantityEx)
        

        strIngredient = ingredientVal.get()
        strQuantity = quantityVal.get()
        

        def submit():
            strIngredient = ingredientVal.get()
            strQuantity = quantityVal.get()
            barObj.addInventory(strIngredient,int(strQuantity))
            ingredientVal.set("")
            quantityVal.set("")
         

        #submit button
        submit = ttk.Button(addInventory, text = 'Submit', command=submit, style="Accent.TButton").place(x=250,y=175)
        
    #function to search data
    def viewInventoryWindow():
        viewInventory = tk.Toplevel(root)
        viewInventory.title("Query Data")
        viewInventory.geometry("300x300")
        viewInventory.maxsize(894, 670)
        viewInventory.minsize(350,500)
        canvas = tk.Canvas(viewInventory, width = 500, height = 300)
        canvas.pack(fill = "both", expand = True)
        viewInventory.iconbitmap("bearicon.ico")

        #photo background
        #canvas.create_image(0,0, image = bg, anchor = "nw")


        #create entry box with labels
        labelView = tk.Label(viewInventory, text="Click to view inventory",bg = "black", fg = "white")
        canvas.create_window(180,100, window=labelView)

        def submit():
            barObj.printInventory()
      
        #submit button
        submit = ttk.Button(viewInventory, text = 'View inventory',style="Accent.TButton", command=submit).place(x=130,y=150)
        
        
          
        
    #import data window
    def makeDrinkWindow():
        fileValue = tk.StringVar()
        makeDrink = tk.Toplevel(root)
        makeDrink.title("Make Drink")
        makeDrink.geometry("550x500")
        makeDrink.maxsize(894, 670)
        makeDrink.minsize(350,500)
        canvas = tk.Canvas(makeDrink, width = 550, height = 300)
        canvas.pack(fill = "both", expand = True)
        makeDrink.iconbitmap("bearicon.ico")

        #photo background
        #canvas.create_image(0,0, image = bg, anchor = "nw")

        #old fashioned image and resizing 
        of_dir = os.path.dirname(os.path.abspath(__file__))
        of = Image.open(os.path.join(of_dir,"img/old_fashioned.jpg"))
        width,height = of.size
        new_width = width//10
        new_height = height//10
        size = (new_width,new_height)
        ofResize = of.resize((size))
        ofImage = ImageTk.PhotoImage(ofResize)

        #function to order oldfashioned
        def orderOF():
            barObj.makeOrder("old_fashioned",barObj.old_fashioned)

        old_fash = tk.Button(makeDrink, image = ofImage, command= lambda:orderOF(),bd = '5')
        old_fash.photo = ofImage
        old_fash.place(x=50,y=50)
        #old fashoned label
        labelOF = tk.Label(makeDrink, text="Old Fashioned",bg = "black", fg = "white")
        canvas.create_window(105,37, window=labelOF)
        
        #margarita image manipulation
        mar_dir = os.path.dirname(os.path.abspath(__file__))
        mar = Image.open(os.path.join(mar_dir,"img/margarita.jpg"))
        marResize = mar.resize((size))
        marImage = ImageTk.PhotoImage(marResize)

        #function to order margarita
        def orderMar():
            barObj.makeOrder("margarita",barObj.margarita)

        marg = tk.Button(makeDrink, image = marImage ,command=lambda:orderMar(), bd = '5')
        marg.photo = marImage
        marg.place(x=175,y=50)
        labelMarg = tk.Label(makeDrink, text="Margarita",bg = "black", fg = "white")
        canvas.create_window(230,37, window=labelMarg)

        #cosmo image manipulation
        cos_dir = os.path.dirname(os.path.abspath(__file__))
        cos = Image.open(os.path.join(cos_dir,"img/cosmo.jpg"))
        cosResize = cos.resize((size))
        cosImage = ImageTk.PhotoImage(cosResize)

        #function to order cosmo
        def orderCosmo():
            barObj.makeOrder("cosmo",barObj.cosmo)
        
        cosmo = tk.Button(makeDrink, image = cosImage,command=lambda:orderCosmo(), bd = '5')
        cosmo.photo = cosImage
        cosmo.place(x=300,y=50)
        labelCosmo = tk.Label(makeDrink, text="Cosmopolitan",bg = "black", fg = "white")
        canvas.create_window(355,37, window=labelCosmo)

        #negroni image manipulation
        neg_dir = os.path.dirname(os.path.abspath(__file__))
        neg = Image.open(os.path.join(neg_dir,"img/negroni.jpg"))
        negResize = neg.resize((size))
        negImage = ImageTk.PhotoImage(negResize)

        #function to order negroni
        def orderNegroni():
            barObj.makeOrder("negroni",barObj.negroni)

        negroni = tk.Button(makeDrink, image = negImage,command=lambda:orderNegroni(), bd = '5')
        negroni.photo = negImage
        negroni.place(x=425,y=150)
        #negroni label
        labelNeg = tk.Label(makeDrink, text="Negroni",bg = "black", fg = "white")
        canvas.create_window(475,137, window=labelNeg)

        #moscow mule image manipulation
        mule_dir = os.path.dirname(os.path.abspath(__file__))
        neg = Image.open(os.path.join(mule_dir,"img/moscow_mule.jpg"))
        muleResize = neg.resize((size))
        muleImage = ImageTk.PhotoImage(muleResize)

        #function to order negroni
        def orderMoscowMule():
            barObj.makeOrder("moscow_mule",barObj.moscow_mule)

        moscow_mule = tk.Button(makeDrink,image=muleImage, command=lambda:orderMoscowMule(),bd = '5')
        moscow_mule.photo = muleImage
        moscow_mule.place(x=50,y=250)
        #moscow mule label
        labelMule = tk.Label(makeDrink, text="Moscow Mule",bg = "black", fg = "white")
        canvas.create_window(105,237, window=labelMule)

        #martini image manipulation
        tini_dir = os.path.dirname(os.path.abspath(__file__))
        neg = Image.open(os.path.join(tini_dir,"img/martini.jpg"))
        tiniResize = neg.resize((size))
        tiniImage = ImageTk.PhotoImage(tiniResize)

        #function to order martini
        def orderMartini():
            barObj.makeOrder("martini",barObj.martini)

        martini = tk.Button(makeDrink, image = tiniImage,command=lambda:orderMartini(), bd = '5')     
        martini.photo = tiniImage
        martini.place(x=175,y=250)
        #martini label
        labelTini = tk.Label(makeDrink, text="Martini",bg = "black", fg = "white")
        canvas.create_window(230,237, window=labelTini)
        
        #mojito image manipulation
        moj_dir = os.path.dirname(os.path.abspath(__file__))
        moj = Image.open(os.path.join(moj_dir,"img/mojito.jpg"))
        mojResize = moj.resize((size))
        mojImage = ImageTk.PhotoImage(mojResize)

        #function to order mojito
        def orderMojito():
            barObj.makeOrder("mojito",barObj.mojito)
        
        mojito = tk.Button(makeDrink, image=mojImage,command=lambda:orderMojito(), bd = '5')
        mojito.photo = mojImage
        mojito.place(x=300,y=250)
        #mojito label
        labelMoj = tk.Label(makeDrink, text="Mojito",bg = "black", fg = "white")
        canvas.create_window(355,237, window=labelMoj)

    #Function to Check if password is correct
    def checkPassword(strPassword, name):
        if strPassword == "JlAK7r%2Xvjb":
            mainMenu()
            
            #Checks who the server is
            if name == "Bryan":
                sOneLogOn()
            elif name == "Carson":
                sTwoLogOn()
            elif name == "Symone":
                sThreeLogOn()
            elif name == "Timothy":
                sFourLogOn()
            
             
        else:
            print("Incorrect Password Entered.")


     #Function to Get Input of Password from server
    def PasswordLogin(name):
        dataEntry = tk.Toplevel(root)
        dataEntry.title("Enter password")
        dataEntry.geometry("400x100")
        dataEntry.maxsize(894, 670)
        dataEntry.minsize(350,500)
        canvas = tk.Canvas(dataEntry, width = 500, height = 200)
        canvas.pack(fill = "both", expand = True)

        #Brings in icon at the top
        dataEntry.iconbitmap("bearicon.ico")

        #For photo Background
        #canvas.create_image(0,0, image = bg, anchor = "nw")
        

        passwordValue = tk.StringVar()
        password = ttk.Entry(dataEntry, textvariable = passwordValue)
        canvas.create_window(250,100, window=password)
        labelPassword = tk.Label(dataEntry, text="Password", bg = "black", fg = "white")
        canvas.create_window(130,100, window=labelPassword)
        
        strPassword = passwordValue.get()
        def submit():
            strPassword = passwordValue.get()
            checkPassword(strPassword, name) 
            passwordValue.set("")
            dataEntry.destroy() #Closes password entry window after login

        
        submit = ttk.Button(dataEntry, text = 'Submit', command=submit,style="Accent.TButton").place(x=200,y=175)

    
    #server one button
    def sOneLogOn():
        barObj.logOn("Bryan")
        
    
    sOne = ttk.Button(text="Server 1", command=lambda:[PasswordLogin("Bryan")], style="Accent.TButton")
    sOne.place(x=125,y=150)

    #server two button
    def sTwoLogOn():
        barObj.logOn("Carson")
        

    sTwo = ttk.Button(text="Server 2", command=lambda:[PasswordLogin("Carson")], style="Accent.TButton")
    sTwo.place(x=125,y=200)

    #server three button
    def sThreeLogOn():
        barObj.logOn("Symone")
        

    sThree = ttk.Button(text="Server 3", command=lambda:[PasswordLogin("Symone")], style="Accent.TButton")
    sThree.place(x=125,y=250)

    #server four button
    def sFourLogOn():
        barObj.logOn("Timothy")
        

    sFour = ttk.Button(text="Server 4", command=lambda:[PasswordLogin("Timothy")], style="Accent.TButton")
    sFour.place(x=125,y=300)

    #Server Login Label
    
    loginLabel = ttk.Label(
            
            text="Server Login",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
    
    loginLabel.place(x=110, y =100)

    #For exit button
    def Close():
        root.destroy()

    #Exit button
    leave = ttk.Button(text="Exit", command=Close)
    leave.place(x=125,y=400)

    #Title Label
    titleLabel = ttk.Label(
            
            text="BEAR-LY Sober Bartender",
            justify="center",
            font=("-size", 10, "-weight", "bold"),
        )
    titleLabel.place(x=95, y=50)

    tk.mainloop()

def main():

    tkmain()



if __name__ == "__main__":
    main()