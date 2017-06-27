def fpOutlierCleaner(pred, x, y):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (x, y, error).
    """
    
    cleanedData = []
    reList = []


    #for i in range(len(x)):
    #   print(pred[i], y[i])

    for i in range(len(x)):
        re = pred[i] - y[i]
        reList.append(re)

    for i in range(90):
        t = (
            x[i][0],
            y[i][0],
            reList[i][0] 
            )
        cleanedData.append(t)

    cleanedData = sorted(cleanedData, key = lambda x: x[2], reverse = True)


    cleanedData = cleanedData[(int(.1 * len(x))): ]

    
    
    return cleanedData

def cleanAndPlot(predictions, x_train, y_train):
    '''
    cleans a dataset of outliers using regression using the fpOutlierCleaner
    function, reshapes the data, and plots it.
    
    Use after plotting variables w/ regression and seeing
    that there are outliers
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn import linear_model
    
    cleanedData = []
    cleanedData = fpOutlierCleaner(predictions, x_train, y_train)
    
    x, y, errors = zip(*cleanedData)
    x = np.reshape( np.array(x), (len(x), 1))
    y = np.reshape( np.array(y), (len(y), 1))

    
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    #plt.plot(x, reg.predict(x), color = 'blue')
    #plt.scatter(x, y)
    #plt.show()
    xx = []
    yy = []
    
    for value in x:
        xx.append(value[0])
    for value in y:
        yy.append(value[0])

    return xx, yy, errors

def nanToNumber (x, y, str_x, str_y, dictionary):
    '''
    turn NaNs to numbers.
    For use in the Enron final project
    
    '''
    x = []
    y = []
    number = 0
    for value in dictionary.values():
        x.append(value[str_x])
        y.append(value[str_y])
    for i in range(len(x)):
        if x[i] == 'NaN':
            x[i] = number
    for i in range(len(y)):
        if y[i] == 'NaN':
            y[i] = number
 
    return x, y

def removeOutliersFromDict(x, y, str_x, str_y, dictionary):
    for value in dictionary.values():
        if value[str_x] not in x:
            value[str_x] == 0
        if value[str_y] not in y:
            value[str_y] == 0

def reshape(x, y):
    import numpy as np
    x = np.reshape(np.array(x), (len(x), 1))
    y = np.reshape(np.array(y), (len(y), 1))
    return x, y

def plotWithPrediction(x, y):
    from sklearn import linear_model
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    predictions = reg.predict(x)
    return predictions