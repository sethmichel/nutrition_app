import psycopg2
from config import config

# create a table if one doesn't exist
# misc info:
# nutrient info: notes, it's what I show the user when they read about nutrients
# basic info: the major things that are on nitrition labels like fat, calories...
def CreateTables(cur, conn, dbTableNames):
    vitMineralTable = """
    CREATE TABLE vitamins_minerals (name VARCHAR(30), vitA VARCHAR(30), vitB1 VARCHAR(30), vitB2 VARCHAR(30), vitB3 VARCHAR(30), vitB4 VARCHAR(30), 
    vitB6 VARCHAR(30), vitB9 VARCHAR(30), vitB12 VARCHAR(30), vitC VARCHAR(30), vitD VARCHAR(30), vitE VARCHAR(30), vitK1 VARCHAR(30), 
    calcium VARCHAR(30), niacin VARCHAR(30), folate VARCHAR(30), manganese VARCHAR(30), magnesium VARCHAR(30), biotin VARCHAR(30), 
    pantonthenic_acid VARCHAR(30), iron VARCHAR(30), potassium VARCHAR(30), iodine VARCHAR(30), phosphorus VARCHAR(30), copper VARCHAR(30), 
    selenium VARCHAR(30), zinc VARCHAR(30), chromium VARCHAR(30), molydhenum VARCHAR(30), chloride VARCHAR(30), silicon VARCHAR(30), 
    lycopene VARCHAR(30), lutein VARCHAR(30), boron VARCHAR(30), vanadium VARCHAR(30), nickel VARCHAR(30))"""

    antioxidantTable = """
    CREATE TABLE antioxidants (name VARCHAR(30), anthocyanin VARCHAR(30), quercetin VARCHAR(30), myricetin VARCHAR(30), pelargonidin VARCHAR(30), 
    procyanidins VARCHAR(30), ellagitannins VARCHAR(30), ellagic_acid VARCHAR(30))"""

    miscNutrientsTable = """
    CREATE TABLE misc_nutrients (name VARCHAR(30), omega3 VARCHAR(30), creatine VARCHAR(30), taurine VARCHAR(30), l_glutamine VARCHAR(30), 
    artificial_flavors VARCHAR(30), artificial_colors VARCHAR(30), artificial_sweeteners VARCHAR(30))"""
    
    BasicTable = """
    CREATE TABLE basic_info (name VARCHAR(30), calories VARCHAR(30), protein VARCHAR(30), carbs VARCHAR(30), sugar VARCHAR(30), added_sugar VARCHAR(30),
    total_fiber VARCHAR(30), soluble_fiber VARCHAR(30), insoluble_fiber VARCHAR(30), dietary_fiber VARCHAR(30), total_fat VARCHAR(30), 
    unsaturated_fat VARCHAR(30), monounsaturated_fat VARCHAR(30), polyunsaturated_fat VARCHAR(30), trans_fat VARCHAR(30), cholesterol VARCHAR(30),
    sodium VARCHAR(30))"""
    
    miscInfoTable = """CREATE TABLE misc_info (name VARCHAR(30), info VARCHAR(30))"""

    nutrientInfo = """CREATE TABLE nutrient_info (name VARCHAR(30), info VARCHAR(30))"""

    # makes it so I can have any of the tables but not the others and I won't have an sql error when making the others
    try:
        if ("basic_info" not in dbTableNames):
            cur.execute(BasicTable)
            dbTableNames.append("basic_info")
        if ("vitamins_minerals" not in dbTableNames):
            cur.execute(vitMineralTable)
            dbTableNames.append("vitamins_minerals")
        if ("antioxidants" not in dbTableNames):
            cur.execute(antioxidantTable)
            dbTableNames.append("antioxidants")
        if ("misc_nutrients" not in dbTableNames):
            cur.execute(miscNutrientsTable)
            dbTableNames.append("misc_nutrients")
        if ("misc_info" not in dbTableNames):
            cur.execute(miscInfoTable)
            dbTableNames.append("misc_info")
        if ("nutrient_info" not in dbTableNames):
            cur.execute(nutrientInfo)
            dbTableNames.append("nutrient_info")

        conn.commit()

    except(Exception, psycopg2.DatabaseError) as error: 
        conn.rollback()
        print(error)


def SendIngredientData(conn, cur, allHeaders, dbTableNames, sm, instance):
    try:
        for i in range(0, len(dbTableNames)):
            if (dbTableNames[i] != "nutrient_info"):
                #cur.execute("INSERT INTO nutrition(name, calories, protein, carbs, sugar, fiber, total_fat) VALUES (%s,%s,%s,%s,%s,%s,%s);", (inputList[6].text,inputList[5].text,inputList[4].text,inputList[3].text,inputList[2].text,inputList[1].text,inputList[0].text))
                sql = "INSERT INTO " + dbTableNames[i] + "("
                
                # the col names
                for j in range(0, len(allHeaders[dbTableNames[i]])):
                    sql += (str(allHeaders[dbTableNames[i]][j]) + ", ")

                sql = sql[:-2] + ") VALUES ("    # cut off last comma
                grid = sm.screens[i].children[0].children[1]

                # textinputs are in the same order as the allHeaders col names, and they're first
                for j in range(0, len(allHeaders[dbTableNames[i]])):
                    sql += (grid.children[j].text + ", ")
                
                sql = sql[:-2] + ");"

                cur.execute(sql)
        conn.commit()
            
    except(Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    

def GetTableSchema(cur, conn, tableName):
    try:
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '" + tableName + "';")
        schema = cur.fetchall()

        for i in range(0, len(schema)):
            holder = (str(schema[i]).lower())[2:-3]            
            holder = holder.replace("_", " ")
            schema[i] = holder

        return schema

    except (Exception) as error:
        conn.rollback()
        print(error)


def GetTableNames(cur, conn):
    try: 
        cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema != 'pg_catalog' AND table_schema != 'information_schema';")
        tableNames = cur.fetchall()
        for i in range(0, len(tableNames)):
            tableNames[i] = tableNames[i][1]
        
        return tableNames

    except (Exception) as error:
        print(error)
        conn.rollback()
        return []


def GetNutrientData(conn, cur):
    nutrientDataDict = {}

    try:
        cur.execute("SELECT * FROM nutrient_info")
        x = cur.fetchall()
        for i in range(0, len(x)):
            nutrientDataDict[x[i][0]] = x[i][1]
        
        return nutrientDataDict

    except (Exception) as error:
        print(error)
        conn.rollback()
        return []



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




# drop all tables: DROP TABLE name;


