from flask import Flask, request, jsonify, make_response, request, render_template, session, flash
import jwt
import requests
import json

app = Flask(__name__)

secret = "My_very_important_secret"

h_mail = "email"
h_pass = "password"
h_role = "role"
h_username = "username"
h_image = "image"
h_area= "area"
h_token = "token"
h_name = "name"
h_address = "address"
h_succ = "success"

dbAddress = "http://127.0.0.1:9703/login"
dbAddressSU = "http://127.0.0.1:9703/signup"

s_invalidToke = "FAIL"

@app.route('/login', methods=['POST'])
def login():
    
    mail = request.args.get(h_mail)
    passw = request.args.get(h_pass)
    role = "Client"

    headerToken = {"mail" : mail, "algorithm":"HS256", "algo":"HS256" }
    
    head = {h_mail : "test@gmail.com"}
    
    dict_response = requests.post(url=dbAddress, params=head)
    
    #print(dict_response.text)
    
    r = json.loads(dict_response.text)
    
    
    if(r[h_pass] == passw ):
        token = jwt.encode(payload=dict({h_mail:mail, h_pass:passw, h_role : role}), key=secret, algorithm="HS256",headers=headerToken)
        suc = True
    else:
        token = s_invalidToke
        suc = False
    
    
    return jsonify({h_succ : suc , h_token: token })

#Request
@app.route('/signup', methods=['POST'])
def register():
    
    # Get all info per specification
    
    mail = request.args.get(h_mail)
    passw = request.args.get(h_pass)
    #name = request.args.get(h_name)
    username = request.args.get(h_username)
    image = request.args.get(h_image)
    area = request.args.get(h_area)
    address = request.args.get(h_address)
    role = "Client"

    #head of toke, uncrypted
    headerToken = {h_mail : mail, h_role: role, "algo":"HS256" }
    
    # Paramethers for the post request to the db
    head = {h_mail : mail, h_pass : passw, h_username : username, h_image:image,h_area:area,h_address:address}
    
    # Response
    dict_response = requests.post(url=dbAddressSU, params=head)
    
    #print(dict_response.text)
    
    # get the dictionary of the response
    r = json.loads(dict_response.text)
    
    
    #Succesfuly created user in db
    if(r[h_succ] ):
        token = jwt.encode(payload=dict({h_mail:mail, h_pass:passw, h_role : role}), key=secret, algorithm="HS256",headers=headerToken)
        suc = True
    # no new user
    else:
        token = s_invalidToke
        suc = False
    
    return jsonify({h_succ:suc, h_token: token})

@app.route('/verifyToken', methods=['GET'])
def verifyToken():
    token_recived = request.args.get(h_token)
    
    try:
        dicHeaders = jwt.get_unverified_header(token_recived)
        
        print(dicHeaders)
        
        verify = jwt.decode(token_recived, secret, algorithms=dicHeaders["algo"])

        return jsonify({h_succ:True})
        
        
    except jwt.exceptions.DecodeError:
        
        return jsonify({h_succ:False})
    
    return jsonify({h_succ:False})

if __name__ == "__main__":
    app.run(debug=True)