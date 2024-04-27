import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score 

def loaddata(file):
    Diabetes=pd.read_csv(file)
    return Diabetes
def trainandevalmodel(X_train_scaled,X_test_scaled,Y_train,Y_test):
    models={
        'RFclassifier': RandomForestClassifier(),
        'SVM': SVC(),
        'LogisticRegression': LogisticRegression(),
        'DTClassifier': DecisionTreeClassifier(),
        'GradBclassifier': GradientBoostingClassifier()
    }
    results = {}
    for name,model in models.items():
        model.fit(X_train_scaled,Y_train)
        Y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(Y_test,Y_pred)
        results[name] = accuracy * 100
    return results

st.title("Machine Learning ALGORITHMS ACCURACY based on Diabetes Dataset")
st.subheader("> In Here, you can able test various algorithm accuracies by uploding the datasets.")
uploaded_file = st.file_uploader('upload csv file',type=['csv'])
if uploaded_file is not None:
        Diabetes = loaddata(uploaded_file)
        dtacpy1 = Diabetes.copy()
        number = preprocessing.LabelEncoder()
        for column in dtacpy1.columns:
            dtacpy1[column] = number.fit_transform(dtacpy1[column])
        X = dtacpy1.drop('class', axis=1)
        y = dtacpy1['class']
        correlation = X.apply(lambda x: x.corr(y))
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        X = dtacpy1.drop('class', axis=1)
        y = dtacpy1['class']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        results = trainandevalmodel(X_train_scaled,X_test_scaled,y_train,y_test)
        st.header("Algorithm Accuracy(in %):")
        for name,accuracy in results.items():
            st.subheader(f'--> {name}: {accuracy:.2f}%')
    