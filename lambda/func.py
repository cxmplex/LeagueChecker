import os
import urllib.request
os.chdir("/tmp")


def lambda_handler(event, context):
    if event['site'] == "LOLNA":
        response = check_account(event['user_name'], event['password'])
        return {
            'message': response
        }


def check_account(user, password):
    url = 'https://auth.riotgames.com/token'
    data = 'client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer&client_assertion=eyJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJodHRwczpcL1wvYXV0aC5yaW90Z2FtZXMuY29t' \
           'XC90b2tlbiIsInN1YiI6ImxvbCIsImlzcyI6ImxvbCIsImV4cCI6MTU0MDM4NzM3MCwiaWF0IjoxNTI0NjA4OTEyLCJqdGkiOiI0YzY1MGQ0MC1kMWFmLTQyNGQtOTg0ZS02ODE2Y2E3MDE4NDgifQ.I32fKF4m0NTDlcZdp2972i2y' \
            'PR1WpmD9zVMBChQGqMBU0No1zpHUvjxT2RlHQC6PwUKsWjARw9O_TF0Q2PY_73SsCgm7q62lrS9estEbUNByIXKOgk3WG-hzQv2OmfZ4u8KBAWLpZ34hJfkbkHdHIPVPPkYhWFWkRo6DEDskqFEnETkmNUcBBpuDyiF_9OhvrH6Mfu20' \
             'MDgIqY3__zzM4oM8Xh5LpWFnNGbczrOuyOlD17yop9nKMG5C2pw62' \
             "eBrYarP1bftz39lozMrW7tnOcnSkRfNGyA3bvyga0qZQpOmebmo_vaqQo3Mj-Czi1EMXv1tPInu-rxdDZ2P5nwgig&grant_type=password&username=NA1%7C{}&password={}&scope=openid".format(user, password)
    req = urllib.request.Request(
        url,
        data=data.encode('ascii'),
        headers={
            'User-Agent': 'RiotClient/17.1.0 (rso-auth)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '/'
        }
    )
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')