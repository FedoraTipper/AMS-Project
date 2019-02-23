import handlers.config as ConfigHandler
import jwt

jwt_config = ConfigHandler.get_keys("JWT")

"""
Add random values on creation aka magic number
"""
def create_token(uid, username, privilege):
	return jwt.encode({"uid": uid, "username": username, "privilege": privilege}, jwt_config[0], algorithm=jwt_config[1])


def decode_token(encode):
	return jwt.decode(encode, jwt_config[0], algorithm=[jwt_config[1]])

def determine_privilege(encode):
	if len(encode) == 0:
		return 0
	decoded_token = decode_token(encode)
	if "privilege" not in decoded_token:
		return 0
	else:
		return int(decoded_token["privilege"])

def authorize_action(torn):
	encoded_token = torn.request.headers["Authorization"] if "Authorization" in torn.request.headers else ""

	if determine_privilege(encoded_token) == 0:
		torn.write({"message":"Authorization failed"})
		torn.add_header("Authorization", "")
		return None

	return decode_token(encoded_token)