from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)