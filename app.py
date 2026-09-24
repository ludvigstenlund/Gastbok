from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
import json

app = Flask(__name__)

SAVEDOC = "EgnaProjekt/LitenSida/static/json/savedata.json" #snyggare än att skriva in hela sökvägen varje gång

def las_json(): #Läser JSON-filen
    if os.path.exists(SAVEDOC): #...men bara om den finns
        with open(SAVEDOC, 'r', encoding='utf-8') as f: #utf-8 för bl.a åäö
            try:
                return json.load(f)
            except json.JSONDecodeError:
                
                return []
    return []


@app.route('/') #laddar hemsida
def home():
    return render_template('home.html')


@app.route('/survey', methods=['GET', 'POST']) #sidan för undersökningen
def survey():

    content_list = las_json() #anropar att läsa json-filen

    content_str = json.dumps(content_list, indent=4, ensure_ascii=False) #bestämmer hur saker ska skrivas till json-filen
    return render_template('survey.html', file_content=content_str, data=content_list)


@app.route('/append', methods=['POST']) #när man skickar in undersökningen
def append(): #append för att lägga till i json

    if request.form['Textruta_att_skriva_i']: #om det finns något att skicka in
        ny_data = { #objekt för en kommentar
            "namn": request.form['Textruta_att_skriva_namn_i'],
            "åsikt": request.form['Textruta_att_skriva_i'],
            "tidpunkt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        tidigare_data = las_json() #sparar den data som fanns tidigare

        tidigare_data.append(ny_data) #lägger på den nya kommentaren

        os.makedirs(os.path.dirname(SAVEDOC), exist_ok=True) #ser till så att savedata.json skapas korrekt, och inte krashar om denna inte finns.
        with open(SAVEDOC, "w", encoding="utf-8") as f:
            json.dump(tidigare_data, f, indent=4, ensure_ascii=False) #tidigare data är nu den totala datan, borde kanske byta namn för tydlighet

    return redirect(url_for('survey')) #laddar in survey.html igen


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')