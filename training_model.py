import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel


def average(num_list):
    avg = sum(num_list) / len(num_list)
    return avg


df = pd.read_csv('train_set_processed.csv')
df_test = pd.read_csv('test_set_processed.csv')

bool_columns_to_encode = list(df.select_dtypes(include='bool').columns)

df.loc[:, bool_columns_to_encode] = (
    df.loc[:,bool_columns_to_encode] == True).astype(int)

bool_columns_to_encode = list(df_test.select_dtypes(include='bool').columns)

df_test.loc[:, bool_columns_to_encode] = (
    df_test.loc[:,bool_columns_to_encode] == True).astype(int)

Y = df['Transported']
X = df.drop(['PassengerId', 'Transported'], axis = 1)


columns_to_encode = list(X.select_dtypes(include='object').columns)

for col in columns_to_encode:
    one_hot = pd.get_dummies(X[col], prefix=col)
    X = X.drop(col, axis=1)
    X = X.join(one_hot)

X_kaggle_test = df_test.drop(['PassengerId'], axis = 1)

for col in columns_to_encode:
    one_hot = pd.get_dummies(X_kaggle_test[col], prefix=col)
    X_kaggle_test = X_kaggle_test.drop(col, axis=1)
    X_kaggle_test = X_kaggle_test.join(one_hot)
    
  
# training model without choosing parameters

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3)
clf = RandomForestClassifier(n_estimators = 50, random_state = 1, n_jobs = -1)
clf.fit(x_train, y_train)



y_pred = clf.predict(x_test)

print('Accuracy (without choosing parameters): {}'.format(
    metrics.accuracy_score(y_test, y_pred)))


labels = list(x_train.columns)
sfm = SelectFromModel(clf, threshold=0.02)
sfm.fit(x_train, y_train)

x_important_train = sfm.transform(x_train)

x_important_test = sfm.transform(x_test)


clf_important = RandomForestClassifier(n_estimators=50, random_state = 1, 
                                       n_jobs =-1)
clf_important.fit(x_important_train, y_train)

y_important_pred = clf_important.predict(x_important_test)


print('Accuracy (chosen parameters with highest importance): {}'.format(
    metrics.accuracy_score(y_important_pred, y_pred)))


x_kaggle_test = sfm.transform(X_kaggle_test)


y_kaggle_pred = clf.predict(X_kaggle_test)
passenger_id = pd.read_csv('test.csv')['PassengerId'].to_frame()
y_kaggle_pred = pd.Series(y_kaggle_pred).rename('Transported').astype(bool)


submission = passenger_id.join(y_kaggle_pred)

submission.to_csv('kaggle_submission.csv', index=False)
