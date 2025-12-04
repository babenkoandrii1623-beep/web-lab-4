import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "Перейдіть на <a href='/form'>/form</a>"

@app.route('/form', methods=['GET', 'POST'])
def form_handler():
    errors = {}
    data = {}

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age', '').strip()
        group = request.form.get('group', '').strip()

        data = {'name': name, 'email': email, 'age': age, 'group': group}

        if not name:
            errors['name'] = "Поле 'Ім'я' не може бути порожнім"
        
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not email:
            errors['email'] = "Поле 'Email' не може бути порожнім"
        elif not re.match(email_pattern, email):
            errors['email'] = "Некоректний формат Email"

        if not age:
            errors['age'] = "Поле 'Вік' не може бути порожнім"
        elif not age.isdigit():
            errors['age'] = "Вік має бути цілим числом"

        if not group:
            errors['group'] = "Поле 'Група' не може бути порожнім"

        if errors:
            return render_template('form.html', errors=errors, data=data)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"submission_{timestamp}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Ім'я: {name}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Вік: {age}\n")
                f.write(f"Група: {group}\n")
                f.write(f"Час створення: {timestamp}\n")
        except Exception as e:
            print(f"Помилка запису файлу: {e}")

        return redirect(url_for('result_handler', 
                                name=name, 
                                email=email, 
                                age=age, 
                                group=group,
                                saved_file=filename))

    return render_template('form.html', data={})

@app.route('/result')
def result_handler():
    name = request.args.get('name')
    email = request.args.get('email')
    age = request.args.get('age')
    group = request.args.get('group')
    saved_file = request.args.get('saved_file')

    return render_template('result.html', 
                           name=name, 
                           email=email, 
                           age=age, 
                           group=group,
                           saved_file=saved_file)

if __name__ == '__main__':
    app.run(debug=True, port=5000)