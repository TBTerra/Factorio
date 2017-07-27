import zlib
import base64
import json
import sys

def decode_blueprint(bp_string):
	return json.loads(str(zlib.decompress(base64.b64decode(bp_string[1:]), wbits=0),'utf-8'))

def encode_blueprint(bp_json_obj):
	return "0" + str(base64.b64encode(zlib.compress(json.dumps(bp_json_obj,separators=(',', ':')).encode('utf-8'),9)),'utf-8')

newX = [-3,-2, 0, 2,3,2,0,-2]
newY = [ 0,-2,-3,-2,0,2,3, 2]
flipDirC = [1,0,7,6,5,4,3,2]
flipDirR = [0,7,2,5,4,3,6,1]
flipDirS = [0,7,6,5,4,3,2,1]

with open(sys.argv[1]) as file:
	bpsI = file.read()

dict = decode_blueprint(bpsI)
for entity in dict['blueprint']['entities']:
	#swap x
	entity['position']['x'] = -entity['position']['x']
	if (entity['name'] == 'curved-rail'):
		if 'direction' not in entity:
			entity['direction'] = 0
		entity['direction'] = flipDirC[entity['direction']]
	if (entity['name'] == 'straight-rail'):
		if 'direction' not in entity:
			entity['direction'] = 0
		entity['direction'] = flipDirR[entity['direction']]
	if (entity['name'] == 'rail-signal') or (entity['name'] == 'rail-chain-signal'):
		if 'direction' not in entity:
			entity['direction'] = 0
		entity['direction'] = flipDirS[entity['direction']]
		entity['position']['x'] = entity['position']['x'] + newX[entity['direction']]
		entity['position']['y'] = entity['position']['y'] + newY[entity['direction']]

bpsO = encode_blueprint(dict)

with open(sys.argv[2],'w') as file:
	file.write(bpsO);