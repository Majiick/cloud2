docker service create --detach=true --replicas 3 -p 8000:80 --name nginx nginx