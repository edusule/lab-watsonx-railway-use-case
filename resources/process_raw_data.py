import pandas as pd
import json
import unidecode

## Generative AI
# Cargar el JSON en un DataFrame
with open('raw_data/genai_raw_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

def add_dot(value):
    value = unidecode.unidecode(value)
    # Replace spaces with hyphens
    value = value.replace(' ', '_')
    return value + '_'

# Apply the function to the 'tipo' column
distinct_values = df['tipo'].unique()

# Creating a dictionary to map distinct values to unique letters
value_to_letter = {value: chr(idx + ord('A')) for idx, value in enumerate(distinct_values)}

dict_tipo = {
    "Problemas con el operario de ayuda":"OP_",
    "Problema con el material de ayuda para la discapacidad":"MAT_",
    "Problemas con la reserva por la página web":"WEB_"
}

# Creating a new column with unique letters as identifiers
df["tipo"].replace(dict_tipo, inplace=True)
df['sentimiento'] = df['sentimiento'].apply(add_dot)

# Dividir el DataFrame en dos basado en el valor de la columna "tipo" - Dataframe para few shot prompting
df_tipo_distinto = df.drop_duplicates(subset=['tipo'])

quejas = list(df_tipo_distinto["queja"])
tipos = list(df_tipo_distinto["contestación"])

#Df para posteriormente evaluaacion de prompt
df_evaluaciones = df[~df.index.isin(df_tipo_distinto.index)]

# Guardar los DataFrames en archivos CSV
df_tipo_distinto.to_csv('output_data/examples_few_shot_prompt.csv', index=False, encoding="utf-8")
df_evaluaciones.to_csv('output_data/ground_truth.csv', index=False, encoding="utf-8")


## Machine Learning

df_churn = pd.read_csv("raw_data/Churn Modeling.csv")
df = df_churn[["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary", "Exited"]]

column_names_mapping = {
    "CreditScore": "Puntos",
    "Geography": "Geografia",
    "Gender": "Genero",
    "Age": "Edad",
    "Tenure": "Antigüedad",
    "Balance": "KmAcompañante",
    "NumOfProducts": "Acompañantes",
    "HasCrCard": "TieneTarjetaClub",
    "IsActiveMember": "EsMiembroActivo",
    "EstimatedSalary": "Km",
    "Exited": "Abandono"
}

df.columns = [column_names_mapping[col] for col in df.columns]


# Separate 5 rows with at least 2 having Exited = 1
exited_rows = df[df["Abandono"] == 1].sample(n=40)  # Getting 2 rows with Exited = 1
non_exited_rows = df[df["Abandono"] == 0].sample(n=160)  # Getting 3 rows with Exited = 0
test_df = pd.concat([exited_rows, non_exited_rows])

# The rest of the data will be used for training
train_df = df.drop(test_df.index)

# Saving the datasets
test_df.to_csv('output_data/test_data_churn.csv', index=False)
train_df.to_csv('output_data/train_data_churn.csv', index=False)

test_df.head(), train_df.head()