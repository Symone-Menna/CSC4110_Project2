# function to modify inventory

import json

def modify_inventory(recipe):
    inventory = {}
    with open("inventory.json") as file:
        inventory = json.load(file)
    for i in recipe.keys():
        inventory[i] = inventory[i] + recipe[i]
    with open("inventory.json", "w") as file:
        file.write(json.dumps(inventory, indent = 4))
            

def main():
    transaction = {'whiskey' : -2, 'bitters' : -0.1, 'sugar cube' : -1, 'orange twist' : -1}
    modify_inventory(transaction)
if __name__=="__main__":
    main()