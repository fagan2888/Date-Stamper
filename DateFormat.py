def Format(year, month, day, format):

    if(year < 10):
        year = ''.join(['200',str(year)])
    elif(year < 100):
        year = ''.join(['20',str(year)])
    else:
        year = str(year)

    month = m[format][month]

    day = d[format][day]

    if format == 0 or format == 1:
        """ M/D/YYYY or MM/DD/YYYY """
        datestring = '/'.join([month,day,year])

    else:
        """ Mon Day, Year and Month Day, Year """
        datestring = ''.join([month,' ',day,', ',year])

    return datestring



""" Dictionary Definitions for the Date Formatting """

_ms = {1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10',
      11:'11', 12:'12'}

_mm = {1:'01', 2:'02', 3:'03', 4:'04', 5:'05', 6:'06', 7:'07', 8:'08', 9:'09',
      10:'10', 11:'11', 12:'12'}

_mon = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug',
       9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

_month = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
         7:'July', 8:'August', 9:'September', 10:'October', 11:'November',
         12:'Decebmer'}

m = [_ms, _mm, _mon, _month];

_ds = {1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10',
      11:'11', 12:'12', 13:'13', 14:'14', 15:'15', 16:'16', 17:'17', 18:'18',
      19:'19', 20:'20', 21:'21', 22:'22', 23:'23', 24:'24', 25:'25', 26:'26',
      27:'27', 28:'28', 29:'29', 30:'30', 31:'31'}

_dd = {1:'01', 2:'02', 3:'03', 4:'04', 5:'05', 6:'06', 7:'07', 8:'08', 9:'09',
      10:'10', 11:'11', 12:'12', 13:'13', 14:'14', 15:'15', 16:'16', 17:'17',
      18:'18', 19:'19', 20:'20', 21:'21', 22:'22', 23:'23', 24:'24', 25:'25',
      26:'26', 27:'27', 28:'28', 29:'29', 30:'30', 31:'31'}

d = [_ds, _dd, _ds, _ds]