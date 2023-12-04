from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('page2', name=name))
    return render_template('test.html')

@app.route('/page2/<name>')
def page2(name):
    return f'HELLO {name}!'

if __name__ == '__main__':
    app.run(debug=True)
