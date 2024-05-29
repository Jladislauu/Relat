from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/relat_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Verifica se o diretório 'static' existe, caso contrário, cria-o
if not os.path.exists('static'):
    os.makedirs('static')

# Definição dos modelos de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(500))
    filename = db.Column(db.String(120), nullable=False)

# Rota inicial e de login
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return redirect(url_for('report'))
    else:
        error = 'Usuário ou senha incorretos.'
        return render_template('login.html', error=error)

# Rota para a página de relatório
@app.route('/report')
def report():
    return render_template('report.html')

# Rota para gerar relatório
@app.route('/generate_report', methods=['POST'])
def generate_report():
    client = request.form['client']
    service = request.form['service']
    date = request.form['date']
    description = request.form.get('description', 'N/A')

    if not client or not service or not date:
        flash('Preencha todos os campos obrigatórios.', 'error')
        return redirect(url_for('relatorios'))

    # Garante que o nome do arquivo PDF seja válido
    pdf_filename = f"relatorio_{client.replace(' ', '_')}_{date.replace('/', '-')}.pdf"
    pdf_file = os.path.join('static', pdf_filename)
    
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.drawString(100, 750, f"Cliente: {client}")
    c.drawString(100, 735, f"Serviço Realizado: {service}")
    c.drawString(100, 720, f"Data: {date}")
    c.drawString(100, 705, f"Descrição: {description}")
    c.showPage()
    c.save()

    # Salvar relatório no banco de dados
    new_report = Report(client=client, service=service, date=date, description=description, filename=pdf_filename)
    db.session.add(new_report)
    db.session.commit()

    message = f"Relatório {pdf_filename} gerado com sucesso!"
    pdf_link = url_for('static', filename=pdf_filename)
    return render_template('report.html', message=message, pdf_link=pdf_link)

# Rota para exibir os relatórios
@app.route('/relatorios')
def relatorios():
    reports = Report.query.all()
    return render_template('relatorios.html', reports=reports)



# Rota para visualizar o PDF
@app.route('/visualizar_relatorio/<filename>')
def visualizar_relatorio(filename):
    # Você precisa definir o diretório onde os PDFs são armazenados
    # Aqui estamos assumindo que eles estão no diretório 'static'
    pdf_directory = os.path.join(app.root_path, 'static')
    return send_from_directory(pdf_directory, filename)

# Rota para visualizar o último relatório gerado
@app.route('/visualizar_ultimo_relatorio')
def visualizar_ultimo_relatorio():
    # Recupera o último relatório da base de dados
    last_report = Report.query.order_by(Report.id.desc()).first()
    if last_report:
        return redirect(url_for('visualizar_relatorio', filename=last_report.filename))
    else:
        flash('Nenhum relatório foi gerado ainda.', 'error')
        return redirect(url_for('report'))


# Rota para listar todos os relatórios emitidos
@app.route('/listar_relatorios')
def listar_relatorios():
    reports = Report.query.all()
    return render_template('relatorios.html', reports=reports)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
        
        # Adiciona um usuário de teste
        if not User.query.filter_by(username='admin').first():
            new_user = User(username='admin', password='admin123')
            db.session.add(new_user)
            db.session.commit()
            
    app.run(debug=True)
