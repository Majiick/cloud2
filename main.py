from flask import Flask, Response, render_template, request
import json
import subprocess


app = Flask(__name__)


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
        return str(e), 403

    return Response(response=resp, mimetype="application/json")





def docker(*args):
    try:
        completed_process = subprocess.run(['docker'].extend(args), shell=True, check=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(e)
        raise

    return completed_process.stdout


if __name__ == '__main__':
    pass