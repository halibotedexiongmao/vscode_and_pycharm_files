from openpyxl.worksheet.views import SheetView

yw="`~!@#$%^&*()_-+=|\?/>.<,{[}]:;'"
zw="·~！@#￥%…&*（）—-+=|、？/》。《，{【}】：；‘"
print(len(zw),len(yw))
for i in range(len(yw)):
    if ord(yw[i])==ord(zw[i]):
        print('{}={}'.format(yw[i],zw[i]))
    else:
        print('{}!={}'.format(yw[i],zw[i]))