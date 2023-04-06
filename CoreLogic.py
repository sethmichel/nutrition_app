# some fields have ??? meaning look it up
# food won't say if it has antioxidants or EAA's
# everything is in grams or "thing"


''' json template (make sure it's in mg)
{"name": {
        "serving size": ,
        "calories": ,
        "protein": ,
        "carbs": ,
        "total_fat": ,
        "saturated_fat": ,
        "trans_fat": ,
        "polyunsaturated_fat": ,
        "monounsaturated_fat": ,
        "cholesterol": ,
        "sodium": ,
        "sugar": ,
        "erythritol (sweetener)": ,
        "cant_tell_fiber": ,
        "dietary_fiber": ,
        "vit_a": ,
        "vit_b1 (thiamine)": ,
        "vit_b2 (riboflavin)": ,
        "vit_b4 (niacin)": ,
        "vit_b5 (pantothenic_acid)": ,
        "vit_b6 (pyridoxine)": ,
        "vit_b7 (biotin)": ,
        "vit_b9 (folic acid)": ,
        "vit_b12 (cobalamin)": ,
        "vit_c": ,
        "vit_d": ,
        "vit_e": ,
        "vit_k": ,
        "potassium": ,
        "folate": ,
        "calcium": ,
        "iron": ,
        "iodine": ,
        "magnesium": ,
        "manganese": ,
        "zinc": ,
        "selenium": ,
        "copper": ,
        "phosphorus": ,
        "molybdenum": ,
        "chromium": ,
        "choline": ,
        "chloride": ,
        "lycopene": ,
        "phenylalanine (EAA)": ,
        "valine (EAA)": ,
        "threonine (EAA)": ,
        "tryptophan (EAA)": ,
        "methionine (EAA)": ,
        "leucine (EAA)": ,
        "isoleucine (EAA)": ,
        "lysine (EAA)": ,
        "histidine (EAA)": ,
        "anthocyanin (antioxidant)": "",
        "quercetin (antioxidant)": "",
        "myricetin (antioxidant)": "",
        "pelargonidin (antioxidant)": "",
        "procyanidins (antioxidant)": "",
        "ellagitannins (antioxidant)": "",
        "ellagic_acid (antioxidant)": "",
        "creatine": ,
        "taurine": ,
        "L_glutamine": ,
        "omega-3": ,
        "omega-6": ,
        "medium-chain triglycerides": ,
        "lutein + zeaxanthin": ,
        "bacillus coagulans": ""
    }
}
'''

import json
import csv
from datetime import date
from tabulate import tabulate
from colorama import Fore, Back, Style


# ask user what they ate, ignore breakfast, lunch, dinner specification, just what they ate that day
# create a meal: enter the foods and amounts -> it'll add to the json

def Main():
    userInput = ""

    while (userInput != "4"):
        with open("Data/foodLog.csv", "r") as fRead: 
            f = open('Data/nutrients.json')
            jsonDict = json.load(f)
            ShowTodaysNutrients(jsonDict)
            ListFoods()
            print("\n")

            userInput = input("1: Create food\n" +
                            "2: Delete an excel food from today\n" +
                            "3: Quit\n" +
                            "OR type a food to add it to today\n")

            if (userInput == "1"):
                jsonDict = CreateFood(jsonDict)
            elif (userInput == "2"):
                DeleteExcelEntry(userInput)
            elif (userInput =="3"):
                break
            else:
                for food in jsonDict.keys():
                    if (userInput == food):
                        AddFoodToExcel(userInput, jsonDict)
                        break
                else:
                    print("NOT A LOGGED FOOD")
            
    f.close();


