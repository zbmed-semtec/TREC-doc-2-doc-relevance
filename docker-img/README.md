# Docker Image

Prerequisites: 
- Docker installed and daemon is running. You can test this by entering `docker version` into your terminal.
- This repository cloned with `git clone https://github.com/zbmed-semtec/TREC-doc-2-doc-relevance/tree/web-app`

If the daemon is running enter the following into your console:
1. Go to the app folder `cd TREC-doc-2-doc-relevance/app`
2. Create the image with `docker build -t app .`
3. Run the image in "test" container with: `docker run -d -p 5001:5000 --name test app`
4. Visit `http://127.0.0.1:5001` in your browser and the app should run.

To copy the database from the container, follow the given steps:
1. Go the directory in the host machine where the database file is to be copied.
2. Open the command terminal in the given directory.
3. For the container name "test", insert the given command `docker cp test:/app/db.sqlite .`
