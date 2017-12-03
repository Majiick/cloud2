DockerCMS ReadME, Zan Smirnov C15437072

Video: https://youtu.be/FvkVLIfCFgc

#Setup:#
1. First build the image with `docker build -t cloud2 .`

2. Then run it.
docker run -d -v ~/cloud2/myapp:/main -p 80:8080 --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock --name cloud2 cloud2
The socket --mount is to be able to run commands on the VM, the -v command is so we can update the python file without rebuilding whole image.


#Q1 1.#
![alt text](https://github.com/Majiick/cloud2/blob/master/4de7906be4499e730e9b9b0bd437fedf.png "Logo Title Text 1")

#Q1 2.#
The endpoints are as described in the assignment pdf.

The code is in main.py and I test it in the video.


#Q2 1.#
![alt text](https://github.com/Majiick/cloud2/blob/master/4de7906be4499e730e9b9b0bd437fedf.png "Logo Title Text 1")

#Q2 2.#
The tests are in tests.sh