def CalcuateFoodTotals(nutrient, listOfFoods, servingsList, jsonDict):
    strFoods = [
        "anthocyanin (antioxidant)",
        "quercetin (antioxidant)",
        "myricetin (antioxidant)",
        "pelargonidin (antioxidant)",
        "procyanidins (antioxidant)",
        "ellagitannins (antioxidant)",
        "ellagic_acid (antioxidant)",
        "bacillus coagulans"
    ]

    # if it's a string it'll be "+". otherwise it's a double
    try: 
        strFoods.index(nutrient)   # error if not found
        total = ""
        for i in range(0, len(listOfFoods)):
            for j in range(0, int(servingsList[i])):
                total = total + jsonDict[listOfFoods[i]][nutrient]
    except:
        total = 0.0
        for i in range(0, len(listOfFoods)):
            total += (jsonDict[listOfFoods[i]][nutrient] * int(servingsList[i]))
        total = round(total, 6)

    return total


# date, list of foods (servings) with , delimiter
def AddFoodToExcel(foodToAdd, jsonDict):
    today = GetTodaysDate()   # 12/11/2019
    servings = input("How many servings? ")
    foodToAdd = foodToAdd + "(" + servings + ")"
    csvDict = LoadCsvDict(headers)

    with open("Data/foodLog.csv", "w", newline='') as w:
        writer = csv.DictWriter(w, fieldnames = headers)

        # add food to csvDict
        if (len(csvDict) > 0 and csvDict[0][headers[0]] == today):
            csvDict[0][headers[1]] = csvDict[0][headers[1]] + '|' + foodToAdd   # 'strawberries (1)'
        else:
            csvDict.insert(0, {headers[0]: today, headers[1]: foodToAdd})       # doesn't add \n
        
        writer.writeheader()
        writer.writerows(csvDict)


# date, list of foods (servings) with , delimiter
def ShowTodaysNutrients(jsonDict):
    csvDict = LoadCsvDict()
    today = GetTodaysDate()

    f = open('Data/CUSTOMNutritionGoals.json')
    nutritonGoalDict = json.load(f)['goals']   # basic dictionary
    nutrientList = list(nutritonGoalDict.keys())
    todaysList = csvDict[0][headers[1]].split('|')   # [blueberries(1), blueberries(1), huel(1)]
    foodList = []
    servingsList = []
    consumedList = []
    goalList = []
    differenceList = []

    for i in range(0, len(todaysList)):
        startIndex = todaysList[i].index('(')
        endIndex = todaysList[i].index(')')
        servingsList.append(todaysList[i][startIndex + 1:endIndex])
        foodList.append(todaysList[i][:startIndex])
        
    for nutrient in nutrientList:
        consumedList.append(CalcuateFoodTotals(nutrient, foodList, servingsList, jsonDict))
        goalList.append(nutritonGoalDict[nutrient])
        if (type(consumedList[-1]) != str):
            difference = round(goalList[-1] - consumedList[-1], 3)
            if (difference > 0):
                differenceList.append(str(difference) + " Left to go")
            else:
                if (difference == 0):   # it'll say " -0.0 over" otherwise
                    differenceList.append(str(difference) + " over")
                else:
                    differenceList.append(str(difference * -1) + " over")
        else:
            differenceList.append(consumedList[-1])
    
    listHolder = AppendUnits(nutrientList, consumedList)
    nutrientList = listHolder[0]
    consumedList = listHolder[1]

    return [nutrientList, consumedList, differenceList]
    
    #tableDict = {'Nutrient': nutrientList, 'Consumed': consumedList, 'Goal': differenceList}

    #print("\n")
    #print(tabulate(tableDict, headers = ['Nutrient', 'Consumed', 'Goal'], tablefmt = 'fancy_grid'))


# converts list of nutrients to include units
def AppendUnits(nutrientList, consumedList):
    for i in range(0, len(nutrientList)):
        if (nutrientList[i] in gNutrients):
            nutrientList[i] = nutrientList[i] + " g"
            consumedList[i] = str(consumedList[i]) + " g"
        elif (nutrientList[i] in mgNutrients):
            nutrientList[i] = nutrientList[i] + " mg"
            consumedList[i] = str(consumedList[i]) + " mg"
        elif (nutrientList[i] in mcgNutrients):
            nutrientList[i] = nutrientList[i] + " mcg"
            consumedList[i] = str(consumedList[i]) + " mcg"
        elif (nutrientList[i] in mnNutrients):
            nutrientList[i] = nutrientList[i] + " mn"
            consumedList[i] = str(consumedList[i]) + " mn"

    return [nutrientList, consumedList]


