import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

def train_model(model_info: dict, dataset: list):
    """ 
        Train dataset based on the model info.
        Return bynary model and accuracy score
    """
    
    dataset_features = model_info['dataset_features']
    dataset_features.append('resolution')
    attributes = len(dataset_features) - 1

    dataframe = pd.DataFrame(dataset)
    array = dataframe.values
    X = array[:,0:attributes]
    y = array[:,attributes]

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        return model, accuracy
    except Exception as e:
        print('Model requires more samples to be trained.', e)
        return None, 0

def predict_entry(model: DecisionTreeClassifier, sample_input):
    return model.predict([sample_input])