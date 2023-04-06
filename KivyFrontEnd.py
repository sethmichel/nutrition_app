from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.core.window import Window

import CoreLogic
import Globals

# todo: show teh days food above nutrient info, give confirmation the food was added


class Main_Page(BoxLayout):
    def __init__(self, **kwargs):
        super(Main_Page, self).__init__(**kwargs)

        Window.size = (1500, 900)

        # app wide variables
        self.miscColors = [[1,1,0,1], [1,0,0,1], [1,0,1,1], [0.5,.75,.9,1], [0,1,0.3,1]]   # red, yellow, purple, light blue, green | colors for plot elements
    
        self.orientation = 'horizontal'
        leftMainBox = BoxLayout(orientation = "vertical", size_hint_x = 0.55)
        leftMainBox.add_widget(self.MakeTodaysNutrients())

        rightMainBox = BoxLayout(orientation = "vertical", size_hint_x = 0.35)
        rightMainBox.add_widget(Button(text="Create Food", size_hint_y = 0.2))
        rightMainBox.add_widget(Button(text="Delete an excel food from today", size_hint_y = 0.2))
        rightMainBox.add_widget(Button(text="Quit", size_hint_y = 0.2))

        rightUpperBox = TextInput(multiline = False, hint_text = "Add Food", size_hint_y = 0.3)
        rightUpperBox.fbind("text", self.ScrollableSearchResults)
        rightUpperBox.ids["currFoodList"] = []

        rightLowerBox = ScrollView(do_scroll_x = False, do_scroll_y = True)          # scrollview will contain the gridlayout
        grid = GridLayout(cols = 2, size_hint_y = None)
        grid.bind(minimum_height = grid.setter("height"))   # makes the gridlayout scrollabel via the scrollview
        rightLowerBox.add_widget(grid)
        
        rightMainBox.add_widget(rightUpperBox)
        rightMainBox.add_widget(rightLowerBox)
        self.add_widget(leftMainBox)
        self.add_widget(rightMainBox)



    def MakeTodaysNutrients(self):
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)   # scrollview will contain the gridlayout
        grid = GridLayout(cols = 3, size_hint_y = None)
        grid.bind(minimum_height = grid.setter("height"))              # makes the gridlayout scrollabel via the scrollview
        
        headers = ["Nutrient", "Consumed", "Goal"]
        for header in headers:
            grid.add_widget(Label(text = header, size_hint_y =  None))
        
        # 2d list [nutrientList, consumedList, differenceList]
        listHolder = CoreLogic.ShowTodaysNutrients()
        for i in range(0, len(listHolder[0])):
            grid.add_widget(Label(text = str(listHolder[0][i]), size_hint_y = None))
            grid.add_widget(Label(text = str(listHolder[1][i]), size_hint_y = None))
            grid.add_widget(Label(text = str(listHolder[2][i]), size_hint_y = None))

        scroll.add_widget(grid)

        return scroll


    # instance = textInput/rightUpperBox, userInput = text from textInput
    def ScrollableSearchResults(self, instance, userInput):
        CoreLogic.SearchForFoods(instance, userInput)
        # rightUpperBox/textinput -> mainRightBox -> rightLowerBox/scrollview -> grid
        grid = instance.parent.children[0].children[0]
        # update grid with new instance.ids["currFoodList"]
        if (len(grid.children) == 0):   # 1st time use
            for food in instance.ids["currFoodList"]:
                btn = Button(text = food)
                btn.fbind("on_release", self.ServingsChecker)
                grid.add_widget(btn)

                txt = TextInput(hint_text = "Servings", multiline = False)
                txt.fbind("text", self.UpdateFoodBtn)
                grid.add_widget(txt)
        else:
            i = 1
            while (i < len(grid.children)):
                if (grid.children[i].text not in instance.ids["currFoodList"]):
                    grid.remove_widget(grid.children[i])
                    grid.remove_widget(grid.children[i - 1])   # txtinput
                else:
                    i += 2
                    

    # fbind: food btn, checks that the user entered number of servings
    def ServingsChecker(self, instance):
        if (instance.parent.ids.get("servings") != None):
            CoreLogic.AddFoodToExcel(instance)
        else:
            self.ServingsPopUp()


    # called by ServingsChecker from the clicked foodBtn
    # user didn't enter servings for a food
    def ServingsPopUp(self):
        popup = Popup(title = "Error", title_align = "center", size_hint = (0.2, 0.2))
        
        mainBox = BoxLayout(orientation = "vertical")
        mainBox.add_widget(Label(text = "Error: Enter number of servings", size_hint_y = 0.7))
        mainBox.add_widget(Button(text = "ok", size_hint_y = 0.3, on_release=popup.dismiss))
        
        popup.content = mainBox

        popup.open()


    # fbind: called when user types in the food servings box
    # writes the text into the food btn's ids field so the btn's fbind function has it
    def UpdateFoodBtn(self, instance, servingTxt):
        instance.parent.ids["servings"] = servingTxt

        



class myApp(App):
    def build(self):
        return Main_Page()

if __name__ == "__main__":
    myApp().run()