# nutrition_app

todo: make the table nicer (colors)

Command line program that tracks 67 nutrients. Made because every nutrition tracker either isn't detailed enough, is 90% ads, or both. Official2000CalorieNutritionGoals.json is the actual doctor reccommended amount for an adult male. Custom2000CalorieNutritionGoals.json is custom to me

* You research and add nutrition info for basic foods to nutrients.json. Daily logs are stored in foodLog.csv (manually editing this csv may introduce new characters like \t or \n and mess everything up)


* Use the CreateFood() method to combine nutrients.json foods into complex foods like smoothies

* Use the WeightMutliplier() method to adjust the serving size which proportionally changes that foods nutrients

Didn't add a ui because it's only for me and I won't be using it much

![Screenshot](https://raw.githubusercontent.com/sethmichel/nutrition_app/main/pics/terminal_pic_1.png)
![Screenshot](https://raw.githubusercontent.com/sethmichel/nutrition_app/main/pics/terminal_pic_2.png)
