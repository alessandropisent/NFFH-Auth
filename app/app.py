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

dbAddress = "http://farmer-be:9703/farmer/login"
dbAddressSU = "http://farmer-be:9703/farmer"

s_invalidToke = "FAIL"

@app.route('/login', methods=['POST'])
def login():
    
    requestBody = request.get_json()
    
    mail = requestBody['mail']
    passw = requestBody['password']
    
    print("Received Mail: " + mail)
    print("Received Password: " + passw)
    
    role = "Farmer"

    headerToken = {"mail" : mail, "algorithm":"HS256", "algo":"HS256" }
    
    head = {h_mail : mail}
    
    RequestToFarmerBody = {
        "email" : mail
    }
    
    response = requests.post(url=dbAddress, json = RequestToFarmerBody)
    
    print("Response from Farmer_BE")
    
    print(response.json())
    
    responseDict = response.json()
    


    if(responseDict[h_pass] == passw ):
        token = jwt.encode(payload=dict({h_mail:mail, h_pass:passw, h_role : role}), key=secret, algorithm="HS256",headers=headerToken).decode('utf-8')
        suc = True
    else:
        token = s_invalidToke
        suc = False
    
    
    return {h_succ : suc , h_token: token }
    
    

@app.route('/signup', methods=['POST'])
def register():
    
    # Get all info per specification
    
    requestBody = request.get_json()
    
    mail = requestBody[h_mail]
    passw = requestBody[h_pass]
    #name = request.args.get(h_name)
    username = requestBody[h_username]
    image = requestBody[h_image]
    area = requestBody[h_area]
    address = requestBody[h_address]

    role = "Farmer"

    #head of toke, uncrypted
    headerToken = {h_mail : mail, h_role: role, "algo":"HS256" }
    
    # Paramethers for the post request to the db
    #head = {h_mail : mail, h_pass : passw, h_username : username, h_image:image,h_area:area,h_address:address}
    
    # Body for the post request to the db
    
    postBody = {
        "username" : username,
        "email" : mail,
        "password" : passw,
        "image" : image,
        "area" : area,
        "address" : address
    }
    
    
    # Response
    dictResponse = requests.post(url=dbAddressSU, json=postBody)
    
    
    print("FarmerBE Response: ")
    print(dictResponse.json())
    
    # Body of the response
    ResponseBody = dictResponse.json()
    
    print("User succesfully created in the db")
    
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
    app.run(debug=True)
    