from main import *
from flask import  request,jsonify
import bcrypt
from json import dumps,JSONEncoder
db=client.db
@app.route('/signup',methods=['POST'])
def signup():
    req=request.json
    name=req['name']
    mail=req['mail']
    password=req['password']
    if request.method == 'POST' and name and mail and password:
        print("running....")
        try:
            data=db.users.find_one({"mail":mail})
            print(data)
            if(data is not None):
                print("Email already exists")
                res={
                    "err":"Mail id already present,Try using another Mail"
                }
            else:
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                try:
                    db.users.insert_one({
                    "name":name,
                    "mail":mail,
                    "password":password,
                    })
                    res={
                    "msg":"Success"
                    }
                except Exception as e:
                    res={
                        "err":e
                    }
                    return jsonify(res)
        except Exception as e:
            res={
                "err":e
            }     

        return jsonify(res)

    else:
        res={
            "err":"Enter all the fields"
        }
        return jsonify(res)
@app.route('/login',methods=['POST'])
def login():
    req=request.json
    mail=req["mail"]
    password=req["password"]
    if mail and password and request.method=='POST':
        print("running...")
        try:
            data=db.users.find_one({"mail":mail})
            flag=bcrypt.checkpw(password.encode('utf-8'), data["password"])
            if flag:
                res={
                    "name":data["name"],
                    "mail":data["mail"],
                    "id":data["_id"]
   
                }
                return dumps(res,default=str)
            else:
                res={
                    "err":"Check your password"
                }
            return jsonify(res)
        except Exception as e:
            print(e)
            res={
                "err":"An error occures"
            }
            return jsonify(res)
    else:
        res={
            "err":"Provide all the fields"
        }
        return jsonify(res)
@app.route('/deleteuser',methods=['DELETE'])
def deleteuser():
    req=request.json
    mail=req["mail"]
    password=req["password"]
    if mail and password and request.method == 'DELETE':
        print("Running...")
        data=db.users.find_one({"mail":mail})
        if(data is None):
            res={
                "err":"No user found"
            }
            return jsonify(res)
        else:
            try:
                flag=bcrypt.checkpw(password.encode('utf-8'), data["password"])
                if(flag):
                    x=db.users.delete_one({"mail":mail})
                    print(x)
                    res={
                        "msg":"User successfully deleted"
                    }
                    return jsonify(res)
                else:
                    res={
                        "err":"You dont enough permission to delete or your password may be incorrect"
                    }
                    return jsonify(res)
            except Exception as e:
                res={
                    "err":e
                }
                return jsonify(res)
    else:
        res={
            "err":"Provide all the details"
        }
        return jsonify(res)
@app.route('/changepassword',methods=['PUT'])
def changepassword():
    req=request.json
    mail=req["mail"]
    oldpassword=req["oldpassword"]
    newpassword=req["newpassword"]
    if mail and oldpassword and newpassword and request.method=="PUT":
        try:
            print("running...")
            data=db.users.find_one({"mail":mail})
            flag=bcrypt.checkpw(oldpassword.encode('utf-8'),data["password"],)
            if flag:
                myquery = { "mail": mail }
                password=bcrypt.hashpw(newpassword.encode('utf-8'),bcrypt.gensalt())
                newvalues = { "$set": { "password": password } }
                db.users.update(myquery,newvalues)
                print("updated successfully")
                res={
                    "msg":"Password updated successfully"
                }
                return jsonify(res)
            else:
                res={
                    "err":"You dont have enough permission to change or your old password may be incorrect"
                }
                return jsonify(res)
        except Exception as e:
            res={
                "err":e
            }
            return jsonify(res)

    else:
        res={
            "err":"Provide al the details"
        }
        return jsonify(res)
