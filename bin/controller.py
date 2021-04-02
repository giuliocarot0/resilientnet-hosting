from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
ip_whitelist = ['172.22.0.253']

@app.route('/hello/', methods=['GET'])
def welcome():
	return jsonify({'nodeName':'it-ub0-hostingnode0',
			'address' :'172.21.0.45',
			'server'  :'nginx',
			'agent_version':'hostingcontroller-0.1a',
			'message' :'nice to meet you, I\'\m node 0'})


@app.route('/insert/', methods=['PUT'])
def insert():
	new_host = request.form.get('hostname')
	issuer = request.form.get('issuer')
	secret = request.form.get('secret')
	auth = request.headers.get('authorization')
	add = 256
	if ip_valid:
		add = subprocess.call('./create_vhost %s %s %s' % (str(new_host), str(issuer), str(secret)), shell=True)
	if add == 256:
		return "",400
	return  jsonify ({'resp_code':add,
			  'issuedby': issuer,
			  'hostname':new_host})


@app.route('/delete/', methods=['DELETE'])
def delete():
	host=request.form.get('hostname')
	issuer=request.form.get('issuer')
	auth=request.headers.get('authorization')
	if not ip_valid:
		return "", 403
	ret= subprocess.call('./delete_vhost %s' % (str(host)), shell=True)
	if ret==0:
		return jsonify ({'resp_code':ret,
                          'issuedby': issuer,
                          'hostname':host})
	else:
		return "", 404

def ip_valid():
	client=request.remote_addr
	if client in ip_whitelist:
		return True
	else:
		return False



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3434)
