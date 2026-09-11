from flask import Flask, render_template, request, render_template_string
import os

app = Flask(__name__)

SAVEDOC = "EgnaProjekt/LitenSida/static/json/savedata.json"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    content = ''
    if os.path.exists(SAVEDOC):
        with open(SAVEDOC, 'r', encoding='utf-8') as f: #Flaggan 'r' (read) anger att filen ska läsas
            content = f.read()
    return render_template('survey.html', file_content=content)


@app.route('/append', methods=['POST'])
def append():
    skrivet_i_rutan = request.form.get('Textruta_att_skriva_i', '')
    if skrivet_i_rutan: 

        print(f"Någon skrev {skrivet_i_rutan}")

        with open(SAVEDOC, "a", encoding="utf-8") as f:
            f.write(skrivet_i_rutan + "\n")

    with open(SAVEDOC, "r", encoding="utf-8") as f:
        content = f.read()
    return render_template('survey.html', file_content=content)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')