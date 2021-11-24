import psycopg2
from config import config

# create a table if one doesn't exist
def create_table(cur, conn):
    try:
        # thiamin = b1
        # riboflavin = b2
        # test if the table exists
        vitMineralTable = """
        CREATE TABLE vitaminMinerals (name VARCHAR(30), vitA VARCHAR(30), vitB1 VARCHAR(30), vitB2 VARCHAR(30), vitB3 VARCHAR(30), vitB4 VARCHAR(30), 
        vitB6 VARCHAR(30), vitB9 VARCHAR(30), vitB12 VARCHAR(30), vitC VARCHAR(30), vitD VARCHAR(30), vitE VARCHAR(30), vitK1 VARCHAR(30), 
        calcium VARCHAR(30), niacin VARCHAR(30), folate VARCHAR(30), manganese VARCHAR(30), magnesium VARCHAR(30), biotin VARCHAR(30), 
        pantonthenic_acid VARCHAR(30), iron VARCHAR(30), potassium VARCHAR(30), iodine VARCHAR(30), phosphorus VARCHAR(30), copper VARCHAR(30), 
        selenium VARCHAR(30), zinc VARCHAR(30), chromium VARCHAR(30), molydhenum VARCHAR(30), chloride VARCHAR(30), silicon VARCHAR(30), 
        lycopene VARCHAR(30), lutein VARCHAR(30), boron VARCHAR(30), vanadium VARCHAR(30), nickel VARCHAR(30))"""

        antioxidantTable = """
        CREATE TABLE antioxidants (name VARCHAR(30), anthocyanin VARCHAR(30), quercetin VARCHAR(30), myricetin VARCHAR(30), pelargonidin VARCHAR(30), 
        procyanidins VARCHAR(30), ellagitannins VARCHAR(30), ellagic_acid VARCHAR(30))"""

        miscNutrientsTable = """
        CREATE TABLE miscNutrients (name VARCHAR(30), omega3 VARCHAR(30), creatine VARCHAR(30), taurine VARCHAR(30), l_glutamine VARCHAR(30), 
        artificial_flavors VARCHAR(30), artificial_colors VARCHAR(30), artificial_sweeteners VARCHAR(30))"""
        
        BasicTable = """
        CREATE TABLE basicInfo (name VARCHAR(30), calories VARCHAR(30), protein VARCHAR(30), carbs VARCHAR(30), sugar VARCHAR(30), added_sugar VARCHAR(30),
        total_fiber VARCHAR(30), soluble_fiber VARCHAR(30), insoluble_fiber VARCHAR(30), dietary_fiber VARCHAR(30), total_fat VARCHAR(30), 
        unsaturated_fat VARCHAR(30), monounsaturated_fat VARCHAR(30), polyunsaturated_fat VARCHAR(30), trans_fat VARCHAR(30), cholesterol VARCHAR(30),
        sodium VARCHAR(30))"""
        
        miscInfoTable = """CREATE TABLE miscInfo (name VARCHAR(30), info VARCHAR(30))"""

        cur.execute(vitMineralTable)
        cur.execute(antioxidantTable)
        cur.execute(miscNutrientsTable)
        cur.execute(BasicTable)
        cur.execute(miscInfoTable)
        conn.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
        

def sendIngredientData(conn, cur, instance):
    #           enterBtn, layout, scroll,     grid       0-6 are textinputs
    try:
        inputList = instance.parent.children[1].children[0].children[0:7]
        cur.execute("INSERT INTO nutrition(Name, calories, protein, carbs, sugar, fiber, total_fat) VALUES (%s,%s,%s,%s,%s,%s,%s);", (inputList[6].text,inputList[5].text,inputList[4].text,inputList[3].text,inputList[2].text,inputList[1].text,inputList[0].text))
        conn.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)






    '''
    for getting data from sql
    #mycursor.execute("SELECT food FROM smoothie")
    mycursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'smoothie'")
    data = str(mycursor.fetchall())

    if (data == "[(None,)]" or data == ['']):
        return []   # blank cell is none and the formatting below messes that up

    data = data[3:-3]              # drop the "[('" and ",)]"
    data = data.replace("'", "")
    data = data.replace(" ", "")

    return data.split(",")
    '''







