import json
import base64
from algosdk import transaction
from algosdk.v2client import algod

def deploy_token():
    # Read the account details from JSON
    with open('account.json', 'r') as file:
        account_data = json.load(file)
    
    # Extract address and private key
    address = account_data['address']
    private_key = base64.b64decode(account_data['privateKey'])
    
    # Connect to Algorand Testnet
    print("Connecting to Algorand Testnet")
    algod_address = 'https://testnet-api.algonode.cloud'
    algod_token = ''
    algod_client = algod.AlgodClient(algod_token, algod_address)
    
    # Get suggested transaction parameters
    params = algod_client.suggested_params()
    
    # Create an asset creation transaction
    print("Creating the Token Metadata")
    txn = transaction.AssetConfigTxn(
        sender=address,
        sp=params,
        default_frozen=False,
        unit_name='Meme',  # Symbol
        asset_name='Meme Coin',  # Name of the asset
        manager=address,
        reserve=address,
        freeze=address,
        clawback=address,
        total=1000,
        decimals=0
    )
    
    # Sign the transaction
    signed_txn = txn.sign(private_key)
    
    # Submit the transaction to the network
    try:
        # Send transaction
        txid = algod_client.send_transaction(signed_txn)
        
        # Wait for confirmation
        print("Waiting for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
        
        # Get the asset ID
        asset_id = confirmed_txn['asset-index']
        print(f"Token deployed. Asset ID: {asset_id}")
        
        # Display AlgoExplorer URL
        url = f"https://app.dappflow.org/explorer/asset/{asset_id}"
        print(f"Asset URL: {url}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the deployment
if __name__ == '__main__':
    deploy_token()
