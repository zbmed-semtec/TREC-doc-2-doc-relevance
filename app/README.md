# ZB MED Article Evaluation App

To try the app locally on your computer:
- Open up a terminal window.
- Clone the repository with `git clone https://github.com/zbmed-semtec/TREC-doc-2-doc-relevance/tree/web-app`
- Go to the `TREC-doc-2-doc-relevance` folder and open the terminal.
- Type:
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
Output:
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```
- Visit `http://127.0.0.1:5000/` in your browser of choice (Firefox, Chrome, Edge, Safari) and the app should be up and running.

To enable the virtual environment:
- Go to the `app` folder.
- Type in the terminal `. venv/bin/activate`

To install setup.py:
- Go to the `TREC-doc-2-doc-relevance` folder
- Type in the terminal `pip install -e .` to install setup.py which will solve the problem of relative paths.
