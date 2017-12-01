from flask import Flask, Response, render_template, request
import json
import subprocess


app = Flask(__name__)


def json_error(err: str):
    return json.dumps({'error': err})


@app.route('/containers', methods=['GET'])
def containers_index():
    """
    List all containers

    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool
    """
    def parse_docker_ps(output):
        ret = []
        for c in [line.split() for line in output.splitlines()[1:]]:
            each = dict()
            each['id'] = c[0]
            each['image'] = c[1]
            each['name'] = c[-1]
            each['ports'] = c[-2]
            ret.append(each)

        return ret

    try:
        if request.args.get('state') == 'running':
            output = docker('ps')
            resp = json.dumps(parse_docker_ps(output))
        else:
            output = docker('ps', '-a')
            resp = json.dumps(parse_docker_ps(output))
    except subprocess.CalledProcessError as e:
        return json_error(str(e))

    return Response(response=resp, mimetype="application/json")


@app.route('/containers/<id_>', methods=['GET'])
def containers_specific(id_):
    output = docker('inspect', str(id_))
    resp = output

    return Response(response=resp, mimetype="application/json")


@app.route('/containers/<id_>/logs', methods=['GET'])
def containers_specific_logs(id_):
    output = docker('logs', str(id_))
    resp = output

    return Response(response=resp, mimetype="application/json")


@app.route('/services', methods=['GET'])
def services():
    output = docker('service' 'ps')
    resp = output

    return Response(response=resp, mimetype="application/json")


@app.route('/nodes', methods=['GET'])
def nodes():
    output = docker('node' 'ls')
    resp = output

    return Response(response=resp, mimetype="application/json")


@app.route('/containers', methods=['POST'])
def containers_create():
    # Create a container with ?image=<imagename>
    output = docker('container', 'create', str(request.args.get('image')))
    resp = output

    return Response(response=resp, mimetype="application/json")


'''
@app.route('/containers/<id_>', methods=['PATCH'])
def containers_patch():
    output = docker('create' 'hello-world')
    resp = output

    return Response(response=resp, mimetype="application/json")
'''


@app.route('/containers/<id_>', methods=['DELETE'])
def containers_delete_id(id_):
    output = docker('rm', str(id_))
    resp = output

    return Response(response=resp, mimetype="application/json")


@app.route('/images', methods=['GET'])
def images_get():
    output = docker('image', 'ls')
    resp = output

    return Response(response=resp, mimetype="application/json")


@app.route('/containers', methods=['DELETE'])
def containers_delete():
    output = docker('rm', '$(docker ps -a -q)')
    resp = output

    return Response(response=resp, mimetype="application/json")


@app.route('/images', methods=['DELETE'])
def images_delete():
    resp = docker('rmi', '$(docker images -q)')

    return Response(response=resp, mimetype="application/json")


@app.route('/images/<id_>', methods=['DELETE'])
def images_delete_id(id_):
    resp = docker('rmi', str(id_))

    return Response(response=resp, mimetype="application/json")


def docker(*args):
    print("Running: {}".format(['docker'] + list(args)))
    try:
        completed_process = subprocess.run(' '.join(['docker'] + list(args)), shell=True, check=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(e)
        raise

    return completed_process.stdout


if __name__ == '__main__':
    app.run()