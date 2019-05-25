from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL



app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'url_short'

@app.route('/')
def index():
    return render_template('index.html')


def short_url(cursor,conn,url,code):
    cursor.execute(f'insert into urls (url, codurl) values("{url}",{code})')
    conn.commit()

def get_url(cursor):
    cursor.execute('SELECT url FROM urls')

    urlss = cursor.fetchall()

    return urlss



@app.route('/short_url', methods=['post'])
def short():
    if request.method == 'POST':
        url = request.form['url']
        code = request.form['code']
        conn = mysql.connect()
        cursor = conn.cursor()

        short_url(cursor,conn,url,code)

        cursor.close()
        conn.close()

        return redirect(code)
    else:
        return index()


@app.route('/access')
def acesso():
    conn = mysql.connect()
    cursor = conn.cursor()

    urlx = get_url(cursor)

    cursor.close()
    conn.close()

    return render_template('/listar.html', urlx=urlx)


if __name__ == '__main__':
    app.run(debug= True)