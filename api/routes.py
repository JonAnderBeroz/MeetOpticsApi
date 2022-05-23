from flask import Blueprint, jsonify, redirect
from .MeetopicsScrapper import scrapper as sc
api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def apiInit():  
    return redirect('/getOptoSigmaData')

@api.route('/getOptoSigmaData', methods=['GET'])
def getOptoSigmaData():
    print('in')
    data = sc.getOptoSigmaData()
    print(data)
    if data:
        return jsonify({'response': 'success', 'data': data})
    else:
        return jsonify({'response': 'error'})
