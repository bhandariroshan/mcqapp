#APA91bG3UXLSwnSDAfKZyWh3jcKaGHO1eFVYUBKm6hxwwEQm_FClctyJeamuiGSl6hktcjp74ocnpXv6NMcE4LZPoWtT898wrn6lFybgcwamV74aPy94tLV_KJCRxV8Xqo-cUSVMk_gHdbA9YWG1PT95QHd98lPudg

import requests
import json
url = 'https://android.googleapis.com/gcm/send'
payload = {'data':{"ma_message":"Did you get message santosh?","ma_title":"Test from Meroanswer"},
'registration_ids': ["APA91bGVuw85JlaP6eUPB07OLywjRyVUMctaPrbJx7pTWWSFNAeAwiVdT9lisleX8a2kFlvg2zNjuaxwzjua27XRDUM4QifQ5zy2p1YHjdKOTdBVxQEIId0PUxwv7l6ImowFh4tO8r6UwJoaYzvzd-keyEQpZf6DSQ","APA91bF61NHoXfH4gHoh74PVvKjUWaJjmVLGnH1fzNWP597u5idX6Do6H3moxMNw3h1fTaZNt2FnnPeaEWTtG1XHJwNPUQHUwsfvIJuUxbH9EeTxN5FQnx2IrAT8uVJg2h5yYMMsJ4r4ijUbsTWzc-u9lsE2XkkNyQ",
]}


headers = {'Authorization': 'key=AIzaSyAS9BHLJ6mQ9h8RIbMg2VGY7qeO1zB0Vt4','content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
