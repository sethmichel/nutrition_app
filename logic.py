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
        "folate": , ,
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

# need to save the names of the foods in an excel, calulcate it each time
# read, write excel
# ask user what they ate, ignore breakfast, lunch, dinner specification, just what they ate that day
# create a meal: enter the foods and amounts -> it'll add to the json

def Main():
    userInput = ""

    while (userInput != "4"):
        with open("foodLog.csv", "r") as fRead: 
            f = open('nutrients.json')
            jsonDict = json.load(f)
            headers = ["Date", "Foods/Servings"]
            ShowTodaysNutrients(headers, jsonDict)

            userInput = input("1: see list of foods\n" +
                            "2: create food\n" +
                            "3: delete an excel food from today\n" +
                            "4: quit\n" +
                            "OR type a food to add it to today\n")

            if (userInput == "1"):
                ListFoods()
            elif (userInput == "2"):
                jsonDict = CreateFood(jsonDict)
            elif (userInput == "3"):
                DeleteExcelEntry(userInput)
            elif (userInput =="4"):
                break
            else:
                for food in jsonDict.keys():
                    if (userInput == food):
                        AddFoodToExcel(userInput, jsonDict, headers)
                        break
                
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
def AddFoodToExcel(foodToAdd, jsonDict, headers):
    today = GetTodaysDate()   # 12/11/2019
    servings = input("How many servings? ")
    foodToAdd = foodToAdd + "(" + servings + ")"
    csvDict = LoadCsvDict(headers)

    with open("foodLog.csv", "w", newline='') as w:
        writer = csv.DictWriter(w, fieldnames = headers)

        # add food to csvDict
        if (len(csvDict) > 0 and csvDict[0][headers[0]] == today):
            csvDict[0][headers[1]] = csvDict[0][headers[1]] + '|' + foodToAdd   # 'strawberries (1)'
        else:
            csvDict.insert(0, {headers[0]: today, headers[1]: foodToAdd})   # doesn't add \n
        
        writer.writeheader()
        writer.writerows(csvDict)


# date, list of foods (servings) with , delimiter
def ShowTodaysNutrients(headers, jsonDict):
    csvDict = LoadCsvDict(headers)
    today = GetTodaysDate()
    if (csvDict[0][headers[0]] != today):
        return

    f = open('CUSTOMNutritionGoals.json')
    nutritonGoalDict = json.load(f)['goals']   # basic dictionary
    nutrientList = list(nutritonGoalDict.keys())
    todaysList = csvDict[0][headers[1]].split('|')   # [blueberries(1), blueberries(1), huel(1)]
    foodList = []
    servingsList = []
    ConsumedList = []
    goalList = []
    differenceList = []

    for i in range(0, len(todaysList)):
        startIndex = todaysList[i].index('(')
        endIndex = todaysList[i].index(')')
        servingsList.append(todaysList[i][startIndex + 1:endIndex])
        foodList.append(todaysList[i][:startIndex])
        
    for nutrient in nutrientList:
        ConsumedList.append(CalcuateFoodTotals(nutrient, foodList, servingsList, jsonDict))
        goalList.append(nutritonGoalDict[nutrient])
        if (type(ConsumedList[-1]) != str):
            difference = round(goalList[-1] - ConsumedList[-1], 3)
            if (difference > 0):
                differenceList.append(str(difference) + " Left to go")
            else:
                differenceList.append(str(difference) + " over")
        else:
            differenceList.append(ConsumedList[-1])

    tableDict = {'Nutrient': nutrientList, 'Consumed': ConsumedList, 'Goal': differenceList}

    print("\n")
    print(tabulate(tableDict, headers = ['Nutrient', 'Consumed', 'Goal'], tablefmt = 'fancy_grid'))
    print("\n")

def LoadCsvDict(headers):
    csvDict = []
    with open('foodLog.csv', "r") as r:
        reader = csv.DictReader(r)

        # load csv data
        for row in reader:
            csvDict.append({headers[0]: row[headers[0]], headers[1]: row[headers[1]]})

    return csvDict

def GetTodaysDate():
    today = str(date.today()).split("-")                  # 2019-12-11
    return (today[1] + "/" + today[2] + "/" + today[0])   # 12/11/2019

def writeTest():
    with open("foodLog.csv", "w", newline='') as w:
        writer = csv.writer(w)

        writer.writerow(["Date", "Foods/Servings"])
        writer.writerow(['11/1/2022', 'strawberries (1)'])
        writer.writerow(["10/31/2022", 'blueberries (1)'])
        w.close()


# because an apple is like 180g but reviewed as 100g. This speeds things up
# TO CALL: call it before main, speparate from the program
def WeightMutliplier(food, multiplier):
    with open("foodLog.csv", "r") as fRead: 
        f = open('nutrients.json')
        jsonDict = json.load(f)

    keyList = list(jsonDict[food].keys())

    for key in keyList:
        if (type(jsonDict[food][key]) != str):
            jsonDict[food][key] = round(jsonDict[food][key] * multiplier, 6)

    jsonObj = json.dumps(jsonDict, indent = 4)
 
    with open("nutrients.json", "w") as outfile:
        outfile.write(jsonObj)


# sum ingredients into new food, save to json
def CreateFood(jsonDict):
    newFood = input("Enter new meal name: ")
    ingreList = (input("Enter ingredients separated by a comma (no servings): blueberries,\n")).split(",")
    servingList = (input("Enter servings for those foods separated by a ,\n")).split(",")

    fgoal = open('CUSTOMNutritionGoals.json')
    nutrientList = list(json.load(fgoal)['goals'].keys())

    # calculate, serving size is "1 thing"
    jsonDict[newFood] = {"serving size": "1 thing"}
    for nutrient in nutrientList:
        jsonDict[newFood][nutrient] = CalcuateFoodTotals(nutrient, ingreList, servingList, jsonDict) 

    jsonObj = json.dumps(jsonDict, indent = 4)
 
    with open("nutrients.json", "w") as outfile:
        outfile.write(jsonObj)

    # reload jsonDict
    f = open('nutrients.json')
    return json.load(f)


#writeTest()
#WeightMutliplier("apple", 1.7)
Main()