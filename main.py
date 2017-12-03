from flask import Flask, Response, render_template, request
import json
import subprocess


app = Flask(__name__)


def json_error(err: str):
    return json.dumps({'error': err})


# Works
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
        return json_error(str(e) + ' ' + str(e.output))

    return Response(response=resp, mimetype="application/json")


# Works
@app.route('/containers/<id_>', methods=['GET'])
def containers_specific(id_):
    output = docker('inspect', str(id_))
    resp = output

    return Response(response=resp, mimetype="application/json")


# Works
@app.route('/containers/<id_>/logs', methods=['GET'])
def containers_specific_logs(id_):
    try:
        output = docker('logs', str(id_))
    except subprocess.CalledProcessError as e:
        return json_error(str(e) + ' ' + str(e.output))

    resp = json.dumps({'result': output})

    return Response(response=resp, mimetype="application/json")


# Works
@app.route('/services', methods=['GET'])
def services():
    def parse_docker_service_ls(output):
        ret = []
        for c in [line.split() for line in output.splitlines()[1:]]:
            each = dict()
            each['id'] = c[0]
            each['name'] = c[1]
            each['mode'] = c[2]
            each['replicas'] = c[3]
            each['image'] = c[4]
            each['ports'] = c[5]
            ret.append(each)

        return ret

    try:
        output = docker('service', 'ls')
    except subprocess.CalledProcessError as e:
        return json_error(str(e) + ' ' + str(e.output))

    resp = json.dumps(parse_docker_service_ls(output))

    return Response(response=resp, mimetype="application/json")


# Works
@app.route('/nodes', methods=['GET'])
def nodes():
    def parse_docker_node_ls(output):
        ret = []
        for c in [line.split() for line in output.splitlines()[1:]]:
            each = dict()
            each['id'] = c[0]
            each['hostname'] = c[1]
            each['status'] = c[2]
            each['availability'] = c[3]
            ret.append(each)

        return ret

    try:
        output = docker('node', 'ls')
    except subprocess.CalledProcessError as e:
        return json_error(str(e) + ' ' + str(e.output))

    resp = json.dumps(parse_docker_node_ls(output))

    return Response(response=resp, mimetype="application/json")


# Works
@app.route('/containers', methods=['POST'])
def containers_create():
    # Create a container with ?image=<imagename>
    try:
        output = docker('container', 'create', str(request.args.get('image')))
    except subprocess.CalledProcessError as e:
        return json_error(str(e) + ' ' + str(e.output))

    resp = json.dumps({'success': 'true', 'message': output})

    return Response(response=resp, mimetype="application/json")


'''
@app.route('/containers/<id_>', methods=['PATCH'])
def containers_patch():
    output = docker('create' 'hello-world')
    resp = output

    return Response(response=resp, mimetype="application/json")
'''


# Works
@app.route('/containers/<id_>', methods=['DELETE'])
def containers_delete_id(id_):
    try:
        output = docker('rm', str(id_))
    except subprocess.CalledProcessError as e:
        return json_error(str(e) + ' ' + str(e.output))

    resp = json.dumps({'success': 'true', 'message': output})

    return Response(response=resp, mimetype="application/json")


# Works
@app.route('/images', methods=['GET'])
def images_get():
    def docker_images_to_array(output):
        ret = []
        for c in [line.split() for line in output.splitlines()[1:]]:
            each = dict()
            each['id'] = c[2]
            each['tag'] = c[1]
            each['name'] = c[0]
            ret.append(each)

        return ret

    try:
        output = docker('image', 'ls')
    except subprocess.CalledProcessError as e:
        return json_error(str(e) + ' ' + str(e.output))

    resp = json.dumps(docker_images_to_array(output))

    return Response(response=resp, mimetype="application/json")


@app.route('/containers', methods=['DELETE'])
def containers_delete():
    try:
        output = docker('rm', '$(docker ps -a -q)')
    except subprocess.CalledProcessError as e:
        return json_error(str(e) + ' ' + str(e.output))

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
    print("Running: {}".format(' '.join((['docker'] + list(args)))))
    try:
        completed_process = subprocess.run(' '.join((['docker'] + list(args))), shell=True, check=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(e)
        raise

    return completed_process.stdout.decode(encoding='UTF-8')


if __name__ == '__main__':
    app.run()