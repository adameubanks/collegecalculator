import numpy as np
import pandas as pd
import tensorflow as tf
def algo(unweightedGPA, weightedGPA, SATMath, SATReading, classRank, collegeSelected):
    unweight = tf.feature_column.numeric_column("UW")
    weight = tf.feature_column.numeric_column("W")
    satm = tf.feature_column.numeric_column("SATM")
    satr = tf.feature_column.numeric_column("SATR")
    rank = tf.feature_column.numeric_column("Rank")
    m = 0
    r = 0
    if collegeSelected == "Stanford":
        m = -10
        r = 0
    elif collegeSelected == "Harvard":
        m = -20
        r = -30
    elif collegeSelected == "MIT":
        m = 0
        r = -50
    elif collegeSelected == "Princeton":
        m = 0
        r = -30
    elif collegeSelected == "Yale":
        m = -30
        r = -30
    elif collegeSelected == "Colombia":
        m = 0
        r = -20

    feat_cols = [unweight, weight, satm, satr, rank]

    stats = [unweightedGPA, weightedGPA, SATMath+m, SATReading+r, classRank]

    model = tf.estimator.DNNClassifier(feature_columns=feat_cols, hidden_units=[5, 10], model_dir='ivy_model')

    multiplier = 1
    if stats[4] > 8:
        multiplier = np.exp(-0.05 * (stats[4] - 8))
        stats[4] = 8
    data = pd.DataFrame({'UW': [stats[0]], 'W': [stats[1]], 'SATM': [stats[2]],'SATR': [stats[3]], 'Rank': [stats[4]]})

    pred_fn = tf.estimator.inputs.pandas_input_fn(x=data, num_epochs=1, shuffle=False)

    pred_gen = list(model.predict(input_fn=pred_fn))
    if SATMath+SATReading < 1400:
        multiplier = multiplier / 2
    if unweightedGPA < 3.0:
        multiplier = multiplier / 2
    if weightedGPA < 3.5:
        multiplier = multiplier / 2
    likelyhood = pred_gen[0]['logistic']
    likelyhood = round(multiplier * likelyhood[0] * 100, 2)

    return likelyhood
