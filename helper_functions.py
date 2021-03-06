import pandas as pd
import numpy as np

def create_X(s):
#   age
    s['age'] = s['saledate'].dt.year - s['YearMade']
    s.loc[s['age'] < 0, 'age'] = 0
    s.loc[s['age'] > 100, 'age'] = s['age'].median()
#   state_dummies
    state_dummies = pd.get_dummies(s['state'])
    states = ['Florida', 'Texas', 'California', 'Washington',
              'Georgia', 'Maryland', 'Mississippi','Ohio', 'Illinois']
    state_dummies_selected = state_dummies[states]
    s[state_dummies_selected.columns] = state_dummies_selected
#   auct_dummies
    auct_dummies = pd.get_dummies(s['auctioneerID'])
    auct_dummies_selected = auct_dummies[[0, 1, 2, 3]]
    s[auct_dummies_selected.columns] = auct_dummies_selected
#   enc_dummies
    enc_dummies = pd.get_dummies(s['Enclosure'])
    enc_dummies_selected = enc_dummies[['OROPS', 'EROPS', 'EROPS w AC', 'EROPS AC']]
    s[enc_dummies_selected.columns] = enc_dummies_selected
#   hydra_dummies
    hydra_dummies = pd.get_dummies(s['Hydraulics'])
    hydra_dummies_selected = hydra_dummies[['2 Valve', 'Standard', 'Auxiliary']]
    s[hydra_dummies_selected.columns] = hydra_dummies_selected
#   desc_dummies
    desc_dummies = pd.get_dummies(s['fiProductClassDesc'], drop_first='True')
    s[desc_dummies.columns] = desc_dummies
    s = s.loc[:,'age':]
    to_drop = ['Hydraulic Excavator, Track - 150.0 to 300.0 Metric Tons',
           'Hydraulic Excavator, Track - 300.0 + Metric Tons',
           'Hydraulic Excavator, Track - 4.0 to 6.0 Metric Tons',
           'Hydraulic Excavator, Track - Unidentified',
           'Hydraulic Excavator, Track - Unidentified (Compact Construction)',
           'Motorgrader - 45.0 to 130.0 Horsepower', 'Motorgrader - Unidentified',
           'Wheel Loader - 1000.0 + Horsepower', 'Motorgrader - 45.0 to 130.0 Horsepower']
    to_drop_final = []
    for i in to_drop:
        if i in s.columns:
            to_drop_final.append(i)
    s = s.drop(to_drop_final, axis = 1)
    return np.array(s)

def create_y_train(s):
    return np.array(np.log(s['SalePrice'])).reshape((len(s['SalePrice']), 1))

def train_model(X, y):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict(model, test, X_test, name):
    y_hat = model.predict(X_test)
    submission = pd.DataFrame(test['SalesID'])
    submission['SalePrice'] = np.exp(y_hat)
    submission.columns = ['SalesID', 'SalePrice']
    submission.to_csv( name + '.csv', index=False)
    return submission

def score(predictions, actual):
    predictions = np.array(predictions['SalePrice'])
    actual = np.array(actual['SalePrice'])
    log_diff = np.log(predictions+1) - np.log(actual+1)
    return np.sqrt(np.mean(log_diff**2))