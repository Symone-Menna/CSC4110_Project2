##BEGIN CODE

from datetime import datetime
import json
import csv
import re       

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
        with open("inventory.json", 'r') as file:
            inventory = json.load(file)
        inventory[key] = inventory[key] + value
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
            return True
        return False

    # trigger off of tkinter button before orders are placed to maintain an open session for the selected server
    def logOn(self,name): 
        self.employee = name