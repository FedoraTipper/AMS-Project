import handlers.config as ConfigHandler
import jwt
from Crypto.Cipher import AES
from Crypto import Random
import base64

jwt_config = ConfigHandler.get_keys("JWT")
hash_config = ConfigHandler.get_keys("PBKDF2")
iv = Random.new().read(16)
cipher = AES.new(hash_config[0], AES.MODE_CFB, iv)

"""
Function to create a JWT token that is encrypted with AES
Inputs: User_ID; username; privilege
Output: base 64 encoded and encrypted token
Caveats: None
"""
def create_token(uid, username, privilege):
	token = jwt.encode({"uid": uid, "username": username, "privilege": privilege}, jwt_config[0], algorithm=jwt_config[1])
	encrypt = cipher.encrypt((iv + bytes(token)))
	return base64.b64encode(encrypt)

"""
Function to decrypt any string or token
Inputs: encrypted base 64 encoded token
Output: "plaintext" JWT token
Caveats: None
"""
def decrypt_token(encrypt):
	return cipher.decrypt(base64.b64decode(encrypt))[len(iv):]

"""
Function to decode and validate a JWT token
Inputs: Encoded token from user
Output: Decoded JWT token
Caveats: None
"""
def decode_token(encode):
	decrypt = decrypt_token(encode)
	return jwt.decode(decrypt, jwt_config[0], algorithm=[jwt_config[1]])

"""
Function to determine user privilege from token
Inputs: Encoded token from user
Output: int formatted privilege level
Caveats: None
"""
def determine_privilege(encode):
	if len(encode) == 0:
		return 0
	#If a token is not available, return a failed authorized response
	try:
		decoded_token = decode_token(encode)
	except:
		return 0
	if "privilege" not in decoded_token:
		return 0
	else:
		return int(decoded_token["privilege"])

"""
Function to return user data stored within a JWT token
Inputs: Encoded token from user
Output: Dictionary of user data within a JWT token
Caveats: None
"""
def decode_userdata(encode):
	decrypted_token = decrypt_token(encode)
	decode = jwt.decode(decrypted_token, jwt_config[0], algorithm=[jwt_config[1]])
	return {"username": decode["username"], "uid": decode["uid"]}

"""
Function to authorise any action that a user requests
Inputs: tornado object to write messages; privilege level that needs to be checked against
Output: None if authorisation failed and message; Or the decoded token
Caveats:
	Privilege levels:
	0: Any level
	1: User level privilege
	2: Admin level privilege
"""
def authorize_action(torn, priv_level):
	encoded_token = torn.request.headers["Authorization"] if "Authorization" in torn.request.headers else ""

	if determine_privilege(encoded_token) < priv_level:
		torn.write({"message":"Authorization failed"})
		torn.add_header("Authorization", "")
		return False

	return decode_token(encoded_token)