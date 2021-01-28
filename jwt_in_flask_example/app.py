from flask import Flask, request, abort

def get_token_from_auth_header():
    #make sure that the request has Authorization key and is authorized
    #if not authorized, abort(401) which is "Unauthorized"
    if 'Authorization' not in request.headers:
        abort(401)

    authorization_header = request.headers['Authorization']
    auth_parts = authorization_header.split(' ')

    #make sure that the authorization header contains bearer and token together
    if len(auth_parts) != 2:
        abort(401)
    #make sure that the authorization header is of type 'bearer'
    elif auth_parts[0].lower() != 'bearer':
        abort(401)

    return auth_parts[1]

app = Flask(__name__)

@app.route('/headers')
def headers():
    jwt = get_token_from_auth_header()
    print(jwt)
    return 'not implemented'