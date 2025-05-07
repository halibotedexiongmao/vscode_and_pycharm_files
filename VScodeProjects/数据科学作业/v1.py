import numpy as np
import pandas as pd
a1=pd.read_csv(r'C:\Users\halib\VScodeProjects\数据科学作业\课内作业\drinks.csv')



drink=a1
grouped = drink.groupby('continent')['beer_servings']
print(grouped)  
#grouped1 = drink.groupby('continent')