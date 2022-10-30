from flask import Flask,render_template,request,jsonify
import pickle
import json
import numpy as np
import pandas as pd

with open("artifacts/columns_name.json","r") as json_file:
    col_name = json.load(json_file)
col_name_list =col_name['col_name']

model = pickle.load(open("artifacts/model.pkl","rb"))

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods= ["GET","POST"])
def predict():
    data = request.form

    credit_score = data['credit_score']

    age = data['age']
    tenure = data['tenure']
    balance = data['balance']
    num_of_products = data['num_of_products']

    if data['has_cr_card']=='Yes':
        has_cr_card = 1
    else:
        has_cr_card = 0

    if data['is_active_member']=='Yes':
        is_active_member = 1
    else:
        is_active_member = 0
       
    estimated_salary = data['estimated_salary']

   
    if data['geography']=='Germany':
        geography_Germany = 1
        geography_Spain = 0
    elif data['geography']=='Spain':
        geography_Germany = 0
        geography_Spain = 1
    else :
        geography_Germany = 0
        geography_Spain = 0


    if data['gender']=='Male':
        gender_Male = 1
    else :
        gender_Male = 0
   
    input = pd.DataFrame({'credit_score': [credit_score],
   'age': [age],
   'tenure': [tenure],
   'balance': [balance],
   'num_of_products': [num_of_products],
   'has_cr_card': [has_cr_card],
   'is_active_member': [is_active_member],
   'estimated_salary': [estimated_salary],
   'geography_Germany': [geography_Germany],
   'geography_Spain': [geography_Spain],
   'gender_Male': [gender_Male]})
 
    print(input)
    result = model.predict(input)

    if result[0] == 0:
        Churn_result = "Dont worry The costumer Will Not Exit"
    else: 
        Churn_result = "Alert! The costumer Will Exit"
        
    return render_template("index.html",prediction = Churn_result)

if __name__== "__main__":
    app.run(debug=True)