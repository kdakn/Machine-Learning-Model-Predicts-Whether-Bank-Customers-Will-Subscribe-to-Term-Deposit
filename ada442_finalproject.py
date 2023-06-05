# -*- coding: utf-8 -*-
"""ADA442_FinalProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_YUwgAOEqCWcQpJTEe0s0b3lx4dgwQfD

<img align="right" src="https://www.tedu.edu.tr/themes/custom/tedu/logo.svg" width="350px" height="350px"/>
<h1 style="font-size:20pt"> ADA 442 | Final Project </h1><br/>
<b> Student Name & ID: </b> Özge Sena Karabıyık 64303375180 <br/>
<b> Student Name & ID: </b> Korhan Deniz Akın 30277304006 <br/>
<b> Student Name & ID: </b> Kerem Irmak 32813381526 <br/>
<b> Submission Date: </b>4 June 2023<br/>

## Import modules
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
python -m pip install seaborn
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from sklearn.preprocessing import OrdinalEncoder
# %matplotlib inline
warnings.filterwarnings('ignore')

from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder,  StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, make_scorer, roc_auc_score
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

"""## Loading the Dataset"""

df = pd.read_csv('bank.csv')
df.head()

df.describe()

df.info()

df.apply(lambda x: len(x.unique()))

"""## Data Visualization"""

sns.countplot(x = df['y'])

plt.style.use('fivethirtyeight')
plt.figure(figsize=(13, 7))
sns.distplot(df['age'], bins=25)

ax = sns.countplot(x = df['job'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

sns.countplot(x = df['marital'])

illiterate_count = df[df['marital'] == 'unkonwn'].shape[0]
print("Number of marital unkonwn people:", illiterate_count)

ax = sns.countplot(x = df['education'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

illiterate_count = df[df['education'] == 'illiterate'].shape[0]
print("Number of illiterate people:", illiterate_count)

sns.countplot(x = df['default'])

illiterate_count = df[df['default'] == 'yes'].shape[0]
print("Number of people has credit in default:", illiterate_count)

sns.countplot(x = df['housing'])

sns.countplot(x = df['loan'])

sns.countplot(x = df['contact'])

sns.countplot(x = df['month'])

sns.countplot(x = df['day_of_week'])

plt.style.use('fivethirtyeight')
plt.figure(figsize=(13, 7))
sns.distplot(df['duration'], bins=25)

sns.countplot(x = df['campaign'])

ax = sns.countplot(x = df['pdays'])

ax = sns.countplot(x = df['previous'])

ax = sns.countplot(x = df['poutcome'])

sns.countplot(x = df['emp.var.rate'])

ax = sns.countplot(x = df['cons.price.idx'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

ax = sns.countplot(x = df['cons.conf.idx'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

plt.style.use('fivethirtyeight')
plt.figure(figsize=(13, 7))
sns.distplot(df['euribor3m'], bins=25)

ax = sns.countplot(x = df['nr.employed'])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

"""## Data Cleaning"""

df.isnull().sum()

"""**there is no null value in dataset so "handling missing values" is not necessary for this dataset**"""

duplicates = df.duplicated()
print(df[duplicates])

num_duplicates = sum(duplicates)
print("Number of duplicate rows:", num_duplicates)

"""**There is no duplicate row in dataset so "deal with duplicates" is not necessary for this dataset**

#### As a "data cleaning" step we do data formatting, we convert our dataset to csv (comma seperated value) format, converted csv file can be found in the homework zip file

## Data Preprocessing

**Perform two types of encoding on categorical data, ordinal and one-hot encoding**

**Specifying "month" and "day_of_week" categories to perform ordinal encoding in sequential order**
"""

month_categories = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
day_categories = ["mon","tue","wed","thu","fri","sat","sun"]

"""**Listing categorical columns to perform one_hot_encoding on them**"""

categorical_columns = ["job","marital","default","housing","loan","contact","education"]

"""**Listing numerical columns to perform scaling on them**"""

numerical_columns = ['age', "duration",'campaign', 'pdays', 'previous','emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']

"""**Defining preprocess steps, they will be performed on dataset with pipeline**"""

preprocess = ColumnTransformer([
                             ("month_encoded",OrdinalEncoder(categories=[month_categories]),['month']),
                             ("day_encoded",OrdinalEncoder(categories=[day_categories]),['day_of_week']),
                             ('one_hot_encoder',OneHotEncoder(handle_unknown='ignore'), categorical_columns[1:]),
                             ("numeric_scaler", StandardScaler(), numerical_columns),
                             ('minmaxscaling', MinMaxScaler(), numerical_columns),
                            ])

"""## Input Split"""

X = df.drop(columns=['y'])
y = df['y']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

"""## Model Selection"""

def makepipeline_findbestmodel(preprocess, model, x_train, y_train, x_test, y_test)->float:
    feature_selection = SelectFromModel(model)
    pipeline = make_pipeline(preprocess,feature_selection, model)
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict (x_test)
    return accuracy_score(y_test, predictions)

"""## Model Training"""

model_and_accuracy = {}

model = LogisticRegression()
accuracy_LR = makepipeline_findbestmodel(preprocess, model,x_train, y_train, x_test, y_test)

model_and_accuracy[model] = accuracy_LR

model = DecisionTreeClassifier()
accuracy_DT = makepipeline_findbestmodel(preprocess, model,x_train, y_train, x_test, y_test)

model_and_accuracy[model] = accuracy_DT

model = RandomForestClassifier()
accuracy_RF = makepipeline_findbestmodel(preprocess, model, x_train, y_train, x_test, y_test)

model_and_accuracy[model] = accuracy_RF

keys = list(model_and_accuracy.keys())
values = list(model_and_accuracy.values())
accuracy = 0
best_model_index = 0
index = 0

for v in values:
    if v > accuracy:
        accuracy = v
        best_model_index = index
    index+=1

best_model = keys[best_model_index]

print(best_model)
print(accuracy)

"""## Hyperparameter Tuning"""

feature_selection = SelectFromModel(best_model)

pipeline = Pipeline([('preprocess', preprocess),
                         ('feature_selection', feature_selection),
                         ('model', LogisticRegression())])

grid_params_logistic = {
    'model__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
    'model__penalty': ['l1', 'l2', 'elasticnet', 'none']
}

def applyGridSearchCv(x_train, y_train, x_test, y_test, pipeline, grid_params):
    grid_search = GridSearchCV(estimator=pipeline, param_grid=grid_params, scoring='neg_mean_squared_error', cv=5)
    grid_search.fit(x_train, y_train)
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"Root Mean Squared Error: {rmse}")

applyGridSearchCv(x_train, y_train, x_test, y_test, pipeline, grid_params_logistic)

precision = precision_score(y_test, preds, pos_label='yes')
print(precision)

cm = confusion_matrix(y_test, preds)
print("Confusion Matrix:")
print(cm)

f1 = f1_score(y_test, preds, pos_label='yes')
print("F1 Score:", f1)



