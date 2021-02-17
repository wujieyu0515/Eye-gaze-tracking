import numpy as np
from sklearn import linear_model

def cali_fitting(iris_pos,inner_pos,mouse_pos,axis):
    iris_pos = np.asarray(iris_pos)
    inner_pos = np.asarray(inner_pos)
    point = np.array(mouse_pos)
    EC_IC = iris_pos - inner_pos

    X = []
    for x, y in EC_IC:
        X.append([x, y, x * y, x ** 2, y ** 2, 1])
    X_mat = np.array(X)

    screen_pos = []
    for i in range(9):
        screen_pos.append([point[i][axis]])

    model = linear_model.LinearRegression()
    model.fit(X_mat, screen_pos)
    print(mouse_pos)
    print(model.predict(X_mat))

    return model

def get_matrix(iris_x,iris_y,inner_x,inner_y):
    EC_IC = [iris_x-inner_x, iris_y-inner_y]
    return np.array([EC_IC[0],EC_IC[1],EC_IC[0]*EC_IC[1],EC_IC[0]**2,EC_IC[1]**2,1])

def get_mid(x1,x2):
    return int((x1+x2)/2)




