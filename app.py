from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Це домашня сторінка! Спробуйте перейти на /hello/ВашеІм'я"


@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html.j2', name=name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)