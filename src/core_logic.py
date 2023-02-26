import sqlite3
import os
import base64
import hashlib
import hmac
import time
import ecdsa

# Initialize database connection
db = sqlite3.connect('spock_database.db')

def create_new_pair():
    # Generate a new ECDSA key pair for the user
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()

    # Save the key pair to the database
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (public_key, private_key) VALUES (?, ?)", (vk.to_string(), sk.to_string()))
    db.commit()

    # Return the public key to the user
    return vk.to_string()

def sign_message(public_key, message):
    # Find the user's private key from the database
    cursor = db.cursor()
    cursor.execute("SELECT private_key FROM users WHERE public_key = ?", (public_key,))
    row = cursor.fetchone()

    if row is not None:
        # Load the user's private key
        sk = ecdsa.SigningKey.from_string(row[0], curve=ecdsa.SECP256k1)

        # Sign the message with the private key
        signature = sk.sign(message.encode())

        # Save the signature to the database
        cursor.execute("INSERT INTO signatures (public_key, signature) VALUES (?, ?)", (public_key, signature))
        db.commit()

        # Return the signature to the user
        return signature

def create_web_token(public_key):
    # Find the user's signature from the database
    cursor = db.cursor()
    cursor.execute("SELECT signature FROM signatures WHERE public_key = ?", (public_key,))
    row = cursor.fetchone()

    if row is not None:
        # Generate a web token for the user
        secret_key = os.urandom(16)
        timestamp = int(time.time())
        message = '{}:{}'.format(public_key, timestamp).encode()
        signature = hmac.new(secret_key, message, hashlib.sha256).digest()

        # Save the secret key and web token to the database
        cursor.execute("INSERT INTO tokens (public_key, secret_key, timestamp, signature) VALUES (?, ?, ?, ?)",
                       (public_key, secret_key, timestamp, signature))
        db.commit()

        # Return the web token to the user
        token_data = {
            'public_key': public_key,
            'timestamp': timestamp,
            'signature': base64.b64encode(signature).decode(),
        }
        return base64.b64encode(str(token_data).encode()).decode()

# Create a new user key pair and save it to the database
public_key = create_new_pair()

# Sign a message with the user's private key and save the signature to the database
message = 'hello world'
signature = sign_message(public_key, message)
print(signature)
# Create a web token for the user and save it to the database
web_token = create_web_token(public_key)
print(web_token)

# Close the database connection
# fetch from DB
cursor = db.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

db.close()

