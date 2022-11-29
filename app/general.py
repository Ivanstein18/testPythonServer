from .secret_key import SECRET_KEY
import hmac, hashlib, base64


def sign_data(data):
    sign_data = hmac.new(key= SECRET_KEY.encode(), msg= data.encode(), digestmod= hashlib.sha256).hexdigest().upper()
    return sign_data

def data_b64_encode(data):
    code = (base64.b64encode(data.encode())).decode()
    return code

def data_b64_decode(data_b64_encode):
    decode = (base64.b64decode(data_b64_encode.encode())).decode()
    return decode

def check_valid_sign_data(usernameS):
    print(usernameS)
    usernameB64, sign = usernameS.split(".")#?????????????????????????????????????????????
    username = data_b64_decode(usernameB64)
    check = hmac.compare_digest(sign, sign_data(username))
    if check:
        return True
    else:
        return False

def username_from_usernameS(usernameS):
    usernameB64, sign = usernameS.split()
    username = data_b64_decode(usernameB64)
    return username

def sign_cookie(username):
    sign_cookie = f"{data_b64_encode(username)}.{sign_data(username)}"
    return sign_cookie