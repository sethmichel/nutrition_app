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

import smoothie_sql


# thiamin = b1
# riboflaven = b2

# all graphics/widgets: grids, btns, labels for all data
class Main_Page(GridLayout):
    def __init__(self, **kwargs):
        super(Main_Page, self).__init__(**kwargs)   # this is only for if kivy code goes in the py file

        self.cols = 4

        # make btns
        new_btn = self.make_btn("Make New Smoothie")
        saved_btn = self.make_btn("Saved Recipeis")
        read_btn = self.make_btn("Read About Ingrediants")
        ingredient_btn = self.make_btn("Add Ingrediant Data")
        
        # bind btns
        new_btn.bind(on_release = self.add_ingrediant_model)
        saved_btn.bind(on_release = self.add_ingrediant_model)
        read_btn.bind(on_release = self.add_ingrediant_model)
        ingredient_btn.bind(on_release = self.add_ingrediant_model)

        # display btns
        self.add_widget(new_btn)
        self.add_widget(saved_btn)
        self.add_widget(read_btn)
        self.add_widget(ingredient_btn)

    
    # EVENT: user clicked a btn
    def add_ingrediant_model(self, instance):
        # make scrollable gridlayout
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)   # a scroll view will contain the stock gridlayout
        grid = GridLayout(cols = 2, rows = 66, size_hint_y = None)      # the gridlayout
        grid.bind(minimum_height = grid.setter("height"))   # makes the gridlayout scrollabel via the scrollview

        # make the 66 labels and txt inputs
        for i in range(0, 66):
            lab = Label(text = food())


    # called at app start by init()
    # makes & returns btns
    # pm: words = text to write
    def make_btn(self, words):
        return Button(text = words, size_hint_y = None)
        

# 25 # ?? means '+', 50 means '++'
def nutrients_db(food):
    if (food.id == "blueberries"):
        food.cals = 57
        food.protien = 0.7
        food.carbs = 14.5
        food.sugar = 10
        food.fiber = 2.4
        food.fat = 0.3
        food.vitc = 25 # ??
        food.vitk1 = 25 # ??
        food.manganese = 25 # ??
        food.anthocyanin = '+'
        food.quercetin = '+'
        food.myricetin = '+'
        return

    elif (food.id == "strawberries"):
        food.cals = 32
        food.sugar = 4.9
        food.protien = 0.7
        food.carbs = 7.7
        food.fiber = 2
        food.fat = 0.3
        food.vitc = 25 # ??
        food.vitb9 = 25 # ??
        food.potassium = 25 # ??
        food.manganese = 25 # ??
        food.pelargonidin = '+'
        food.procyanidins = '+'
        food.ellagitannins = '+'
        food.ellagic_acid = '+'
        return

    elif (food.id == "blackberries"):
        food.cals = 62
        food.sugar = 7
        food.protien = 2 
        food.carbs = 14
        food.fiber = 7.6
        food.fat = 0.7
        food.vitc = 50 # ??
        food.vitk1 = 50 # ??
        food.manganese = 50 # ?? 
        food.potassium = 25 # ??
        food.anthocyanin = '+'
        food.procyanidins = '+'
        food.ellagitannins = '+'
        food.ellagic_acid = '+' 
        return

    elif (food.id == "raspberries"):
        food.cals = 64
        food.sugar = 7
        food.protien = 1.5 
        food.carbs = 14.7
        food.fiber = 8
        food.fat = 0.8
        food.vitc = 54
        food.vitk = 12
        food.vite = 5
        food.vitb4 = 6
        food.manganese = 41
        food.iron = 5
        food.phosphorus = 4
        food.potassium = 5
        food.copper = 6
        food.anthocyanin = '+'
        food.quercetin = '+'
        food.ellagic_acid = '+'
        return

    elif (food.id == "protein_powder"):
        food.cals = 200
        food.cholesterol = 100
        food.sugar = 3
        food.protien = 30 
        food.calcium = 160
        food.fiber = 1
        food.fat = 4
        food.satfat = 1.5
        food.sodium = 190
        food.potassium = 340
        food.creatine = 1.5
        food.taurine = 1.5
        food.L_glutamine = 1.5
        return

    else: 
        print("ERROR: UNKNOWN UNGREDIANT, EVERYTHNG IS RUINED OH MOI GAWD")


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


        
class myApp(App):
    def build(self):
        return Main_Page()


if __name__ == "__main__":
    myApp().run()














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





