import json

jsonDict = json.load(open('Data/nutrients.json'))   # data

usedToSeeDebugVariablesInThisFile = 0







''' json template (make sure it's in mg)
{"name": {
        "serving size": ,
        "calories": ,
        "protein": ,
        "carbs": ,
        "total_fat": ,
        "saturated_fat": ,
        "trans_fat": ,
        "polyunsaturated_fat": ,
        "monounsaturated_fat": ,
        "cholesterol": ,
        "sodium": ,
        "sugar": ,
        "erythritol (sweetener)": ,
        "cant_tell_fiber": ,
        "dietary_fiber": ,
        "vit_a": ,
        "vit_b1 (thiamine)": ,
        "vit_b2 (riboflavin)": ,
        "vit_b4 (niacin)": ,
        "vit_b5 (pantothenic_acid)": ,
        "vit_b6 (pyridoxine)": ,
        "vit_b7 (biotin)": ,
        "vit_b9 (folic acid)": ,
        "vit_b12 (cobalamin)": ,
        "vit_c": ,
        "vit_d": ,
        "vit_e": ,
        "vit_k": ,
        "potassium": ,
        "folate": ,
        "calcium": ,
        "iron": ,
        "iodine": ,
        "magnesium": ,
        "manganese": ,
        "zinc": ,
        "selenium": ,
        "copper": ,
        "phosphorus": ,
        "molybdenum": ,
        "chromium": ,
        "choline": ,
        "chloride": ,
        "lycopene": ,
        "phenylalanine (EAA)": ,
        "valine (EAA)": ,
        "threonine (EAA)": ,
        "tryptophan (EAA)": ,
        "methionine (EAA)": ,
        "leucine (EAA)": ,
        "isoleucine (EAA)": ,
        "lysine (EAA)": ,
        "histidine (EAA)": ,
        "anthocyanin (antioxidant)": "",
        "quercetin (antioxidant)": "",
        "myricetin (antioxidant)": "",
        "pelargonidin (antioxidant)": "",
        "procyanidins (antioxidant)": "",
        "ellagitannins (antioxidant)": "",
        "ellagic_acid (antioxidant)": "",
        "creatine": ,
        "taurine": ,
        "L_glutamine": ,
        "omega-3": ,
        "omega-6": ,
        "medium-chain triglycerides": ,
        "lutein + zeaxanthin": ,
        "bacillus coagulans": ""
    }
}
'''