from flask import Flask, render_template, request, flash
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

    # if unweightedGPA or weightedGPA or SATMath or SATReading or classRank == 5:
    #     return render_template('form.html', error="Fill out all forms correctly!")
    for i in range(len(tier1)):
        colleges_dict[tier1[i]][0] = ivy.algo(unweightedGPA, weightedGPA, SATMath, SATReading, classRank, tier1[i])

    return render_template('results.html', colleges_dict=colleges_dict, colleges=list(colleges_dict.keys()), num_colleges=6)
if __name__ == "__main__":
    app.run(debug=True)
