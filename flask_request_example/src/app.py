import requests
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

conn = psycopg2.connect(host='127.0.0.1',
                            database='testdb',
                            user="postgres",
                            password="postgres",
                            port = "5432")


cur = conn.cursor()
# cur.execute('''CREATE TABLE ADDRESS
#       (NFT_ADDR TEXT PRIMARY KEY     NOT NULL);''')
# conn.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nfr_address = request.form['first_name']
        cur.execute("SELECT * from ADDRESS WHERE NFT_ADDR=%s", (nfr_address,))
        if cur.fetchall(): # checking if something found with this address
            print("already exists")
            url = f"https://solana-gateway.moralis.io/nft/mainnet/{nfr_address}/metadata"
            headers = {
                        "accept": "application/json",
                        "X-API-Key": "FzA6L5hendGEXQzNFOFcOAQfAqWbVNaMs8mLQNWVk1diN6nNN0DpeQWJB2HEbdsY"
                    }
            response = requests.get(url, headers=headers)
            rep = response.json()
            return render_template('index.html', rep=rep)
        else:
            cur.execute("INSERT INTO ADDRESS (NFT_ADDR) VALUES (%s)", (nfr_address,))
            conn.commit()
            print('inserted succesfully')
            return render_template('index.html')
    return render_template('create.html')


@app.route('/create.html', methods=('GET', 'POST'))
def create():
    return render_template('create.html')

if __name__ == '__main__':

    app.run(debug=True) #

conn.close()
