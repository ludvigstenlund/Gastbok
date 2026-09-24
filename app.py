from flask import Flask, render_template, request
import os
import datetime

app = Flask(__name__)

SAVEDOC = "EgnaProjekt/LitenSida/static/json/savedata.json"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    content = ''
    if os.path.exists(SAVEDOC):
        with open(SAVEDOC, 'r', encoding='utf-8') as f:
            content = f.read()
    return render_template('survey.html', file_content=content)


@app.route('/append', methods=['POST'])
def append():
    namn = request.form['Textruta_att_skriva_namn_i']
    skrivet_i_rutan = request.form['Textruta_att_skriva_i']
    if skrivet_i_rutan: 

        with open(SAVEDOC, "a", encoding="utf-8") as f:
            f.write(f'\n\n{namn} skrev: \n"{skrivet_i_rutan}" \nDetta gjordes {datetime.datetime.now()}')

    with open(SAVEDOC, "r", encoding="utf-8") as f:
        content = f.read()
    return render_template('survey.html', file_content=content)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')