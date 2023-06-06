import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle #pickle for saving the model.
import sklearn


st.title('Deposit Prediction Web App')

age = st.number_input('Enter an integer', step=1)

job = st.selectbox(
     'Please select your job',
    ('admin','blue-collar','entrepreneur', 'housemaid','management','retired','self-employed', 'services','student','technician','unemployed','unknown'))

marital = st.selectbox('Please select your marital status',
                       ('married','single','divorced'))

education = st.selectbox('Please select your education',
                          ('basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown'))

default = st.selectbox('default',('yes','no','unknown') )

housing = st.selectbox('housing',('yes','no','unknown') )

loan = st.selectbox('loan:',('yes','no','unknown') )

contact = st.selectbox('Please select our contact communication type',
                ('cellular','telephone'))

month = st.selectbox('Please select when was our lasst contact',
                      ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec') )

day_of_week = st.selectbox('day_of_week',('mon','tue','wed','thu','fri'))

duration = st.number_input('duration:')

campaign = st.number_input('campaign:')

pdays = st.number_input('pdays:')

previous = st.number_input('previous:')

poutcome = st.selectbox('poutcome',('success','failure','nonexistent') )

emp_var_rate = st.number_input('emp_var_rate:')

cons_price_idx = st.number_input('cons_price_idx:')

cons_conf_idx = st.number_input('cons_conf_idx:')

euribo3m = st.number_input('euribo3m:')

nr_employed = st.number_input('nr_employed:')



#Test single input.
input_data = np.array([age, job, marital,education,default,housing,loan,contact,month,day_of_week,duration,campaign,pdays,previous,poutcome,emp_var_rate,cons_price_idx ,cons_conf_idx,	euribo3m,nr_employed])
input_data = input_data.reshape(1, -1)
columns = ['age', 'job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']
input_data_df = pd.DataFrame(input_data, columns=columns)


def my_function():
    #pickled_model = pickle.load(open("C:/Users/Deniz/OneDrive/Belgeler/GitHub/ada442/models/tuned_best_model.pkl", 'rb'))#Load the model.
    pickled_model = pickle.load(open("models/tuned_best_model.pkl", 'rb'))#Load the model.

    input_predictions = pickled_model.predict(input_data_df)
    # Print out the prediction
    st.write(input_predictions)


if st.button('Press me'):
    my_function()