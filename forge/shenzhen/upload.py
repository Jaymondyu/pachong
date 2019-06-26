import os, requests, json
from math import ceil
import uuid

def _GetToken(scope):
	url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
	headers = { "Content-Type": "application/x-www-form-urlencoded" }
	body = {
		"client_id" : "OK54AyvODOgdSUmA9ivy04PwmzIZAP3g",
		"client_secret" : "bvbwXbwI7HxO0lQ2",
		"grant_type": "client_credentials",
		"scope": scope
	}
	r = requests.post(url, headers=headers, data=body)
	respose = json.loads(r.text)
	access_token = respose['access_token']
	return access_token


CHUNK = 5
bucketKey = 'plokijuh12345678'
objectName = 'BIG.nwd'
# file to upload
fn = objectName

# URL to resumably upload a file
url = "https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s/resumable" % (bucketKey, objectName)

# file size in bytes
size = os.path.getsize(fn)

# each chunck has a size of 5MB
chunkSize = CHUNK * 1024 * 1024

# compute how many chuncks are needed
num_chunks = int(ceil(1. * size / chunkSize))
# token = "token"
token = _GetToken("data:write data:create")
GUID = str(uuid.uuid1())
f = open(fn, "rb")

for i in range(num_chunks):
	start = i*chunkSize
	end = min((i+1)*chunkSize-1, size-1)
	real_size = end - start + 1

	headers = {
		"Authorization": "Bearer %s" % token,
		"Content-Length": str(int(real_size)),
		"Content-Range": "bytes %d-%d/%d"%(start, end, size),
		"Session-Id": GUID
	}
	data = f.read(chunkSize)

	r = requests.put(url, headers=headers, data=data)
	if r.status_code > 202:
		print r.status_code
		print r.text
	else:
		print r.status_code, "range %d" % (i+1), headers["Content-Range"], "Uploaded"

print "DONE!"
