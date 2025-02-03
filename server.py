from flask import Flask, request, redirect, url_for, render_template, session
import bcrypt

app = Flask(__name__)

# für die Session wird ein Secret Key benötigt (damit wird der Cookie verschlüsselt)
app.secret_key = 'li4QuX00quwiX1yA'

# einfaches Beispiel - normalerweise wird das Passwort nicht im Klartext gespeichert
users = {
    "user@example.org": b'$2b$12$ZK4eGD1EzNJwkNkmDjcpcucVVdZfCQqhIgHDanG9g9Pykqc8mILDm'  # 12345
}

# Zum Hashen von Passwörtern
# password = bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt())
# print(password)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Ein Post-Request bedeutet, dass das Formular abgesendet wurde
    if request.method == 'POST':
        # Formulardaten auslesen
        email = request.form['email']
        password = request.form['password']

        # Passwort überprüfen mit Hashing (bcrypt überprüft das Passwort mit dem Hash)
        if bcrypt.checkpw(password.encode('utf-8'), users[email]):
            # den eingeloggten User in der Session speichern
            session['user'] = email

            # Weiterleitung auf die geschützte Seite
            return redirect(url_for('userarea'))
        else:
            # Fehlermeldung anzeigen, Login-Formular erneut anzeigen
            return render_template('login.html', message="Falsche E-Mail oder Passwort")

        # Passwort überprüfen, zunächst ohne Verschlüsselung
        # if email in users and users[email] == password:
        #     # den eingeloggten User in der Session speichern
        #     session['user'] = email
        #     return redirect(url_for('userarea'))
        # else:
        #     return render_template('login.html', message="Falsche E-Mail oder Passwort")
    else:
        # Formular anzeigen bei einem Get-Request
        return render_template('login.html')
    

@app.route('/logout')
def logout():
    # Session löschen beim Logout
    session.pop('user', None)

    # Weiterleitung auf die Loginseite
    return redirect(url_for('login'))

@app.route('/userarea')
def userarea():
    # Geschützte Seite, nur erreichbar wenn der User in der Session gespeichert ist
    if 'user' in session:
        # User ist eingeloggt ... darf die Seite sehen
        return render_template('userarea.html', user=session['user'])
    else:
        # User ist nicht eingeloggt ... Weiterleitung auf die Loginseite
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