def LoadCsvDict():
    csvDict = []
    with open('Data/foodLog.csv', "r") as r:
        reader = csv.DictReader(r)

        # load csv data
        for row in reader:
            csvDict.append({headers[0]: row[headers[0]], headers[1]: row[headers[1]]})

    return csvDict


def GetTodaysDate():
    today = str(date.today()).split("-")                  # 2019-12-11
    return (today[1] + "/" + today[2] + "/" + today[0])   # 12/11/2019


def ListFoods():
    today = GetTodaysDate()
    csvDict = LoadCsvDict()
    with open("Data/foodLog.csv", "r", newline='') as r:
        reader = csv.DictReader(r, fieldnames = headers)
        for row in reader:
            if (row["Date"] == today):
                holder = row["Foods/Servings"]
                holder = holder.replace("|", ", ")
                print(holder)

        

# sum ingredients into new food, save to json
def CreateFood(jsonDict):
    newFood = input("Enter new meal name: ")
    ingreList = (input("Enter ingredients separated by a comma (no servings): blueberries,\n")).split(",")
    servingList = (input("Enter servings for those foods separated by a ,\n")).split(",")

    fgoal = open('Data/CUSTOMNutritionGoals.json')
    nutrientList = list(json.load(fgoal)['goals'].keys())

    # calculate, serving size is "1 thing"
    jsonDict[newFood] = {"serving size": "1 thing"}
    for nutrient in nutrientList:
        jsonDict[newFood][nutrient] = CalcuateFoodTotals(nutrient, ingreList, servingList, jsonDict) 

    jsonObj = json.dumps(jsonDict, indent = 4)
 
    with open("Data/nutrients.json", "w") as outfile:
        outfile.write(jsonObj)

    # reload jsonDict
    f = open('Data/nutrients.json')
    return json.load(f)

# globals
# antioxidents are mg. I write them simply as "+" so don't include them in these lists
gNutrients = ["protein", "carbs", "total_fat", "saturated_fat", "trans_fat", "polyunsaturated_fat", "monounsaturated_fat", "sugar", "erythritol (sweetener)", "cant_tell_fiber", "dietary_fiber", "vit_b7 (biotin)", "creatine", "L_glutamine"]
mgNutrients = ["cholesterol", "sodium", "vit_b1 (thiamine)", "vit_b2 (riboflavin)", "vit_b4 (niacin)", "vit_b5 (pantothenic_acid)", "vit_b6 (pyridoxine)", "vit_b12 (cobalamin)", "vit_c", "vit_e", "potassium", "calcium", "iron", "magnesium", "manganese", "zinc", "copper", "phosphorus", "choline", "chloride", "lycopene", "phenylalanine (EAA)", "valine (EAA)", "threonine (EAA)", "tryptophan (EAA)", "methionine (EAA)", "leucine (EAA)", "isoleucine (EAA)", "lysine (EAA)", "histidine (EAA)", "anthocyanin (antioxidant)", "quercetin (antioxidant)", "myricetin (antioxidant)", "pelargonidin (antioxidant)", "procyanidins (antioxidant)", "ellagitannins (antioxidant)", "ellagic_acid (antioxidant)", "taurine", "omega-3", "omega-6", "medium-chain triglycerides", "lutein + zeaxanthin"]
mcgNutrients = ["vit_a", "vit_b9 (folic acid)", "vit_b12 (cobalamin)", "vit_d", "vit_k", "folate", "iodine", "selenium", "molybdenum", "chromium"]
mnNutrients = ["bacillus coagulans"]

headers = ["Date", "Foods/Servings"]
# end

#Main()