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
Add random values on creation aka magic number
"""
def create_token(uid, username, privilege):
	token = jwt.encode({"uid": uid, "username": username, "privilege": privilege}, jwt_config[0], algorithm=jwt_config[1])
	encrypt = cipher.encrypt((iv + bytes(token)))
	return base64.b64encode(encrypt)

def decrypt_token(encrypt):
	return cipher.decrypt(base64.b64decode(encrypt))[len(iv):]

def decode_token(encode):
	decrypt = decrypt_token(encode)
	return jwt.decode(decrypt, jwt_config[0], algorithm=[jwt_config[1]])

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

def decode_userdata(encode):
	decrypted_token = decrypt_token(encode)
	decode = jwt.decode(decrypted_token, jwt_config[0], algorithm=[jwt_config[1]])
	return {"username": decode["username"], "uid": decode["uid"]}

"""
0: Any level
1: User level privilege
2: Admin level privilege
"""
def authorize_action(torn, priv_level = 1):
	encoded_token = torn.request.headers["Authorization"] if "Authorization" in torn.request.headers else ""

	if determine_privilege(encoded_token) < priv_level:
		torn.write({"message":"Authorization failed"})
		torn.add_header("Authorization", "")
		return None

	return decode_token(encoded_token)