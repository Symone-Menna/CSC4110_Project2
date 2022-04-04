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
            print("order made")
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
    canvasRoot.create_image(0,0, image = bg, anchor = "nw")
    

        
    #function for main menu page
    def mainMenu():
        mainMenu = tk.Toplevel(root)
        mainMenu.title("Main Menu")
        mainMenu.geometry("350x500")
        mainMenu.maxsize(894, 670)
        mainMenu.minsize(350,500)
        mainMenu.iconbitmap("bearicon.ico")

        #photo background
        canvas = tk.Canvas(mainMenu, width = 600, height = 500)
        canvas.pack(fill = "both", expand = True)
        canvas.create_image(0,0, image = bg, anchor = "nw")

        #add inventory button
        adb = tk.Button(mainMenu, text = 'Add Inventory',command=addInventoryWindow, bd = '5',bg = "black", fg = "white").place(x=100,y=100)

        #Veiw Inventory button
        qdb = tk.Button(mainMenu, text = 'Veiw Inventory',command=viewInventoryWindow, bd = '5',bg = "black", fg = "white").place(x=100,y=150)

        #Make drink button
        ipb = tk.Button(mainMenu, text = 'Make Drink',command=makeDrinkWindow, bd = '5',bg = "black", fg = "white").place(x=100,y=200)

        #Veiw Transaction button
        rdb = tk.Button(mainMenu, text = 'Veiw Transactions', bd = '5',bg = "black", fg = "white").place(x=100,y=250)


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
        canvas.create_image(0,0, image = bg, anchor = "nw")

        ingredientVal = tk.StringVar()
        quantityVal = tk.StringVar()
       

        #create entry boxes
        ingredient = tk.Entry(addInventory, textvariable = ingredientVal)
        quantity = tk.Entry(addInventory, textvariable = quantityVal)
        
        canvas.create_window(250,100, window=ingredient)
        canvas.create_window(250,150, window=quantity)
       
        #create labels
        example = tk.Label(addInventory, text="Example Format",bg = "black", fg = "white")
        canvas.create_window(367,65, window=example)
        labelIngredient = tk.Label(addInventory, text="Ingredient",bg = "black", fg = "white")
        canvas.create_window(150,100, window=labelIngredient)
        ingredientEx = tk.Label(addInventory, text="Pinappple juice",bg = "black", fg = "white")
        canvas.create_window(360,100, window=ingredientEx)
        labelQuantity = tk.Label(addInventory, text="Quantity",bg = "black", fg = "white")
        canvas.create_window(150,150, window=labelQuantity)
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
        submit = tk.Button(addInventory, text = 'Submit', command=submit,bd = '5',bg = "black", fg = "white").place(x=250,y=450)
        
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
        canvas.create_image(0,0, image = bg, anchor = "nw")


        #create entry box with labels
        labelView = tk.Label(viewInventory, text="Click to veiw inventory",bg = "black", fg = "white")
        canvas.create_window(180,100, window=labelView)
      
        #submit button
        submit = tk.Button(viewInventory, text = 'view inventory',bd = '5',bg = "black", fg = "white").place(x=130,y=150)
          
        
    #import data window
    def makeDrinkWindow():
        fileValue = tk.StringVar()
        makeDrink = tk.Toplevel(root)
        makeDrink.title("Make Drink")
        makeDrink.geometry("500x500")
        makeDrink.maxsize(894, 670)
        makeDrink.minsize(350,500)
        canvas = tk.Canvas(makeDrink, width = 500, height = 300)
        canvas.pack(fill = "both", expand = True)
        makeDrink.iconbitmap("bearicon.ico")

        #photo background
        canvas.create_image(0,0, image = bg, anchor = "nw")

        #old fashioned image and resizing 
        of_dir = os.path.dirname(os.path.abspath(__file__))
        of = Image.open(os.path.join(of_dir,"old_fashioned.jpg"))
        ofResize = of.resize((80,80))
        ofImage = ImageTk.PhotoImage(ofResize)

        #function to order oldfashioned
        def orderOF():
            barObj.makeOrder("old_fashioned",barObj.old_fashioned)

        old_fashioned = tk.Button(makeDrink, image = ofImage, text = 'Old Fashioned', command= orderOF(),bd = '5').place(x=100,y=100)


        margarita = tk.Button(makeDrink, text = 'Margarita', bd = '5',bg = "black", fg = "white").place(x=100,y=200)


        cosmo = tk.Button(makeDrink, text = 'Cosmo', bd = '5',bg = "black", fg = "white").place(x=200,y=100)


        negroni = tk.Button(makeDrink, text = 'Negroni', bd = '5',bg = "black", fg = "white").place(x=200,y=200)


        moscow_mule = tk.Button(makeDrink, text = 'Moscow Mule',bd = '5',bg = "black", fg = "white").place(x=300,y=100)


        martini = tk.Button(makeDrink, text = 'Martini', bd = '5',bg = "black", fg = "white").place(x=300,y=200)       
        
        
        mojito = tk.Button(makeDrink, text = 'Mojito', bd = '5',bg = "black", fg = "white").place(x=400,y=150)


        




    #server one button
    def sOneLogOn():
        barObj.logOn("Bryan")

    sOne = tk.Button(root, text = 'Server 1',command=lambda:[sOneLogOn(), mainMenu()], bd = '5',bg = "black", fg = "white").place(x=150,y=100)

    #server two button
    def sTwoLogOn():
        barObj.logOn("Carson")

    sTwo = tk.Button(root, text = 'Server 2',command=lambda:[sTwoLogOn(), mainMenu()], bd = '5',bg = "black", fg = "white").place(x=150,y=150)

    #server three button
    def sThreeLogOn():
        barObj.logOn("Symone")

    sThree = tk.Button(root, text = 'Server 3',command=lambda:[sThreeLogOn(), mainMenu()], bd = '5',bg = "black", fg = "white").place(x=150,y=200)

    #server four button
    def sFourLogOn():
        barObj.logOn("Timothy")

    sFour = tk.Button(root, text = 'Server 4', command=lambda:[sFourLogOn(), mainMenu()], bd = '5',bg = "black", fg = "white").place(x=150,y=250)

    tk.mainloop()

def main():

    tkmain()



if __name__ == "__main__":
    main()