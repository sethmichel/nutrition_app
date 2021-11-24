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

import psycopg2
from config import config

import sqlCommands


# WARNING: this repo uses a database.ini file to connect to the db, this isn't uploaded to github for security reasons so make your own connection


# connects to the db and prints pgsql version
conn = None

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

    sqlCommands.create_table(cur, conn)

except (Exception, psycopg2.DatabaseError) as error:
    print("error ", error)


# all graphics/widgets: grids, btns, labels for all data
class Main_Page(GridLayout):
    def __init__(self, **kwargs):
        super(Main_Page, self).__init__(**kwargs)   # this is only for if kivy code goes in the py file

        self.cols = 4

        # make btns
        new_btn = self.MakeBtn("Make New Smoothie")
        saved_btn = self.MakeBtn("Saved Recipeis")
        read_btn = self.MakeBtn("Read About Ingrediants")
        ingredient_btn = self.MakeBtn("Add Ingrediant Data")
        
        # bind btns
        read_btn.bind(on_release = self.ReadIngredients)
        ingredient_btn.bind(on_release = self.AddIngredientModel)

        # display btns
        self.add_widget(new_btn)
        self.add_widget(saved_btn)
        self.add_widget(read_btn)
        self.add_widget(ingredient_btn)


    # called at app start by init()
    def MakeBtn(self, words):
        return Button(text = words, size_hint_y = None)


    # EVENT: user clicked the add an ingredients btn
    def AddIngredientModel(self, instance):
        mainview = ModalView(size_hint = (0.75, 0.75))
        layout = BoxLayout(orientation = "vertical")
        layout.add_widget(Label(text = "Add Ingrediant Data", size_hint_y = 0.2))
        enterBtn = Button(text = "Submit", size_hint_y = 0.1)
        
        # make scrollable gridlayout
        grid = GridLayout(rows = 50, cols = 7, size_hint_y = 0.7)
        grid.bind(minimum_height = grid.setter("height"))               # makes the gridlayout scrollabel via the scrollview
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)    # a scroll view will contain the gridlayout
        
        ingredientList = ["Food", 'Calories', 'Protein (g)', 'Carbs (g)', 'Sugar (g)', 'Fiber (g)', 'Total Fat (g)']
        for i in ingredientList:
            grid.add_widget(Label(text = i))
        for i in range(0, 7):
            grid.add_widget(TextInput())

        enterBtn.fbind("on_release", sqlCommands.sendIngredientData, conn, cur)
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        layout.add_widget(enterBtn)
        mainview.add_widget(layout)
        mainview.open()


    # EVENT: user clicked the read about ingredients btn
    def ReadIngredients(self, instance):
        mainview = ModalView(size_hint = (0.75, 0.75))
        layout = BoxLayout(orientation = "vertical")

        # search bar
        searchGrid = GridLayout(rows = 1, cols = 2, size_hint_y = 0.1)
        searchGrid.add_widget(TextInput(hint_text = "ingredient...", size_hint_x = 0.8))
        searchGrid.add_widget(Button(text = "Search", size_hint_x = 0.2))
        searchGrid.children[0].bind(on_release = self.SearchIngredient)

        layout.add_widget(searchGrid)
        layout.add_widget(self.ReadIngredientsUpperGrid())
        layout.add_widget(self.ReadIngredientsLowerGrid())

        mainview.add_widget(layout)
        mainview.open()


    # default is display all
    # for all, food is headers, ingredients is rows. Tap a col and it'll highlight that whole col
    # > for easier scrolling
    def ReadIngredientsLowerGrid(self):
        # make scrollable gridlayout
        grid = GridLayout(cols = 7, size_hint_y = 0.7)
        grid.bind(minimum_height = grid.setter("height"))
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)

        # get list of foods as headers
        # get list of ingredients as cols
        # insert data

        return scroll


    # returns the uppder grid of btns for the read ingredients menu
    def ReadIngredientsUpperGrid(self):
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

        return upperGrid
    
    
    def SearchIngredient(self, instance):
        pass

    def colorChanger(self, instance):
        for btn in instance.parent.children:
            if (btn.background_color == [0, 255, 255, 0.4]):
                btn.background_color = [1, 1, 1, 1]
                break

        instance.background_color = [0, 255, 255, 0.4]



    def bulkUpload(self):
       pass



        
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





