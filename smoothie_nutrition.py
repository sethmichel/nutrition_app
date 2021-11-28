from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

import random
import psycopg2
from config import config

import sqlCommands


# WARNING: this repo uses a database.ini file to connect to the db, this isn't uploaded to github for security reasons so make your own connection


# connects to the db and prints pgsql version
conn = None
tableNames = []
originalSchema = []
editedSchema = []

try:
    params = config() # this is the config library
    conn = psycopg2.connect("dbname='nutritionDB' user='postgres' host='localhost' password='1234'")

    # connect to the PostgreSQL server
    print('\nConnecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    cur = conn.cursor()
    
    # execute a statement
    print('PostgreSQL database version: ')
    cur.execute('SELECT version()')

    # display the PostgreSQL db server version
    db_version = cur.fetchone()
    print(db_version)

    sqlCommands.CreateTables(cur, conn)

except (Exception, psycopg2.DatabaseError) as error:
    print("error ", error)


# all graphics/widgets: grids, btns, labels for all data
class Main_Page(GridLayout):
    def __init__(self, **kwargs):
        super(Main_Page, self).__init__(**kwargs)   # this is only for if kivy code goes in the py file

        self.cols = 4

        # make btns
        new_btn = Button(text = "Make New Smoothie", size_hint_y = None)
        saved_btn = Button(text = "Saved Recipeis", size_hint_y = None)
        read_btn = Button(text = "Read About Ingrediants", size_hint_y = None)
        ingredient_btn = Button(text = "Add Ingrediant Data", size_hint_y = None)
        
        # bind btns
        read_btn.bind(on_release = self.ReadIngredients)
        ingredient_btn.bind(on_release = self.AddIngredient)

        # display btns
        self.add_widget(new_btn)
        self.add_widget(saved_btn)
        self.add_widget(read_btn)
        self.add_widget(ingredient_btn)


    # EVENT: user clicked the add an ingredients btn
    def AddIngredient(self, instance):
        originalSchema = []

        tableNames = sqlCommands.GetTableNames(cur, conn)

        if (originalSchema == []):
            self.GetSchemas()

        sm = ScreenManager()
        mainView = ModalView(size_hint = (0.9, 0.9))
        names = ["Basic Info", "Vitamins And Minerals", "Antioxidants", "Misc Nutrients", "Misc Info"]

        # make the screens
        for i in range(0, len(names)):
            screen = Screen(name = names[i])
            
            layout = BoxLayout(orientation = "vertical")
            grid = GridLayout(cols = 7, size_hint_y = 0.8)

            # load grids (probably better as a boxlayout so it's dynamic sizes tbh)
            for j in range(0, len(editedSchema[i])):
                grid.add_widget(Label(text = editedSchema[i][j], size_hint_y = 0.2))
            for j in range(0, len(editedSchema[i])):
                grid.add_widget(TextInput(size_hint_y = 0.2))

            btnLayout = GridLayout(rows = 1, cols = 3, size_hint_y = 0.1)            
            backBtn = Button(text = "Back", size_hint_x = 0.1, ids = {"name": "back"})
            testBtn = Button(text = "test", size_hint_x = 0.1, ids = {"name": "test"})
            backBtn.fbind("on_release", self.NextBtnEvent, sm)
            testBtn.fbind("on_release", self.MakeTestData, grid)
            btnLayout.add_widget(backBtn)
            btnLayout.add_widget(testBtn)

            if (i < len(names) - 1):
                nextBtn = Button(text = "Next", size_hint_x = 0.8, ids = {"name": "next"})
                nextBtn.fbind("on_release", self.NextBtnEvent, sm)
                btnLayout.add_widget(nextBtn)
            else:
                submitBtn = Button(text = "Submit", size_hint_x = 0.7, ids = {"name": "submit"})
                submitBtn.fbind("on_release", sqlCommands.SendIngredientData, conn, cur, originalSchema, tableNames, sm)
                btnLayout.add_widget(submitBtn)
            
            layout.add_widget(Label(text = names[i], size_hint_y = 0.1))
            layout.add_widget(grid)
            layout.add_widget(btnLayout)
            screen.add_widget(layout)
            sm.add_widget(screen)

        mainView.add_widget(sm)
        mainView.open()

    # send data to sql, change ui
    # sm is screen manager
    def NextBtnEvent(self, sm, instance):
        # header label, and change grids
        if (sm.current == "Basic Info"):
            sm.transition.direction = 'left'
            sm.current = "Vitamins And Minerals"    

        elif (sm.current == "Vitamins And Minerals"):
            if (instance.ids["name"] == "next"):
                sm.transition.direction = 'left'
                sm.current = "Antioxidants"
            else:
                sm.transition.direction = 'right'
                sm.current = "Basic Info"

        elif (sm.current == "Antioxidants"):
            if (instance.ids["name"] == "next"):
                sm.transition.direction = 'left'
                sm.current = "Misc Nutrients"
            else:
                sm.transition.direction = 'right'
                sm.current = "Vitamins And Minerals"
            
        elif (sm.current == "Misc Nutrients"):
            if (instance.ids["name"] == "next"): 
                sm.transition.direction = 'left'
                sm.current = "Misc Info"
            else: 
                sm.transition.direction = 'right'
                sm.current = "Antioxidants"
        else:
            sm.transition.direction = 'right'
            sm.current = "Misc Nutrients"
                








    # EVENT: user clicked the read about ingredients btn
    def ReadIngredients(self, instance):
        mainview = ModalView(size_hint = (0.75, 0.75))
        layout = BoxLayout(orientation = "vertical")

        # search bar grid
        searchGrid = GridLayout(rows = 1, cols = 2, size_hint_y = 0.1)
        searchGrid.add_widget(TextInput(hint_text = "ingredient...", size_hint_x = 0.8))
        searchGrid.add_widget(Button(text = "Search", size_hint_x = 0.2))
        searchGrid.children[0].bind(on_release = self.SearchIngredient)

        # upper grid of buttons
        upperGrid = GridLayout(rows = 1, cols = 5, size_hint_y = 0.2)

        basicInfoBtn = Button(text = "Basic Info")
        antioxidantsBtn = Button(text = "Antioxidants")
        vitaminMineralsBtn = Button(text = "vitaminMinerals")
        miscInfoBtn = Button(text = "Misc Info")
        allBtn = Button(text = "All")

        basicInfoBtn.bind(on_release = self.colorChanger)
        antioxidantsBtn.bind(on_release = self.colorChanger)
        vitaminMineralsBtn.bind(on_release = self.colorChanger)
        miscInfoBtn.bind(on_release = self.colorChanger)
        allBtn.bind(on_release = self.colorChanger)

        upperGrid.add_widget(basicInfoBtn)
        upperGrid.add_widget(antioxidantsBtn)
        upperGrid.add_widget(vitaminMineralsBtn)
        upperGrid.add_widget(miscInfoBtn)
        upperGrid.add_widget(allBtn)

        # combine stuff
        layout.add_widget(searchGrid)
        layout.add_widget(upperGrid)
        layout.add_widget(self.HelperReadIngredientsLowerGrid())

        mainview.add_widget(layout)
        mainview.open()


    # default is display basic info
    # nutrient is row headers, the other cols is the info. Click it to open a popup with the info
    def ReadIngredientsLowerGrid(self):
        # make scrollable gridlayout
        grid = GridLayout(cols = 2, size_hint_y = 0.7)
        grid.bind(minimum_height = grid.setter("height"))
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)

        # get list of foods as headers
        for i in editedSchema[0][1:]:
            grid.add_widget(Label(text = i, size_hint_x = 0.2))
            grid.add_widget(Label())

        # get list of ingredients as cols
        # insert data

        # I need anohter table of nutrient info, just 2 cols, every nutrient from each tabel. Need that first


        scroll.add_widget(grid)

        return scroll


    
    
    def SearchIngredient(self, instance):
        pass





    def bulkUpload(self):
       pass




    # these are helpers ------------------------------------------------------------------------------

    # add ingredient helper
    def OrganizeList(self, tableSchema):
        newList = []

        for i in tableSchema:
            newList.append(i[0])
            newList[-1] = newList[-1].replace("_", " ")
            if (newList[-1] != "name" and newList[-1] != "calories" and newList[-1] != "info"):
                if (newList[-1] == "cholesterol" or newList[-1] == "sodium"):
                    newList[-1] = newList[-1] + ' mg'
                else:
                    newList[-1] = newList[-1] + ' g'
            
        return newList
            

    # read about ingredients helper
    def colorChanger(self, instance):
        for btn in instance.parent.children:
            if (btn.background_color == [0, 255, 255, 0.4]):
                btn.background_color = [1, 1, 1, 1]
                break

        instance.background_color = [0, 255, 255, 0.4]


    def GetSchemas(self):
        originalSchema.append(sqlCommands.GetTableSchema(cur, conn, tableNames[0]))
        originalSchema.append(sqlCommands.GetTableSchema(cur, conn, tableNames[1]))
        originalSchema.append(sqlCommands.GetTableSchema(cur, conn, tableNames[2]))
        originalSchema.append(sqlCommands.GetTableSchema(cur, conn, tableNames[3]))
        originalSchema.append(sqlCommands.GetTableSchema(cur, conn, tableNames[4]))

        editedSchema.append(self.OrganizeList(originalSchema[0]))
        editedSchema.append(self.OrganizeList(originalSchema[1]))
        editedSchema.append(self.OrganizeList(originalSchema[2]))
        editedSchema.append(self.OrganizeList(originalSchema[3]))
        editedSchema.append(self.OrganizeList(originalSchema[4]))


    # test data for add ingredient screens
    def MakeTestData(self, grid, instance):
        # textinputs are the first half of grids children. ex) first 8 of 16
        for i in range(0, len(grid.children) // 2):
            grid.children[i].text = str(random.randrange(0, 51))
        



class myApp(App):
    def build(self):
        return Main_Page()


if __name__ == "__main__":
    myApp().run()

    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()
        print('\nDatabase connection closed')













# thiamin = b1
# riboflaven = b2
def smoothie_adder(food, smoothie):
    smoothie.cals += food.cals
    smoothie.sugar += food.sugar
    smoothie.added_sugar += food.added_sugar
    smoothie.fiber += food.fiber
    smoothie.fat += food.fat
    smoothie.satfat += food.satfat
    smoothie.cholesterol += food.cholesterol
    smoothie.sodium += food.sodium

    smoothie.vita += food.vita
    smoothie.vitb9 += food.vitb9
    smoothie.vitb4 += food.vitb4
    smoothie.vitb_mystery += food.vitb_mystery
    smoothie.vitc += food.vitc
    smoothie.vitd += food.vitd
    smoothie.vite += food.vite
    smoothie.vitk1 += food.vitk1

    smoothie.calcium += food.calcium
    smoothie.manganese += food.manganese
    smoothie.potassium += food.potassium
    smoothie.iron += food.iron
    smoothie.phosphorus += food.phosphorus
    smoothie.copper += food.copper
    smoothie.zinc += food.zinc
    smoothie.creatine += food.creatine
    smoothie.taurine += food.taurine
    smoothie.L_glutamine += food.L_glutamine

    # these are strs, just a '+' or '++' if they have a ton
    smoothie.anthocyanin =  smoothie.anthocyanin + food.anthocyanin
    smoothie.quercetin =  smoothie.quercetin + food.quercetin
    smoothie.myricetin =  smoothie.myricetin + food.myricetin
    smoothie.pelargonidin =  smoothie.pelargonidin + food.pelargonidin
    smoothie.procyanidins =  smoothie.procyanidins + food.procyanidins
    smoothie.ellagitannins =  smoothie.ellagitannins + food.ellagitannins
    smoothie.ellagic_acid =  smoothie.ellagic_acid + food.ellagic_acid
    

# prints the smoothie facts
def printer(smoothie):
    print('cals: ', smoothie.cals)
    print('sugar: ', smoothie.sugar, 'g')
    print('added sugar: ', smoothie.added_sugar, 'g')
    print('fiber: ', smoothie.fiber, 'g')
    print('total fat: ', smoothie.fat, 'g')
    print('sat fat: ', smoothie.satfat, 'g')
    print('cholesterol: ', smoothie.cholesterol, 'mg')
    print('sodium: ', smoothie.sodium, 'mg\n')

    print('vita: ', smoothie.vita, '%')
    print('vitb9: ', smoothie.vitb9, '%')
    print('vitb4: ', smoothie.vitb4, '%')
    print('vitb_mystery: ', smoothie.vitb_mystery, '%')
    print('vitc: ', smoothie.vitc, '%')
    print('vitd: ', smoothie.vitd, '%')
    print('vite: ', smoothie.vite, '%')
    print('vitk1: ', smoothie.vitk1, '%\n')

    print('calcium: ', smoothie.calcium, '%')
    print('manganese: ', smoothie.manganese, '%')
    print('potassium: ', smoothie.potassium, '%')
    print('iron: ', smoothie.iron, '%')
    print('phosphorus: ', smoothie.phosphorus, '%')
    print('copper: ', smoothie.copper, '%')
    print('zinc: ', smoothie.zinc, '%')
    print('creatine: ', smoothie.creatine, 'g')
    print('taurine: ', smoothie.taurine, 'g')
    print('L_glutamine: ', smoothie.L_glutamine, 'g\n')

    print("Anti-Oxidents\n")

    print('anthocyanin: ', smoothie.anthocyanin)
    print('quercetin: ', smoothie.quercetin)
    print('myricetin: ', smoothie.myricetin)
    print('pelargonidin: ', smoothie.pelargonidin)
    print('procyanidins: ', smoothie.procyanidins)
    print('ellagitannins: ', smoothie.ellagitannins)
    print('ellagic_acid: ', smoothie.ellagic_acid)


def main():
    blueberries = ingrediants("blueberries")
    strawberries = ingrediants("strawberries")
    blackberries = ingrediants("blackberries")
    raspberries = ingrediants("raspberries")
    protein_powder = ingrediants("protein_powder")
    smoothie = ingrediants("smoothie")

    ingrediant_list = []
    ingrediant_list.append(blueberries)
    ingrediant_list.append(strawberries)
    ingrediant_list.append(blackberries)
    ingrediant_list.append(raspberries)
    ingrediant_list.append(protein_powder)
    
    for i in ingrediant_list:
        nutrients_db(i)
    
    for i in ingrediant_list:
        smoothie_adder(i, smoothie)

    printer(smoothie)

    print("\n\npause")


        















'''
    for i in ingrediants_list:
        if (i.vita != 0): smoothie.vita += i.vita

        if (i.vitb9 != 0): smoothie.vitb9 += i.
        if (i.vitb4 != 0): smoothie.vitb4 += i.
        if (i.vitb_mystery != 0): smoothie.vitb_mystery += i.
        if (i.vitc != 0): smoothie.vitc += i.
        if (i.vitd != 0): smoothie.vitd += i.
        if (i.vite != 0): smoothie.vite += i.
        if (i.vitk1 != 0): smoothie.vitk1 += i.

        if (i.calcium != 0): smoothie.calcium += i.
        if (i.manganese != 0): smoothie.manganese += i.
        if (i.potassium != 0): smoothie.potassium += i.
        if (i.iron != 0): smoothie.iron += i.
        if (i.phosphorus != 0): smoothie.phosphorus += i.
        if (i.copper != 0): smoothie.copper += i.
        if (i.zinc != 0): smoothie.zinc += i.
        if (i.creatine != 0): smoothie.creatine += i.
        if (i.taurine != 0): smoothie.taurine += i.
        if (i.L_glutamine != 0): smoothie.L_glutamine += i.

        if (i.anthocyanin != 0): smoothie.anthocyanin += i.
        if (i.quercetin != 0): smoothie.quercetin += i.
        if (i.myricetin != 0): smoothie.myricetin += i.
        if (i.pelargonidin != 0): smoothie.pelargonidin += i.
        if (i.procyanidins != 0): smoothie.procyanidins += i.
        if (i.ellagitannins != 0): smoothie.ellagitannins += i.
        if (i.ellagic_acid != 0): smoothie.ellagic_acid += 

    blackberries.cals = 32
    blackberries.sugar =
    blackberries.protien = 
    blackberries.carbs = 
    blackberries.fiber = 
    blackberries.fat = 
    blackberries.vitc = 
    blackberries.vitk1 = 
    blackberries.manganese = 
    blackberries.anthocyanin = 
    blackberries.quercetin = 
    blackberries.myricetin = 

    blackberries.cals = 32
    blackberries.sugar =
    blackberries.protien = 
    blackberries.carbs = 
    blackberries.fiber = 
    blackberries.fat = 
    blackberries.vitc = 
    blackberries.vitk1 = 
    blackberries.manganese = 
    blackberries.anthocyanin = 
    blackberries.quercetin = 
    blackberries.myricetin = 

    blackberries.cals = 32
    blackberries.sugar =
    blackberries.protien = 
    blackberries.carbs = 
    blackberries.fiber = 
    blackberries.fat = 
    blackberries.vitc = 
    blackberries.vitk1 = 
    blackberries.manganese = 
    blackberries.anthocyanin = 
    blackberries.quercetin = 
    blackberries.myricetin = 

    blackberries.cals = 32
    blackberries.sugar =
    blackberries.protien = 
    blackberries.carbs = 
    blackberries.fiber = 
    blackberries.fat = 
    blackberries.vitc = 
    blackberries.vitk1 = 
    blackberries.manganese = 
    blackberries.anthocyanin = 
    blackberries.quercetin = 
    blackberries.myricetin = 

    blackberries.cals = 32
    blackberries.sugar =
    blackberries.protien = 
    blackberries.carbs = 
    blackberries.fiber = 
    blackberries.fat = 
    blackberries.vitc = 
    blackberries.vitk1 = 
    blackberries.manganese = 
    blackberries.anthocyanin = 
    blackberries.quercetin = 
    blackberries.myricetin = 
'''





