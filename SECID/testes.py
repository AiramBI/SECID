from Demos.win32ts_logoff_disconnected import username

from SECID import app, database
from SECID.models import Usuario

with app.app_context():
   database.drop_all() #deleta o banco de dados
   database.create_all() #cria o banco de dados

#with app.app_context():
#    usuario = Usuario(username = "Lira", email = "lira@gmail.com", senha = "123456")
#    usuario2 = Usuario(username = "Joao", email = "joao@gmail.com", senha = "1234567")

# with app.app_context():
#    usuario3 = Usuario(username = "teste", email = "teste@gmail.com", senha = "123456")
#    usuario = Usuario(username="lira", email="lira@gmail.com", senha="123456")
#    usuario2 = Usuario(username = "Joao", email = "joao@gmail.com", senha = "1234567")
#    database.session.add_all([usuario,usuario3,usuario2])
#   database.session.commit()


# with app.app_context():
#    meus_usuarios = Usuario.query.all()
#    usuario2 = Usuario.query.filter_by(username ='Joao').first()
#    print(usuario2)
#    print(usuario2.senha)
#    print(meus_usuarios)