import json
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

cur.execute('''CREATE TABLE IF NOT EXISTS nft_information

      (nft_addr VARCHAR(100),

      info json);''')

conn.commit()

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('create.html')

@app.route('/nft', methods=[ 'GET', 'POST'])
def nft():
        nft_address = request.args.get('nftaddr')
        cur.execute("SELECT * from nft_information WHERE NFT_ADDR=%s", (nft_address,))
        conn.commit()
        if cur.fetchall(): 
            url =f"https://solana-gateway.moralis.io/nft/mainnet/{nft_address}/metadata"
            headers = {
                        "accept": "application/json",
                        "X-API-Key": "FzA6L5hendGEXQzNFOFcOAQfAqWbVNaMs8mLQNWVk1diN6nNN0DpeQWJB2HEbdsY"
                    }
            response = requests.get(url, headers=headers)
            query_sql1 = """ UPDATE nft_information SET info = (%s)  WHERE nft_addr = (%s); """
            
            somth = response.json
            rep = json.dumps(somth()) 
                          
            cur.execute(query_sql1, (rep,nft_address,))
            conn.commit()
            cur.execute (" select info -> 'name' from nft_information WHERE nft_addr = (%s)", (nft_address,))
            name_of_nft = cur.fetchone()
            
            cur.execute (" select info -> 'metaplex' -> 'metadataUri' from nft_information WHERE nft_addr = (%s)", (nft_address,))
            nft_img_url = cur.fetchone()

            cur.execute (" select info -> 'mint'  from nft_information WHERE nft_addr = (%s)", (nft_address,))
            nft_mint = cur.fetchone()
            conn.commit()
            return render_template('index.html', nm=name_of_nft[0], imgurl = nft_img_url[0], mint = nft_mint[0])
        else:
            cur.execute("INSERT INTO nft_information (NFT_ADDR) VALUES (%s)", (nft_address,))
            conn.commit()
            return render_template('create.html')
    

if __name__ == '__main__':

    app.run(debug=True) #

conn.close()
