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

@app.route('/<role>/login', methods=['POST'])
def login(role):
    
    requestBody = request.get_json()
    
    mail = requestBody['mail']
    passw = requestBody['password']
    
    print("Received Mail: " + mail)
    print("Received Password: " + passw)
    


    headerToken = {
        "mail" : mail, 
        "algo":"HS256"
    }
    
    
    RequestToBEBody = {
        "email" : mail
    }
    
    toEncryptData = { 
        h_mail:mail, 
        h_pass:passw, 
        h_role : role
    }
    
    # Depending on role i will do requests on differt servers
    if role == "farmer":
        dict_response = requests.post(url=dbFarmerAddress+"/login", json = RequestToBEBody)
    elif role == "client":
        dict_response = requests.post(url=dbClientAddress+"/login", json = RequestToBEBody)
    
    #response = requests.post(url=dbAddress, json = RequestToFarmerBody)
    
    print("Response from Farmer_BE")
    
    print(dict_response.json())
    
    # if the db response = no succ -> no mail in the db
    if( not dict_response[h_succ] ):
        suc = False
        token = s_invalidToke
        errString = "NO_MAIL"
        
    # if invalid password and valid
    elif(dict_response[h_pass] != passw ):
        token = s_invalidToke
        suc = False
        errString = "NO_PASS"
    else:
        token = jwt.encode(payload=toEncryptData, key=secret, algorithm="HS256",headers=headerToken)
        suc = False
        errString = "GOOD"
    
    
    return jsonify({h_succ : suc , h_token: token, h_errStringLogin:errString})


    

@app.route('/<role>/signup', methods=['POST'])
def register(role):
    
    # Get all info per specification
    
    requestBody = request.get_json()
    
    mail = requestBody[h_mail]
    passw = requestBody[h_pass]
    username = requestBody[h_username]
    image = requestBody[h_image]
    area = requestBody[h_area]
    address = requestBody[h_address]

    #head of toke, uncrypted
    headerToken = {
        h_mail : mail, 
        h_role: role, 
        "algo":"HS256" 
    }
    
    # Paramethers for the post request to the db
    #head = {h_mail : mail, h_pass : passw, h_username : username, h_image:image,h_area:area,h_address:address}
    
    # Body for the post request to the db
    
    if (role == "farmer"):
    
        postBody = {
            "username" : username,
            "email" : mail,
            "password" : passw,
            "image" : image,
            "area" : area,
            "address" : address
        }
    
    
        # Response
        dictResponse = requests.post(url=dbFarmerAddress, json=postBody)


        #print("FarmerBE Response:")
        #print(dictResponse.json())

        # Body of the response
        ResponseBody = dictResponse.json()
    
    elif (role == "client"):
        postBody = {
            "username" : username,
            "email" : mail,
            "password" : passw
        }
    
    
        # Response
        dictResponse = requests.post(url=dbFarmerAddress, json=postBody)


        #print("FarmerBE Response:")
        #print(dictResponse.json())

        # Body of the response
        ResponseBody = dictResponse.json()
    
    print("User succesfully created in the db")
    
    #return ResponseBody
    
    #Succesfuly created user in db
    if(ResponseBody['success'] == True):
        
        dictToEncode = {
            h_mail : mail,
            h_pass : passw,
            h_role : role
        }
    
        token = jwt.encode(payload=dictToEncode, key=secret, algorithm="HS256", headers=headerToken).decode('utf-8')
        
        #token = jwt.encode(payload=dict({h_mail:mail, h_pass:passw, h_role : role}), key=secret, algorithm="HS256",headers=headerToken)
        suc = True
    
    
    # no new user
    else:
        token = s_invalidToke
        suc = False
    
    
    finalResponse = {
        h_succ : suc,
        h_token: token
    }
    
    return finalResponse
    
    #return jsonify({h_succ:suc, h_token: token})
    
    
@app.route('/verifyToken', methods=['POST'])
def verifyToken():
    
    requestBody = request.get_json()
    
    token_received = requestBody[h_token]
    
    try:
        dicHeaders = jwt.get_unverified_header(token_received)
        
        print(dicHeaders)
        
        verify = jwt.decode(token_received, secret, algorithms=dicHeaders["algo"])

        return jsonify({h_succ:True})
        
        
    except jwt.exceptions.DecodeError:
        
        return jsonify({h_succ:False})
    
    return jsonify({h_succ:False})
    
if __name__ == "__main__":
    app.run(debug=True, port=9701, host='0.0.0.0')
    