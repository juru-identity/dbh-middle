from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import json
from flask import Flask, url_for, request
app = Flask(__name__)
bdb = BigchainDB('http://localhost:59984')

class BigChainDBInterface:

    def generateActor(self):
        return generate_keypair()

    def createAsset(self, asset, assetType, recipientPublicKey, recipientPrivateKey):
        metadata = {'Identity': assetType}
        prepared_creation_tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=recipientPublicKey,
            asset=asset,
            metadata=metadata,
            )
        prepared_creation_tx
        fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx, private_keys=recipientPrivateKey)
        sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)
        txid = fulfilled_creation_tx['id']
        return txid

    def transferAsset(self, assetId,signingKey,recipientKey):
        transfer_asset = {
            'id' : assetId,
        }
        output_index = 0
        output = creation_tx['outputs'][output_index]
        transfer_input = {
            'fulfillment' : output['condition']['details'],
            'fulfills': {
            'output' : output_index,
            'txid' : assetId,
        },
        'owners_before': output['public_keys'],
        }
        prepared_transfer_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=recipientKey,
        )
        fulfilled_transfer_tx = bdb.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=signingKey,
        )
        sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)
        return sent_transfer_tx


@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/createAsset',methods=['POST'])
def api_createAsset():
    JSONobject=request.get_json()
    bcI = BigChainDBInterface()

    res = bcI.createAsset(JSONobject['asset'], JSONobject['assetType'], JSONobject['recipientPublicKey'], JSONobject['recipientPrivateKey'])
    payload = {
      'asset': res
    }
    return json.dumps(res)

@app.route('/transferAsset',methods=['POST'])
def api_transferAsset():
    JSONobject=request.get_json()
    bcI = BigChainDBInterface()
    return  bcI.createAsset(JSONobject['assetId'],JSONobject['signingPrivateKey'], JSONobject['recipientPublicKey'])

@app.route('/demo',methods=['POST'])
def api_demo():
    print(request)
    JSONobject=request.get_json()
    print(JSONobject)
    return  json.dumps(JSONobject)

@app.route('/generateActor')
def api_generateActor():
    bcI = BigChainDBInterface()
    keypair = bcI.generateActor()
    JSONReturnValue = {'publicKey': keypair.public_key,
                        'privateKey': keypair.private_key,
                       }
    return json.dumps(JSONReturnValue)

if __name__ == '__main__':
    app.run()
