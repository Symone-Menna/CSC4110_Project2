##BEGIN CODE

from datetime import datetime

class Drink:
        def __init__(self):  
            self.drinkInfo = {
                "Name":"Unknown",
                "QuantityNo" : [0,0,0],
                "QuantityName": ["unknown","unknown","unknown"]
                }


        def __init__(self, name, ingredientOne, ingredientOneName, ingredientTwo,ingredientTwoName, ingredientThree,ingredientThreeName):
            self.drinkInfo = {
                "Name":name,
                "QuantityNo":[ingredientOne,ingredientTwo,ingredientThree],
                "QuantityName":[ingredientOneName,ingredientTwoName,ingredientThreeName]               
                }
          

class Order:
    def __init__(self):
        self.orderInfo = {
            "Server":"Unknown",
            "Time":"00:00xx",
            "Drink":"Unknown"
        }

    def __init__(self,employee,date,drink):
        self.orderInfo = {
            "Server": employee,
            "Time": date,
            "Drink" : drink.drinkInfo["Name"]
            
            }
       
    def make(self,bar,drink):

        if bar.stockCheck(drink) == False:
            return

        bar.barLog.write("\n Server: ", self.orderInfo["Server"] , " Time: ",self.orderInfo["Time"], "Drink: ", self.orderInfo["Drink"])

        #Subtrack first ingredient, second, etc
        bar.stock[drink.drinkInfo["QuantityName"][0]] -= drink.drinkInfo["QuantityNo"[0]]
        bar.stock[drink.drinkInfo["QuantityName"][1]] -= drink.drinkInfo["QuantityNo"[1]]
        bar.stock[drink.drinkInfo["QuantityName"][2]] -= drink.drinkInfo["QuantityNo"[2]]






##Main class
class Bar:
   


    def __init__(self):
        self.employee = ""

        self.barLog = open("BarLog.txt",'w')
        
        self.drinks = {
            "Old Fashioned": Drink("Old Fashioned",2,"Whiskey",0.1,"Bitters",1,"Sugar Cube"),
            "Margarita": Drink("Margarita",2,"Tequila",1,"Cointreau",1,"Lime Juice"),
            "Cosmo": Drink("Cosmo",1.5,"Vodka",1,"Cointreau",.5,"Lime Juice"),
            "Negroni": Drink("Negroni",1,"Gin",1,"Campari",1,"Sweet Vermouth"),
            "Moscow Mule": Drink("Moscow Mule",2,"Vodka",6,"Ginger Beer",.5,"Lime Juice"),
            "Gin Martini": Drink("Gin Martini",3,"Gin",0.5,"Dry Vermouth",2,"Olive"),
            "Vodka Martini": Drink("Vodka Martini",3,"Vodka",0.5,"Dry Vermouth",2,"Olive"),
            "Mojito": Drink("Mojito",2,"Rum",0.75,"Lime Juice",.5,"Simple Syrup")
             
            }
        self.stock = {
            "Whiskey" : 20.0,
            "Bitters" : 20.0,
            "Sugar Cube" : 20.0,
            "Tequila" : 20.0,
            "Cointreau" : 20.0,
            "Lime Juice" : 20.0,
            "Vodka" : 20.0,
            "Gin" : 20.0,
            "Campari" : 20.0,
            "Sweet Vermouth" : 20.0,
            "Ginger Beer" : 20.0,
            "Dry Vermouth": 20.0,
            "Olive" : 20.0,
            "Simple Syrup" : 20.0,
            "Rum" : 20.0
            }


    def makeOrder(self,bar,drink):
        newOrder = Order(self.employee,datetime.now(),drink)
        newOrder.make(self,drink)



    def logOn(self,employee): #Sets employee thru tkinter button
        self.employee = employee

    def addInventory(ingredient, quantity): #Add stock (tkinter function)
        self.stock[ingredient] += quantity

    def stockCheck(self,drink):
        
        #Stock -> name of ingredient is used as a key to find corresponding value in stock dictionary, then compared to value in actual drink being ordered
        if self.stock[drink.drinkInfo["QuantityName"][0]] < drink.drinkInfo["QuantityNo"][0]:
            print("Not enough ", drink.drinkInfo["QuantityName"][0])
            return False
        if self.stock[drink.drinkInfo["QuantityName"][1]] < drink.drinkInfo["QuantityNo"][1]:
            print("Not enough ", drink.drinkInfo["QuantityName"][1])
            return False
        if self.stock[drink.drinkInfo["QuantityName"][2]] < drink.drinkInfo["QuantityNo"][2]:
            print("Not enough ", drink.drinkInfo["QuantityName"][2])
            return False
        return True
