"""An intentionally messy example file used to demonstrate the analyzer
catching real problems: bad naming, unused variables, duplicate lines,
and high complexity."""


def calculateTotalPrice(items, taxRate):
    debugFlag = True
    total = 0
    for item in items:
        if item > 0:
            total = total + item
        elif item < 0:
            print('skipping negative item')
        elif item == 0:
            print('skipping negative item')
        else:
            total = total
    return total * (1 + taxRate)


class shopping_cart:
    def __init__(self):
        self.items = []
