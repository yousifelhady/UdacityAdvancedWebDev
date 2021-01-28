import sys
import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'yousifelhady.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImR1SWtESmhMSGtpMFRlTDhydG1jRyJ9.eyJpc3MiOiJodHRwczovL3lvdXNpZmVsaGFkeS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM5NTQ2NjE1ODU5MjA2ODgxNTQiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYxMTg0MTcwNSwiZXhwIjoxNjExODQ4OTA1LCJhenAiOiI5MEFZd0NJenptMlN6aFRKYUpKdHdxMmJoNmNGZlpjaiIsInNjb3BlIjoiIn0.IHUK0f3J-VVECzxFFHViEUrf4noMuYCg6LKLGPGilpYuikiLW3JPRYnu0VvtZHIXNp1pDLHQpO8HmcyUTHLhvlZgGbs-cqmtd4ItCbgMXILgyNdUREhPo4KPCJINCsmCIK4f3q3dFG5QYU6gmRGY3syBDG6HHMbK49DJwIcQ5lfBjvuJVXRNGvWegAIDB-y9FwUuyLN8fxuTJQR1M-gYuinNX_MDet9_zPQBjLL-tEhpBOjncGnRJNMET2q-bHxiq5mheExTTvpkdfqXmirxo4ZQzlXyf_ycIJ36XjA4qRHhKp2ZMV5-MYDDiY5leo3oF_PPEZ_5acscSBtMf72DSg'

    def verify_decode_jwt(token):
        # GET THE PUBLIC KEY FROM AUTH0
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        
        # GET THE DATA IN THE HEADER
        unverified_header = jwt.get_unverified_header(token)
        
        # CHOOSE OUR KEY
        rsa_key = {}
        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                # USE THE KEY TO VALIDATE THE JWT
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )

                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
        raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to find the appropriate key.'
                }, 400)
    print(verify_decode_jwt(token))