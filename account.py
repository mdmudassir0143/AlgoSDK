import base64
import json
import algosdk

def create_account_and_export():
    # Create an account
    private_key, public_address = algosdk.account.generate_account()
    
    # Convert private key to mnemonic (passphrase)
    passphrase = algosdk.mnemonic.from_private_key(private_key)
    
    # Print account details
    print(f"My address: {public_address}")
    print(f"My passphrase: {passphrase}")
    
    # Create dispenser URL
    dispenser_url = f"https://dispenser.testnet.aws.algodev.network/?account={public_address}"
    print(f"Fund the wallet via Algorand Dispenser: {dispenser_url}")
    
    # Wait for user to confirm funding
    input("Press Enter when the account is funded...")
    
    # Convert private key to base64
    # Ensure private_key is converted to bytes if it's not already
    private_key_bytes = private_key.encode('utf-8') if isinstance(private_key, str) else private_key
    private_key_base64 = base64.b64encode(private_key_bytes).decode('utf-8')
    
    # Prepare account data
    account_data = {
        "address": public_address,
        "passphrase": passphrase,
        "privateKey": private_key_base64
    }
    
    # Export to JSON
    with open('account.json', 'w') as f:
        json.dump(account_data, f, indent=2)
    
    print("Account details exported to account.json")

# Run the script
if __name__ == '__main__':
    create_account_and_export()
