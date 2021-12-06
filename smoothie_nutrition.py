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

# changeing the btns around is so messed up


try:
    print('\nConnecting to the PostgreSQL database...')
    conn = psycopg2.connect(**config())
    cur = conn.cursor()
    
    print('PostgreSQL database version: ')
    cur.execute('SELECT version()')
    print(cur.fetchone())

    dbTableNames = sqlCommands.GetTableNames(cur, conn)
    sqlCommands.CreateTables(cur, conn, dbTableNames)

except (Exception, psycopg2.DatabaseError) as error:
    print("error ", error)


class Main_Page(GridLayout):
    def __init__(self, **kwargs):
        super(Main_Page, self).__init__(**kwargs)

        self.cols = 4

        self.uiTableNames = self.FormatHeaders()
        self.allHeaders = self.GetSchemas()         # dictionary of lists with all table headers
        self.nutrientData = sqlCommands.GetNutrientData(conn, cur)

        self.add_widget(Button(text = "Make New Smoothie", size_hint_y = None))
        self.add_widget(Button(text = "Saved Recipes", size_hint_y = None))
        self.add_widget(Button(text = "Read About Nutrients", size_hint_y = None, on_release = self.ReadNutrients))
        self.add_widget(Button(text = "Add Ingrediant Data", size_hint_y = None, on_release = self.AddIngredient))


    # user clicked the add an ingredients btn
    def AddIngredient(self, instance):
        sm = ScreenManager()
        mainView = ModalView(size_hint = (0.9, 0.9))

        # make the screens
        for i in range(0, len(self.uiTableNames)):
            if (self.uiTableNames[i] != "nutrient_info"):
                screen = Screen(name = self.uiTableNames[i])
                
                layout = BoxLayout(orientation = "vertical")
                grid = GridLayout(cols = 7, size_hint_y = 0.8)

                # load grids (probably better as a boxlayout so it's dynamic sizes tbh)
                for j in range(0, len(self.allHeaders[self.uiTableNames[i]])):
                    grid.add_widget(Label(text = self.allHeaders[self.uiTableNames[i]][j], size_hint_y = 0.2))
                for j in range(0, len(self.allHeaders[self.uiTableNames[i]])):
                    grid.add_widget(TextInput(size_hint_y = 0.2))

                btnLayout = GridLayout(rows = 1, cols = 3, size_hint_y = 0.1)            
                backBtn = Button(text = "Back", size_hint_x = 0.1, ids = {"name": "back"})
                testBtn = Button(text = "test", size_hint_x = 0.1, ids = {"name": "test"})
                backBtn.fbind("on_release", self.NextBtnEvent, sm)
                testBtn.fbind("on_release", self.MakeTestData, grid)
                btnLayout.add_widget(backBtn)
                btnLayout.add_widget(testBtn)

                if (i < len(self.uiTableNames) - 1):
                    nextBtn = Button(text = "Next", size_hint_x = 0.8, ids = {"name": "next"})
                    nextBtn.fbind("on_release", self.NextBtnEvent, sm)
                    btnLayout.add_widget(nextBtn)
                else:
                    submitBtn = Button(text = "Submit", size_hint_x = 0.7, ids = {"name": "submit"})
                    submitBtn.fbind("on_release", sqlCommands.SendIngredientData, conn, cur, self.allHeaders, dbTableNames, sm)
                    btnLayout.add_widget(submitBtn)
                
                layout.add_widget(Label(text = self.uiTableNames[i], size_hint_y = 0.1))
                layout.add_widget(grid)
                layout.add_widget(btnLayout)
                screen.add_widget(layout)
                sm.add_widget(screen)

        sm.screens[0].children[0].children[0].children[2].disabled = True    # basic info (1st screens) back btn
        mainView.add_widget(sm)
        mainView.open()


    # send data to sql, change ui
    # sm is screen manager
    def NextBtnEvent(self, sm, instance):
        # header label, and change grids
        if (sm.current == "Basic Info"):
            sm.transition.direction = 'left'
            sm.current = "Vitamins and Minerals"

        elif (sm.current == "Vitamins and Minerals"):
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
                sm.current = "Vitamins and Minerals"
            
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


    # user clicked the read about nutrients btn
    def ReadNutrients(self, instance):
        mainview = ModalView(size_hint = (0.75, 0.75))
        layout = BoxLayout(orientation = "vertical")

        # search bar grid
        searchGrid = GridLayout(rows = 1, cols = 1, size_hint_y = 0.1)
        txt = TextInput(hint_text = "Ingredient...")
        txt.fbind("text", self.SearchIngredient, layout)   # text callback also passes the actual text as a para
        searchGrid.add_widget(txt)

        # upper grid of buttons
        upperGrid = GridLayout(rows = 1, cols = 5, size_hint_y = 0.15)
        basicInfoBtn = Button(text = "Basic Info")
        antioxidantsBtn = Button(text = "Antioxidants")
        vitMinBtn = Button(text = "VitaminMinerals")
        miscInfo = Button(text = "Misc Info")
        allBtn = Button(text = "All", background_color = [0, 255, 255, 0.4])

        basicInfoBtn.fbind("on_release", self.ReadNutrientsChangeLowerGrid, layout)
        antioxidantsBtn.fbind("on_release", self.ReadNutrientsChangeLowerGrid, layout)
        vitMinBtn.fbind("on_release", self.ReadNutrientsChangeLowerGrid, layout)
        miscInfo.fbind("on_release", self.ReadNutrientsChangeLowerGrid, layout)
        allBtn.fbind("on_release", self.ReadNutrientsChangeLowerGrid, layout)

        upperGrid.add_widget(basicInfoBtn)
        upperGrid.add_widget(antioxidantsBtn)
        upperGrid.add_widget(vitMinBtn)
        upperGrid.add_widget(miscInfo)
        upperGrid.add_widget(allBtn)

        # lower grid
        grid = GridLayout(cols = 4, size_hint_y = None)
        grid.bind(minimum_height = grid.setter("height"))
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)

        # combine stuff
        scroll.add_widget(grid)
        layout.add_widget(searchGrid)
        layout.add_widget(upperGrid)
        layout.add_widget(scroll)

        # populate
        self.ReadNutrientsChangeLowerGrid(layout, "All")

        mainview.add_widget(layout)
        mainview.open()


    # instance: if user just landed on this screen "all" is default so instance is a string "all"
    # if user clicks a btn to limit results, instance is the btn clicked
    def ReadNutrientsChangeLowerGrid(self, layout, instance):
        # start screen (only happens once)
        if (instance == "All"):
            for table in self.uiTableNames:
                for cell in self.allHeaders[table]:
                    if (cell != "name" and cell != "info"):
                        layout.children[0].children[0].add_widget(Button(text = cell, size_hint_y = None, on_release = self.NutrientInfoModel))
            
        # user cliked a btn (the table is guarenteed to have been made already)
        else:
            btnList = []
            self.colorChanger(instance)

            if (instance.text == "All"): 
                for table in self.uiTableNames:
                    for cell in self.allHeaders[table]:
                        if (cell != "name" and cell != "info"):
                            btnList.append(cell)

            elif (instance.text == "Basic Info"):
                btnList = self.allHeaders["Basic Info"]
            elif (instance.text == "Antioxidants"):
                btnList = self.allHeaders["Antioxidants"]
            elif (instance.text == "VitaminMinerals"):
                btnList = self.allHeaders["Vitamins and Minerals"]
            else:
                btnList = self.allHeaders["Misc Info"]

            if ("name" in btnList): btnList.remove("name")
            if ("info" in btnList): btnList.remove("info")
            
            # if a layout btn isn't in btnList -> delete it from layout
            # if a layout btn is in btnList -> delete it from btnList
            # then add whatevers left in btnList to layout
            # NOTE: kivy was glitching and showing random cells from other tables when I did this via another, more
            #       efficient, way. there was no error in my code so I switched to using clear()
            layout.children[0].children[0].children.clear()
            for cell in btnList:
                layout.children[0].children[0].add_widget(Button(text = cell, size_hint_y = None, on_release = self.NutrientInfoModel))

            print(btnList)
            



    # this should be editable
    # modelView from read ingredients buttons
    def NutrientInfoModel(self, instance):
        # if edited, update sql
        mainview = ModalView(size_hint = (0.75, 0.75))
        layout = BoxLayout(orientation = "vertical")

        upperGrid = GridLayout(cols = 3, size_hint_y = 0.15)
        upperGrid.add_widget(Label(text = instance.text, size_hint_x = 0.8))   # how do I center this?
        upperGrid.add_widget(Button(text = "Edit", size_hint_x = 0.1, on_release = self.EditEnabler))
        closeBtn = Button(text = "X", size_hint_x = 0.1)
        closeBtn.fbind("on_release", self.CloseNutrientInfo)
        upperGrid.add_widget(closeBtn)

        layout.add_widget(upperGrid)
        layout.add_widget(TextInput(text = self.nutrientData[instance.text], readonly = True))
        mainview.add_widget(layout)
        mainview.open()


    # enables textinputs editing in the layout
    def EditEnabler(self, instance):
        # btn, gridlayout, boxlayout, textinput
        instance.parent.parent.children[0].readonly = False


    # if things have been edited, do a pop up asking if they want to save
    # popups can only have 1 widget in content, so I gotta use a gridlayout
    def CloseNutrientInfo(self, instance):
        # btn, gridlayout, boxlayout, textinput
        if (instance.parent.parent.children[0].disabled == False):
            layout = GridLayout(cols = 2)
            layout.add_widget(Button(text = "Save"))
            layout.add_widget(Button(text = "Close"))

            popup = Popup(title = "Save Changes?", title_align = "center", content = layout, size_hint = (0.4, 0.2))
            
            popup.open()


    def SearchIngredient(self, layout, instance, text):
        length = len(text)
        text = text.lower()
        listHolder = layout.children[0].children[0].children
        endIndex = len(listHolder)   # -1 didn't work for end of list, so I use this

        for i in range(1, len(listHolder)):
            if (listHolder[i].text[:length] == text):
                btnHolder = layout.children[0].children[0].children.pop(i)
                btnHolder.parent = None
                layout.children[0].children[0].add_widget(btnHolder, endIndex)


    def bulkUpload(self):
       pass


    # these are helpers ------------------------------------------------------------------------------

    # read about ingredients helper
    def colorChanger(self, instance):
        for btn in instance.parent.children:
            if (btn.background_color == [0, 255, 255, 0.4]):
                btn.background_color = [1, 1, 1, 1]
                break

        instance.background_color = [0, 255, 255, 0.4]


    # a little messy, but I just prefer to have the ui table names as the keys instead of db table names
    def GetSchemas(self):
        holder = {}
        for i in range(0, len(dbTableNames)):
            holder[self.uiTableNames[i]] = sqlCommands.GetTableSchema(cur, conn, dbTableNames[i])

        return holder


    def FormatHeaders(self):
        uiTableNames = []
        for i in range(0, len(dbTableNames)):
            uiTableNames.append(dbTableNames[i].replace('_', ' '))
            uiTableNames[i] = uiTableNames[i].replace("'", "@")   # title function has issues with ', so temp replacing it
            uiTableNames[i] = uiTableNames[i].title()
            uiTableNames[i] = uiTableNames[i].replace("@", "'")
            if (uiTableNames[i] == "Vitamins Minerals"):
                uiTableNames[i] = "Vitamins and Minerals"
        
        return uiTableNames


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


