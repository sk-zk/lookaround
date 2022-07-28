from auth import Authenticator

auth = Authenticator()
url = auth.authenticate_url("https://gspe19-ssl.ls.apple.com/tile.vf?style=64&size=2&scale=0&v=14030365&z=12&x=2155&y=1300&vlang=en&preflight=2")
print(url)
