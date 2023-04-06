from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.core.window import Window

import CoreLogic
import json

class Main_Page(BoxLayout):
    def __init__(self, **kwargs):
        super(Main_Page, self).__init__(**kwargs)

        Window.size = (1500, 900)

        with open("Data/foodLog.csv", "r") as fRead: 
            f = open('Data/nutrients.json')
            jsonDict = json.load(f)
            self.miscColors = [[1,1,0,1], [1,0,0,1], [1,0,1,1], [0.5,.75,.9,1], [0,1,0.3,1]]   # red, yellow, purple, light blue, green | colors for plot elements
        
            self.orientation = 'horizontal'
            leftbox = BoxLayout(orientation = "vertical", size_hint_x = 0.55)
            leftbox.add_widget(self.MakeTodaysNutrients(jsonDict))

            rightbox = BoxLayout(orientation = "vertical", size_hint_x = 0.35)
            rightbox.add_widget(Button(text="Create Food", size_hint_y = 0.2))
            rightbox.add_widget(Button(text="Delete an excel food from today", size_hint_y = 0.2))
            rightbox.add_widget(Button(text="Quit", size_hint_y = 0.2))
            rightbox.add_widget(TextInput(multiline = False, hint_text = "Add Food", size_hint_y = 0.2))
            
            self.add_widget(leftbox)
            self.add_widget(rightbox)


    def MakeTodaysNutrients(self, jsonDict):
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)   # scrollview will contain the gridlayout
        grid = GridLayout(cols = 3, size_hint_y = None)
        grid.bind(minimum_height = grid.setter("height"))   # makes the gridlayout scrollabel via the scrollview
        
        headers = ["Nutrient", "Consumed", "Goal"]
        for header in headers:
            grid.add_widget(Label(text = header, size_hint_y =  None))
        
        # 2d list [nutrientList, consumedList, differenceList]
        listHolder = CoreLogic.ShowTodaysNutrients(jsonDict)
        for i in range(0, len(listHolder[0])):
            grid.add_widget(Label(text = str(listHolder[0][i]), size_hint_y = None))
            grid.add_widget(Label(text = str(listHolder[1][i]), size_hint_y = None))
            grid.add_widget(Label(text = str(listHolder[2][i]), size_hint_y = None))

        scroll.add_widget(grid)
        return scroll





class myApp(App):
    def build(self):
        return Main_Page()

if __name__ == "__main__":
    myApp().run()