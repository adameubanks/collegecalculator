from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import tensorflow as tf
app = Flask(__name__)

@app.route('/')
def myForm():
    return render_template('ivy.html')

@app.route('/', methods=['POST'])
def myFormPost():
    unweightedGPA = request.form.get('unweightedGPA', type=float)
    weightedGPA = request.form.get('weightedGPA', type=float)
    SATMath = request.form.get('SATMath', type=int)
    SATReading = request.form.get('SATReading', type=int)
    classRank = request.form.get('classRank', type=int)

    unweight = tf.feature_column.numeric_column("UW")
    weight = tf.feature_column.numeric_column("W")
    satm = tf.feature_column.numeric_column("SATM")
    satr = tf.feature_column.numeric_column("SATR")
    rank = tf.feature_column.numeric_column("Rank")

    feat_cols = [unweight,weight,satm,satr,rank]

    stats = [unweightedGPA,weightedGPA,SATMath,SATReading,classRank]

    model = tf.estimator.DNNClassifier(feature_columns=feat_cols,hidden_units=[5,10], model_dir='ivy_model')

    multiplier=1
    if stats[4] > 8:
        multiplier = np.exp(-0.05*(stats[4]-8))
        stats[4] = 8
    data = pd.DataFrame({'UW': [stats[0]], 'W': [stats[1]], 'SATM': [stats[2]],
                         'SATR': [stats[3]], 'Rank': [stats[4]]})

    pred_fn = tf.estimator.inputs.pandas_input_fn(x=data,num_epochs=1,shuffle=False)

    pred_gen = list(model.predict(input_fn=pred_fn))

    likelyhood = pred_gen[0]['logistic']
    likelyhood = round(multiplier*likelyhood[0]*100,2)

    return ("You are "+str(likelyhood)+"% likely to get into Ivy")

if __name__ == "__main__":
    app.run(debug=True)
