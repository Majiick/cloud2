curl -s -X GET -H 'Accept: application/json' http://localhost:5000/containers
curl -s -X GET -H 'Accept: application/json' http://localhost:5000/containers?state=running
curl -s -X GET -H 'Accept: application/json' http://localhost:5000/containers/testcontainerid
curl -s -X GET -H 'Accept: application/json' http://localhost:5000/containers/testcontainerid/logs
curl -s -X GET -H 'Accept: application/json' http://localhost:5000/services
curl -s -X GET -H 'Accept: application/json' http://localhost:5000/nodes
curl -s -X GET -H 'Accept: application/json' http://localhost:5000/images
curl -s -X POST -H 'Accept: application/json' http://localhost:5000/containers?image=hello-world
curl -s -X DELETE -H 'Accept: application/json' http://localhost:5000/containers/testcontainerid
curl -s -X DELETE -H 'Accept: application/json' http://localhost:5000/containers
curl -s -X DELETE -H 'Accept: application/json' http://localhost:5000/images
curl -X PATCH http://localhost:8080/containers/testcontainerid?action=start
curl -s -X PATCH http://localhost:8080/images/testimageid?tag=testimagetag