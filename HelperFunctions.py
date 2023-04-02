import json
import csv


# because an apple is like 180g but reviewed as 100g. This speeds things up
def WeightMutliplier(food, multiplier):
    with open("Data/foodLog.csv", "r") as fRead: 
        f = open('Data/nutrients.json')
        jsonDict = json.load(f)

    keyList = list(jsonDict[food].keys())

    for key in keyList:
        if (type(jsonDict[food][key]) != str):
            jsonDict[food][key] = round(jsonDict[food][key] * multiplier, 6)

    jsonObj = json.dumps(jsonDict, indent = 4)
 
    with open("Data/nutrients.json", "w") as outfile:
        outfile.write(jsonObj)



# maybe I add a food with erythritol and I want to add that. This adds a "erythritol: 0," entry
# > to every food entry PLEASE ALSO ADD IT TO THE TEMPLATE
# pm: insertAfter: nutrient that goes right before it | insertThis: nutrient to add
def EditNutrientJson(insertAfter, insertThis):
    holderDict = {}
    file = 'backups/nutrientsBACKUP.json'
    #'Data/nutrients.json'
    f = open(file)
    foodDict = json.load(f)

    # copy contents/new nutrient to holder dictionary, replace original with holder
    for food in list(foodDict.keys()):
        for nutrient in foodDict[food]:
            holderDict[nutrient] = foodDict[food][nutrient]
            if (nutrient == insertAfter):
                holderDict[insertThis] = 0
        foodDict[food] = holderDict
        holderDict = {}

    if (FileConfirmationText(file) == 'y'):
        jsonObj = json.dumps(foodDict, indent = 4)
        with open(file, "w") as outfile:
            outfile.write(jsonObj)



# if I decide I want something in mg instead of g or something
def ConvertAllNutrients():
    file = 'backups/OFFICIAL2000CalorieNutritionGoals.json'
    #'Data/nutrients.json'
    #'backups/nutrientsBACKUP.json'
    #'Data/CUSTOMNutritionGoals.json'
    #'backups/OFFICIAL2000CalorieNutritionGoals.json'
    f = open(file)
    foodDict = json.load(f)

    for food in list(foodDict.keys()):
        for nutrient in foodDict[food]:
            if (nutrient in gNutrients):
                foodDict[food][nutrient] = foodDict[food][nutrient] / 1000
            elif (nutrient in mgNutrients):
                foodDict[food][nutrient] = foodDict[food][nutrient] 
            elif (nutrient in mcgNutrients):
                foodDict[food][nutrient] = foodDict[food][nutrient] * 1000
            elif (nutrient in mnNutrients):
                foodDict[food][nutrient] = foodDict[food][nutrient] 

    if (FileConfirmationText(file) == 'y'):
        jsonObj = json.dumps(foodDict, indent = 4)
        with open(file, "w") as outfile:
            outfile.write(jsonObj)



def WriteTest():
    with open("Data/foodLog.csv", "w", newline='') as w:
        writer = csv.writer(w)

        writer.writerow(["Date", "Foods/Servings"])
        writer.writerow(['11/1/2022', 'strawberries (1)'])
        writer.writerow(["10/31/2022", 'blueberries (1)'])
        w.close()



def FileConfirmationText(file):
    x = input("Is the file right? (y/n) " + file + " ")
    return x



# antioxidents are mg. I write them simply as "+" so don't include them in these lists
gNutrients = ["protein", "carbs", "total_fat", "saturated_fat", "trans_fat", "polyunsaturated_fat", "monounsaturated_fat", "sugar", "erythritol (sweetener)", "cant_tell_fiber", "dietary_fiber", "vit_b7 (biotin)", "creatine", "L_glutamine"]
mgNutrients = ["cholesterol", "sodium", "vit_b1 (thiamine)", "vit_b2 (riboflavin)", "vit_b4 (niacin)", "vit_b5 (pantothenic_acid)", "vit_b6 (pyridoxine)", "vit_b12 (cobalamin)", "vit_c", "vit_e", "potassium", "calcium", "iron", "magnesium", "manganese", "zinc", "copper", "phosphorus", "choline", "chloride", "lycopene", "phenylalanine (EAA)", "valine (EAA)", "threonine (EAA)", "tryptophan (EAA)", "methionine (EAA)", "leucine (EAA)", "taurine", "omega-3", "omega-6", "medium-chain triglycerides", "lutein + zeaxanthin"]
mcgNutrients = ["vit_a", "vit_b9 (folic acid)", "vit_b12 (cobalamin)", "vit_d", "vit_k", "folate", "iodine", "selenium", "molybdenum", "chromium"]
mnNutrients = ["bacillus coagulans"]


#EditNutrientJson("sugar", "erythritol (sweetener)")
#WeightMutliplier("apple", 1.7)
ConvertAllNutrients()
#WriteTest()