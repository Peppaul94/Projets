import validators
from urllib.parse import urlparse

result = urlparse("http://35.175.136.38/login")
if result.scheme and result.netloc:
    print("Success")
else:
    print("Failed")

print(result)