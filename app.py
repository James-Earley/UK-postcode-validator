from flask import Flask, request, render_template
import requests

app = Flask(__name__)

POSTCODES_IO_URL = "https://api.postcodes.io/postcodes/"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        postcode = request.form['postcode'].strip().replace(' ', '')
        api_url = f"{POSTCODES_IO_URL}{postcode}"

        try:
            response = requests.get(api_url)
            data = response.json()

            if response.status_code != 200 or not data.get('result'):
                message = '❌ Invalid postcode. Please try again.'
            else:
                constituency = data['result']['parliamentary_constituency']
                district = data['result']['admin_district']
                region = data['result']['region']
                country = data['result']['country']

                # Check if the postcode falls within Finchley and Golders Green
                if constituency == "Finchley and Golders Green":
                    message = (f"✅ Postcode is in Finchley and Golders Green.<br>"
                               f"📍 District: {district}<br>"
                               f"🌍 Region: {region}<br>"
                               f"🏴 Country: {country}")
                else:
                    message = (f"❌ Postcode is in '{constituency}', not Finchley and Golders Green.<br>"
                               f"📍 District: {district}<br>"
                               f"🌍 Region: {region}<br>"
                               f"🏴 Country: {country}")
        except Exception as e:
            message = f"⚠️ Error during validation: {str(e)}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
