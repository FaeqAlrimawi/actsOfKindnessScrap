import pandas as pd

# read excel sheet
df = pd.read_excel("actsOfKindess.xlsx")

# get title and description
review_df = df[['Title', 'Description']]
# print(review_df)

