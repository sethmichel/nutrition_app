# create db only if one doens't exist
def connect_to_db():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS smoothie")
    mycursor.execute("USE smoothie")


# create a table if one doesn't exist
def create_table():
    try:
        # test if the table exists
        mycursor.execute("SELECT calories FROM smoothie WHERE food = 'strawberries'")

    except:
        # if not then create table
        mycursor.execute("CREATE TABLE smoothie (food VARCHAR(30), calories VARCHAR(30), sugar VARCHAR(30), added_sugar VARCHAR(30), fiber VARCHAR(30), soluble_fiber VARCHAR(30),dietary_fiber VARCHAR(30), fat VARCHAR(30), satfat VARCHAR(30), transfat VARCHAR(30), cholesterol VARCHAR(30), sodium VARCHAR(30), vita VARCHAR(30), thiamin VARCHAR(30), riboflaven VARCHAR(30), vitb3 VARCHAR(30), vitb4 VARCHAR(30), vitb6 VARCHAR(30), vitb9 VARCHAR(30), vitb12 VARCHAR(30), vitb_mystery VARCHAR(30), vitc VARCHAR(30), vitd VARCHAR(30), vite VARCHAR(30), vitk1 VARCHAR(30), calcium VARCHAR(30), niacin VARCHAR(30), folate VARCHAR(30),manganese VARCHAR(30), magnesium VARCHAR(30),biotin VARCHAR(30), pantonthenic_acid VARCHAR(30), potassium VARCHAR(30), iron VARCHAR(30), iodine VARCHAR(30), phosphorus VARCHAR(30), copper VARCHAR(30), selenium VARCHAR(30), zinc VARCHAR(30), chromium VARCHAR(30), molybdenum VARCHAR(30), chloride VARCHAR(30), silicon VARCHAR(30), lycopene VARCHAR(30), lutein VARCHAR(30), boron VARCHAR(30), vanadium VARCHAR(30), nickel VARCHAR(30), artificial_flavors VARCHAR(30), artificial_colors VARCHAR(30), artificial_sweeteners VARCHAR(30), creatine VARCHAR(30), taurine VARCHAR(30), L_glutamine VARCHAR(30), anthocyanin VARCHAR(30), quercetin VARCHAR(30), myricetin VARCHAR(30), pelargonidin VARCHAR(30), procyanidins VARCHAR(30), ellagitannins VARCHAR(30), ellagic_acid VARCHAR(30))")


# called at app start by init() (This is called 1 time)
# returns the column of food names as list
def get_food_names():
    #mycursor.execute("SELECT food FROM smoothie")
    mycursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'smoothie'")
    data = str(mycursor.fetchall())

    if (data == "[(None,)]" or data == ['']):
        return []   # blank cell is none and the formatting below messes that up

    data = data[3:-3]              # drop the "[('" and ",)]"
    data = data.replace("'", "")
    data = data.replace(" ", "")

    return data.split(",")








