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
h_errStringLogin = "error"

dbClientAddress = "http://client-be:9702"
dbFarmerAddress = "http://farmer-be:9703"

s_invalidToke = "FAIL"

# LOGIN
# role : farmer or client
@app.route('/<role>/login', methods=['POST'])
def farmer_login(role):
    
    mail = request.args.get(h_mail)
    passw = request.args.get(h_pass)

    #uncripted header
    headerToken = {"mail" : mail,h_role:role, "algo":"HS256" }
    
    #to be cryped headers
    toEncryptToken = dict({h_mail:mail, h_pass:passw, h_role : role})
    
    # Request to BE:
    head = {h_mail : mail}
    
    # Depending on role i will do requests on differt servers
    if role == "farmer":
        dict_response = requests.get(url=dbFarmerAddress+"/login", params=head)
    elif role == "client":
        dict_response = requests.get(url=dbClientAddress+"/login", params=head)
    
    # Debug
    print(dict_response.text)    
    
    # Response dictionary
    r = json.loads(dict_response.text)
    
    # if the db response = no succ -> no mail in the db
    if( not r[h_succ] ):
        suc = False
        token = s_invalidToke
        errString = "NO_MAIL"
        
    # if invalid password and valid
    elif(r[h_pass] != passw ):
        token = s_invalidToke
        suc = False
        errString = "NO_PASS"
    else:
        token = jwt.encode(payload=toEncryptToken, key=secret, algorithm="HS256",headers=headerToken)
        suc = False
        errString = "GOOD"
    
    
    return jsonify({h_succ : suc , h_token: token, h_errStringLogin:errString})


# SIGNUP
# role : "farmer", "client"
@app.route('/<role>/signup', methods=['POST'])
def register(role):
    
    # Get all info per specification
    
    mail = request.args.get(h_mail)
    passw = request.args.get(h_pass)
    name = request.args.get(h_name)
    username = request.args.get(h_username)
    image = request.args.get(h_image)
    area = request.args.get(h_area)
    address = request.args.get(h_address)
    
    #head of toke, uncrypted
    headerToken = {h_mail : mail, h_role: role, "algo":"HS256" }
    
    # to be encrypted info
    toEncyptToken = dict({h_mail:mail, h_pass:passw, h_role : role})
    
    
    if role == "farmer":
    
        # Paramethers for the post request to the db
        head = {h_mail : mail, h_pass : passw, h_username : username, h_image:image, h_area:area,h_address:address}
    
        # Response
        dict_response = requests.post(url=dbFarmerAddress, params=head)
    
    elif role == "client":
        # Paramethers for the post request to the db
        head = {h_mail : mail, h_pass : passw, h_name : name}
    
        # Response
        dict_response = requests.post(url=dbClientAddress, params=head)
    
    # debug
    #print(dict_response.text)
    
    # get the dictionary of the response
    r = json.loads(dict_response.text)
    return head
    
    #Succesfuly created user in db
    if(r[h_succ] ):
        token = jwt.encode(payload=toEncyptToken, key=secret, algorithm="HS256",headers=headerToken)
        suc = True
        
    # no new user created -> alread in system the mail
    else:
        token = s_invalidToke
        suc = False
    
    return jsonify({h_succ:suc, h_token: token})

# Verification

@app.route('/verifyToken', methods=['GET'])
def verifyToken():
    
    token_recived = request.args.get(h_token)
    
    try:
        
        # unverified toke headers
        dicHeaders = jwt.get_unverified_header(token_recived)
        
        #check
        print(dicHeaders)
        
        #to verify
        verify = jwt.decode(token_recived, secret, algorithms=dicHeaders["algo"])

        #return success
        return jsonify({h_succ:True,h_mail:verify[h_mail]})
        
        
    except jwt.exceptions.DecodeError:
        
        return jsonify({h_succ:False,h_mail:"Error Mail"})
    
    return jsonify({h_succ:False,h_mail:"Error"})

if __name__ == "__main__":
    app.run(debug=True, port=9701, host='0.0.0.0')