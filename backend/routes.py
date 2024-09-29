from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"Message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return all data"""
    if data:
        return jsonify(data), 200

    return {"Message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return a data when id"""
    if data:
        picture_found = None
        for picture in data:
            if int(picture["id"]) == int(id):
                picture_found = picture
                break
        if  picture_found:                     
            return jsonify(picture_found), 200
        return {"Message": "picture not found"}, 404   
    return {"Message": "Internal server error"}, 500    
    
######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """create a picture from JSON POST"""
    data_req = request.json
    if data:
        picture_found = None
        for picture in data:
            if int(picture["id"]) == int(data_req["id"]):
                picture_found = picture
                break
        if  picture_found:                     
            return {"Message": f"picture with id {picture['id']} already present"}, 302 
        data.append(data_req)
        return jsonify(data_req), 201   
    return {"Message": "Internal server error"}, 500      

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update a picture from JSON PUT"""
    data_req = request.json
    if data:
        picture_found = None
        for picture in data:
            if int(picture["id"]) == int(data_req["id"]):
                picture["pic_url"]=data_req["pic_url"]
                picture["event_country"]=data_req["event_country"]
                picture["event_state"]=data_req["event_state"]
                picture["event_city"]=data_req["event_city"]
                picture["event_date"]=data_req["event_date"]
                picture_found = picture
                break
        if  picture_found:                     
            return jsonify(picture_found), 200
        return {"Message": "picture not found"}, 404  
    return {"Message": "Internal server error"}, 500   

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete a picture from JSON DELETE"""
    if data:
        picture_found = None
        for picture in data:
            if int(picture["id"]) == int(id):
                picture_found = picture
                break
        if  picture_found:
            data.remove(picture_found)                     
            return jsonify(picture_found), 204
        return {"Message": "picture not found"}, 404   
    return {"Message": "Internal server error"}, 500   
