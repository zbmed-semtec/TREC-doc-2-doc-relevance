# Docker Image

Skills you would need before using this repo as a docker image
- Basic knowledge on docker as a user, i.e., you do not need to know how to create images but how to build and use an instance. [More information about docker](https://docs.docker.com/)
- Basic knowledge on Git or a desktop client version, e.g., [GitHub desktop](https://desktop.github.com/)

Before you start:
- This repository should be already cloned and locally available in your computer
  - You can clone it via command line `git clone https://github.com/zbmed-semtec/TREC-doc-2-doc-relevance`
  - You can also use the [GitHub desktop](https://desktop.github.com/)
- Docker should be installed and running. If you do not have docker already, you will need [to dowload it](https://docs.docker.com/get-docker/) and install it
  - You can test docker is up and running by entering `docker version` into your terminal. You should get a response like
```
Client:
 Cloud integration: v1.0.22
 Version:           20.10.12
 API version:       1.41
 Go version:        go1.16.12
 Git commit:        e91ed57
 Built:             Mon Dec 13 11:44:07 2021
 OS/Arch:           windows/amd64
 Context:           default
 Experimental:      true

Server: Docker Desktop 4.5.1 (74721)
 Engine:
  Version:          20.10.12
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.16.12
  Git commit:       459d0df
  Built:            Mon Dec 13 11:43:56 2021
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.4.12
  GitCommit:        7b11cfaabd73bb80907dd23182b9347b4245eb5d
 runc:
  Version:          1.0.2
  GitCommit:        v1.0.2-0-g52b36a2
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
  ```

Building the instance
You will need to do this only once. If docker is up and running enter the following into your console:
1. Go to the app folder `cd TREC-doc-2-doc-relevance/app`
2. Create the image with `docker build -t app .`
3. Run the image in "test" container with: `docker run -d -p 5001:5000 --name test app`
4. Visit `http://127.0.0.1:5001` in your browser and the app should run.

To copy the database from the container, follow the given steps:
1. Go the directory in the host machine where the database file is to be copied.
2. Open the command terminal in the given directory.
3. For the container name "test", insert the given command `docker cp test:/app/db.sqlite .`

Using the instance
If you already created the instance you can use it at any time
1. Start the instance using ```docker start test``` (you do not need to do this if you just created the instance, see above, as it will be running already)
2. Visit `http://127.0.0.1:5001` in your browser and add your relevance assessments
3. Once you are done, remeber to get a copy/backup of the database `docker cp test:/app/db.sqlite .` (we suggest you do this outside the repo folder so you do not overwrite the initial database)
4. Stop the instance using ```docker stop test```
