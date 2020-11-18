import pandas as pd


def groupAge(age):
    if age <= 70: return 0
    if age > 80: return 6
    return (age - 70 + 1) // 2


def input_processing(form):
    Education = int(form['Education'])
    Sex = int(form['Sex'])
    Age = int(form['Age'])
    Activity = form['Activity']
    Pet = int(form['Pet'])
    Children = int(form['Children'])
    Sport = int(form['Sport'])
    Family = Pet + Children
    IsAlone = 1 if not Family else 0
    AgeEducation = groupAge(Age) * Education
    Status = groupAge(Age) + Sport + IsAlone
    
    return pd.DataFrame(
            [[Education,Sex,Age,Pet,Children,Activity,Sport,Family,IsAlone,AgeEducation,Status]],
            columns=['Education','Sex','Age','Pet','Children','Activity','Sport','Family','IsAlone','Age*Education','Status'],
            dtype=int)
