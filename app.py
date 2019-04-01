from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import ivy_model as ivy
app = Flask(__name__)

colleges_dict = {
    'Stanford': [0,5.0],
    'Harvard': [0,5.6],
    'MIT': [0,8.3],
    'Princeton': [0,7.1],
    'Yale': [0,6.7],
    'Columbia': [0,6.6]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chanceme')
def form():
    return render_template('form.html')

@app.route('/chanceme', methods=['POST'])
def formPost():
    tier1 = ['Stanford','Harvard', 'MIT', 'Princeton', 'Yale', 'Columbia']
    unweightedGPA = request.form.get('unweightedGPA', type=float)
    weightedGPA = request.form.get('weightedGPA', type=float)
    SATMath = request.form.get('SATMath', type=int)
    SATReading = request.form.get('SATReading', type=int)
    classRank = request.form.get('classRank', type=int)
    if request.form.get('tos') == None:
        return render_template('form.html', message='Box must be checked before submission')
    try:
        float(unweightedGPA)
    except TypeError:
        return render_template('form.html', message='Unweighted GPA must be between 2.0 and 4.0')
    try:
        float(unweightedGPA)
    except TypeError:
        return render_template('form.html', message='Weighted GPA must be between 2.0 and 5.0')
    try:
        int(SATMath/10)
    except TypeError:
        return render_template('form.html', message='Invalid SAT Math score')
    try:
        int(SATReading/10)
    except TypeError:
        return render_template('form.html', message='Invalid SAT Reading score')
    try:
        int(classRank)
    except TypeError:
        return render_template('form.html', message='Invalid class rank. Must be an integer.')

    if unweightedGPA < 2.0 or unweightedGPA > 4.0:
        return render_template('form.html', message='Unweighted GPA must be between 2.0 and 4.0')
    if weightedGPA < 2.0 or weightedGPA > 5.0:
        return render_template('form.html', message='Weighted GPA must be between 2.0 and 5.0')
    if SATMath > 800 or SATMath < 200:
        return render_template('form.html', message='SAT Math score must be between 200 and 800.')
    if SATReading > 800 or SATReading < 200:
        return render_template('form.html', message='SAT Reading score must be between 200 and 800.')
    if classRank < 1:
        return render_template('form.html', message='Invalid Class Rank')



    for i in range(len(tier1)):
        colleges_dict[tier1[i]][0] = ivy.algo(unweightedGPA, weightedGPA, SATMath, SATReading, classRank, tier1[i])

    return render_template('results.html', colleges_dict=colleges_dict, colleges=list(colleges_dict.keys()), num_colleges=6)
if __name__ == "__main__":
    app.run(debug=True)
