import requests
from flask import Flask, render_template, request
from twilio.rest import Client

account_sid = 'AC18eb24b4597adafe5d234b092c7a7479';
auth_token = '94d05c3f89a3f19b5b05d0edaf5670f5';

client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('Welcome_page.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/form', methods=['POST', 'GET'])
def login_registration_dtls():
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    source_st = request.form['source_state']
    source_dt = request.form['source_city']
    destination_st = request.form['destination_state']
    destination_dt = request.form['destination_city']
    email_id = request.form['email']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    reason=request.form['reason']
    date = request.form['trip']
    full_name = first_name+"."+last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="whatsapp:+91"+phoneNumber,
                               from_="whatsapp:+14155238886",
                               body="Hello "+" "+full_name+", "+",We are glad to tell you that your travel from"+" "+source_dt+" "+"to"+" "+destination_dt+" "
                                    + "has"+" been "+status+" "+"on "+date)
        return render_template('user_registration_details.html', pl0=full_name, pl1=email_id, 
                               pl2=source_st, pl3=source_dt, pl4=destination_st, pl5=destination_dt,pl6=id_proof,
                               pl7=phoneNumber, pl8=date, pl9=status,pl10=reason)
    else:
        status='Not Confirmed'
        client.messages.create(to="whatsapp:+91"+phoneNumber,
                               from_="whatsapp:+14155238886",
                               body="Hello " + " " + full_name + " " + ",We are sorry to say that you travel from" + " " + source_dt + " " + "to" + " " + destination_dt + " "
                                    + "has" + " " + status + " " + "on " + date + ".We would recommend you to try again after couple of days.")
        return render_template('user_registration_details.html', pl0=full_name, pl1=email_id, 
                               pl2=source_st, pl3=source_dt, pl4=destination_st, pl5=destination_dt,pl6=id_proof,
                               pl7=phoneNumber, pl8=date, pl9=status,pl10=reason)


if __name__ == "__main__":
    app.run(port=5000, debug=True,use_reloader=False)
