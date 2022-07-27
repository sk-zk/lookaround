import base64
from Crypto.Cipher import AES
import hashlib
import random
import requests
import string
import time
from urllib.parse import urlparse, quote

import ResourceManifest_pb2


class Authenticator:
    TOKEN_P1 = "4cjLaD4jGRwlQ9U"
    MANIFEST_URL = "https://gspe35-ssl.ls.apple.com/geo_manifest/dynamic/config?application=geod" \
                   "&application_version=1&country_code=US&hardware=MacBookPro11,2&os=osx" \
                   "&os_build=20B29&os_version=11.0.1"

    def __init__(self):
        self.token_p2 = None
        self.resource_manifest = None
        self.session_id = None
        self.refresh_credentials()

    def refresh_credentials(self):
        self.session_id = _generate_session_id()
        self.resource_manifest = self._get_resource_manifest()
        self.token_p2 = self.resource_manifest.token_p2

    def authenticate_url(self, url):
        url_obj = urlparse(url)

        token_p3 = _generate_token_p3()
        token = self.TOKEN_P1 + self.token_p2 + token_p3
        timestamp = int(time.time()) + 4200
        separator = "&" if url_obj.query else "?"

        plaintext = f"{url_obj.path + url_obj.query}{separator}sid={self.session_id}{timestamp}{token_p3}"
        plaintext_bytes = _pad_pkcs7(plaintext.encode("utf-8"))
        key = hashlib.sha256(token.encode()).digest()
        iv = b"\0" * 16
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(plaintext_bytes)
        ciphertext_b64 = base64.b64encode(ciphertext).decode()
        ciphertext_url = quote(ciphertext_b64, safe="")
        access_key = f"{timestamp}_{token_p3}_{ciphertext_url}"
        final = f"{url}{separator}sid={self.session_id}&accessKey={access_key}"
        return final

    def _get_resource_manifest(self):
        response = requests.get(self.MANIFEST_URL)
        manifest = ResourceManifest_pb2.ResourceManifest()
        manifest.ParseFromString(response.content)
        return manifest


def _generate_session_id():
    return ''.join(random.choices(string.digits, k=40))


def _generate_token_p3():
    return ''.join(random.choices(string.digits + string.ascii_lowercase + string.ascii_uppercase, k=16))


def _pad_pkcs7(data, block_size=16):
    # via https://stackoverflow.com/a/70344303
    # CC BY-SA 4.0
    if type(data) != bytearray and type(data) != bytes:
        raise TypeError()
    pl = block_size - (len(data) % block_size)
    return data + bytearray([pl for i in range(pl)])