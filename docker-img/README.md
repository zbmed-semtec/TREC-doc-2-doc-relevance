# Docker Image

Prerequisites: 
- Docker installed and daemon is running. You can test this by entering `docker version` into your terminal.
- This repository cloned with `git clone https://github.com/zbmed-semtec/TREC-doc-2-doc-relevance/tree/web-app`

If the daemon is running enter the following into your console:
1. Go to the app folder `cd TREC-doc-2-doc-relevance/app`
2. Create the image with `docker build -t app`
3. Run the image in "test" container with: `docker run -p 5001:5000 --name test app`
4. Visit `http://127.0.0.1:5001` in your browser and the app should run.