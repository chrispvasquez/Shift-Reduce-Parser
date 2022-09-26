# def checkForSymbol(str, table):
#
#     current_symbol = ''
#
#     for letter in str:
#         current_symbol += letter
#         if current_symbol in table.symbols:
#             return True
#     return False

def getCurrentSymbol(str, table):

    current_symbol = ''

    for letter in str:
        current_symbol += letter
        if current_symbol in table.symbols:
            return current_symbol

def getStateNum(val):
    # Determine State Number
    snum = ''
    for c in reversed(val):
        if c.isnumeric():
            snum += c
        else:
            snum = snum[::-1]
            break
    return snum
