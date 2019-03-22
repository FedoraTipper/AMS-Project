import handlers.config as confighandler
import jwt
from Crypto.Cipher import AES
from Crypto import Random
import base64

jwt_config = confighandler.get_keys("JWT")
hash_config = confighandler.get_keys("PBKDF2")
iv = Random.new().read(16)
cipher = AES.new(hash_config[0], AES.MODE_CFB, iv)

def create_token(uid, username, privilege):
	"""
	Function to create a JWT token that is encrypted with AES
	Inputs: User_ID; username; privilege
	Output: base 64 encoded and encrypted token
	Caveats: None
	"""
	token = jwt.encode({"uid": uid, "username": username, "privilege": privilege}, jwt_config[0], algorithm=jwt_config[1])
	encrypt = cipher.encrypt((iv + bytes(token)))
	return base64.b64encode(encrypt)

def decrypt_token(encrypt):
	"""
	Function to decrypt any string or token
	Inputs: encrypted base 64 encoded token
	Output: "plaintext" JWT token
	Caveats: None
	"""
	return cipher.decrypt(base64.b64decode(encrypt))[len(iv):]

def decode_token(encode):
	"""
	Function to decode and validate a JWT token
	Inputs: Encoded token from user
	Output: Decoded JWT token
	Caveats: None
	"""
	decrypt = decrypt_token(encode)
	return jwt.decode(decrypt, jwt_config[0], algorithm=[jwt_config[1]])

def determine_privilege(encode):
	"""
	Function to determine user privilege from token
	Inputs: Encoded token from user
	Output: int formatted privilege level
	Caveats: None
	"""
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

def decode_userdata(encode):
	"""
	Function to return user data stored within a JWT token
	Inputs: Encoded token from user
	Output: Dictionary of user data within a JWT token
	Caveats: None
	"""
	decrypted_token = decrypt_token(encode)
	decode = jwt.decode(decrypted_token, jwt_config[0], algorithm=[jwt_config[1]])
	return {"username": decode["username"], "uid": decode["uid"]}

def authorize_action(torn, priv_level):
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
	encoded_token = torn.request.headers["Authorization"] if "Authorization" in torn.request.headers else ""

	if determine_privilege(encoded_token) < priv_level:
		torn.set_status(401)
		torn.write({"message":"Authorization failed"})
		torn.add_header("Authorization", "")
		return False

	return decode_token(encoded_token)