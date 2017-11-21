def buyLotsOfFruit(orderList):

    totalCost = 0.0
    "*** YOUR CODE HERE ***"
    print len(orderList)
    return totalCost

# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [ ('apples', 2.0), ('pears', 3.0), ('limes', 4.0) ]
    print len(orderList)
    print 'Cost of', orderList, 'is', buyLotsOfFruit(orderList)
