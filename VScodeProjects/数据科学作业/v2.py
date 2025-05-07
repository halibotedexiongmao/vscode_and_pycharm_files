import numpy as np
import pandas as pd
a=pd.Series([1,2,3,4,5])
#a.name='hh'
#a.index.name='indexhh'
b=pd.Series([6,7,8,9,10])
e=b.T
print(e)
print(b)
'''print(a)
c=pd.DataFrame({'a':a,'b':b})
print(c)
d=c.T
print(d)'''