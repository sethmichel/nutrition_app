# some fields have ??? meaning look it up
# food won't say if it has antioxidants or EAA's
# everything is in grams or "thing"


import json
import csv
from datetime import date
from tabulate import tabulate
from colorama import Fore, Back, Style

import HelperFunctions

# need to save the names of the foods in an excel, calulcate it each time
# read, write excel
# ask user what they ate, ignore breakfast, lunch, dinner specification, just what they ate that day
# create a meal: enter the foods and amounts -> it'll add to the json

def Main():
    userInput = ""

    while (userInput != "4"):
        with open("Data/foodLog.csv", "r") as fRead: 
            f = open('Data/nutrients.json')
            jsonDict = json.load(f)
            headers = ["Date", "Foods/Servings"]
            ShowTodaysNutrients(headers, jsonDict)
            ShowTodaysFoods(headers, jsonDict)


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
def AddFoodToExcel(foodToAdd, jsonDict, headers):
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
def ShowTodaysNutrients(headers, jsonDict):
    csvDict = LoadCsvDict(headers)
    today = GetTodaysDate()
    if (csvDict[0][headers[0]] != today):
        return

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
                differenceList[-1] = f"{Back.RED}{differenceList[-1]}{Style.RESET_ALL}"
            else:
                if (difference == 0):   # it'll say " -0.0 over" otherwise
                    differenceList.append(str(difference) + " over")
                else:
                    differenceList.append(str(difference * -1) + " over")
                differenceList[-1] = f"{Back.GREEN}{differenceList[-1]}{Style.RESET_ALL}"
        else:
            differenceList.append(consumedList[-1])
    
    listHolder = AppendUnits(nutrientList, consumedList)
    nutrientList = listHolder[0]
    consumedList = listHolder[1]
    
    tableDict = {'Nutrient': nutrientList, 'Consumed': consumedList, 'Goal': differenceList}

    print("\n")
    print(tabulate(tableDict, headers = ['Nutrient', 'Consumed', 'Goal'], tablefmt = 'fancy_grid'))


# converts list of nutrients to include units
def AppendUnits(nutrientList, consumedList):
    for i in range(0, len(nutrientList)):
        if (nutrientList[i] in HelperFunctions.gNutrients):
            nutrientList[i] = nutrientList[i] + " g"
            consumedList[i] = str(consumedList[i]) + " g"
        elif (nutrientList[i] in HelperFunctions.mgNutrients):
            nutrientList[i] = nutrientList[i] + " mg"
            consumedList[i] = str(consumedList[i]) + " mg"
        elif (nutrientList[i] in HelperFunctions.mcgNutrients):
            nutrientList[i] = nutrientList[i] + " mcg"
            consumedList[i] = str(consumedList[i]) + " mcg"
        elif (nutrientList[i] in HelperFunctions.mnNutrients):
            nutrientList[i] = nutrientList[i] + " mn"
            consumedList[i] = str(consumedList[i]) + " mn"

    return [nutrientList, consumedList]


def LoadCsvDict(headers):
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


# sum ingredients into new food, save to json
def CreateFood(jsonDict):
    newFoodName = input("Enter new meal name: ")
    newFoodServingSize = input("Enter the serving size of this new food: ")
    ingreList = (input("Enter ingredients separated by a comma (no servings): ")).split(",")
    servingList = (input("Enter servings for those foods separated by a comma: ")).split(",")

    # remove leading whitespace from lists
    for i in range(0, len(ingreList)):
        ingreList[i] = ingreList[i].lstrip(" ")
        servingList[i] = servingList[i].lstrip(" ")

    f = open('Data/nutritionTemplate.json')
    jsonDict[newFoodName] = (json.load(f))["name"]

    jsonDict[newFoodName]["_is this a recipes bool"] = "t"
    jsonDict[newFoodName]["_ingredients"] = ingreList
    jsonDict[newFoodName]["_ingreServingSizes"] = servingList
    jsonDict[newFoodName]["serving size"] = newFoodServingSize

    for i in range(0, len(ingreList)):
        food = ingreList[i]
        for nutrient in jsonDict[food]:
            if (nutrient not in ["_is this a recipes bool", "_ingredients", "_ingreServingSizes", "serving size"]):
                if (nutrient == "_comments"):
                    if (jsonDict[newFoodName]["_comments"] == ""):
                        jsonDict[newFoodName]["_comments"] = jsonDict[food]["_comments"]
                    else:
                        jsonDict[newFoodName]["_comments"] = jsonDict[newFoodName]["_comments"] + ", " + jsonDict[food]["_comments"]

                # str's will either say something or be a + if I can't figure out its details
                elif (type(jsonDict[newFoodName][nutrient]) != str):
                    jsonDict[newFoodName][nutrient] += (jsonDict[food][nutrient] * float(servingList[i]))

                elif (type(jsonDict[newFoodName][nutrient]) == str):
                    if (jsonDict[newFoodName][nutrient] == ""):
                        jsonDict[newFoodName][nutrient] =  jsonDict[food][nutrient]
                    elif (jsonDict[food][nutrient] != ""):
                        jsonDict[newFoodName][nutrient] =  jsonDict[newFoodName][nutrient] + ", " + jsonDict[food][nutrient]

    jsonObj = json.dumps(jsonDict, indent = 4)
 
    with open("Data/nutrients.json", "w") as outfile:
        outfile.write(jsonObj)

    # reload jsonDict
    f = open('Data/nutrients.json')
    return json.load(f)


# list all foods eaten today under the table
def ShowTodaysFoods(headers, jsonDict):
    csvDict = LoadCsvDict(headers)
    today = GetTodaysDate()
    if (csvDict[0][headers[0]] != today):
        return

    print(str(csvDict[0][headers[1]].split('|'))[2:-2])   # [blueberries(1), blueberries(1), huel(1)]
    print("\n")





Main()