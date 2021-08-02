import yfinance as yf
import flask.json
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import boto3
from boto3 import resource
import decimal
from boto3.dynamodb.conditions import Key, Attr

# The boto3 dynamoDB resource
dynamodb_resource = resource('dynamodb')
from botocore.exceptions import ClientError

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DSE_MATHS_MC')

CORS(app)


# Helper class to convert a DynamoDB item to JSON.

class DecimalEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


app.json_encoder = DecimalEncoder


@app.route('/')
def hello_world():
    return 'Hello, World!'

'''
@app.route('/stock/<symbol>', methods=["GET"])
def get_stock(symbol):
    """
    get the stock
    """
    if not symbol:
        return {"error": True, "success": False, "data": None, 'msg': 'please specify the symbol'}

    ### URL params
    page = request.args.get("page")
    print(page)

    ### The logic and database CRUD operations are performed in here

    try:
        res = {}
        yahoo_data = yf.Ticker(symbol)

        res['ma200'] = yahoo_data.info['twoHundredDayAverage']
        res['ma50'] = yahoo_data.info['fiftyDayAverage']
        res['price'] = yahoo_data.info['previousClose']
        res['forward_pe'] = yahoo_data.info['forwardPE']
        res['forward_eps'] = yahoo_data.info['forwardEps']
        if yahoo_data.info['dividendYield'] is not None:
            res['dividend_yield'] = yahoo_data.info['dividendYield'] * 100

        return {'error': False, 'success': True, 'data': res, 'msg': 'return stock data'}

    except Exception as e:
        # traceback.print_exc()
        return {'error': True, 'success': False, 'data': None, 'msg': e.__str__()}
'''

@app.route('/maths', methods=["GET"])
def etf_list():
    year = int(request.args.get("year"))
    #per_page = int(request.args.get("per_page"))
    try:
        response = table.scan(
            #AttributesToGet=("Beta", "Name")
        )
        '''response = table.query(
        	KeyConditionExpression=Key('year').eq(year)
        )'''
        mc_list = response['Items']
        return {'error': False, 'success': True, 'data': mc_list,
                'msg': 'return mc answers'}
    except Exception as e:
        #tracebacks.print_exc()
        print(e)
        return {'error': True, 'success': False, 'data': None, 'msg': str(e)}


'''
@app.route('/etfInfo/<n>', methods=["GET"])
def etfinfo(n):
    try:
        response = table.get_item(
            Key={
                'unique_key': n
            }
        )
        item = response['Item']
        
        return {'error': False, 'success': True, 'data': item, 'msg': 'return term deposit info'}

    except Exception as e:
        # traceback.print_exc()
        print(e)
        return {'error': True, 'success': False, 'data': None, 'msg': 'No such term deposit'}
'''

if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host='0.0.0.0')


