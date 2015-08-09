# tasktime
Serviço de tickets (help desk), timing e suporte.

App em fase de desenvolvimento visando o aprendizado flask (não estranhe encontrar muitas páginas repetitivas ou algo semelhante). Sinta-se livre para contribuir.

## Instalação
1. Faça o clone do repositório
```
git clone https://github.com/juliarizza/tasktime.git
```
2. Entre na pasta do projeto
```
cd tasktime
```
3. Instale as bibliotecas necessárias
```
sudo pip install -r requirements.txt
```
4. Execute
```
python run.py runserver
```
5. Abra seu navegador e acesse `http://localhost:5000`

**Note:** You will have to configure your own database. In this application, we use a postgresql configuration on `config.py` file wich points to a localhost database called **tasktime**.
