# 
FROM python:slim-bullseye
WORKDIR /final-project
COPY /site /final-project
ENV FLASK_APP="main.py"
ENV FLASK_DEBUG=1
RUN pip install --upgrade pip \ 
    # flask framework    
    pip install flask \
    # flask login module for website       
    flask_login \ 
    # sql_alchemy module to communicate with DB
    flask_sqlalchemy \ 
    # bcrypt for encryption
    bcrypt \
    # pyJWT using for api to encode and decode token
    pyJWT \
    # boto3 using to retrieve secrets from aws secrets manager
    boto3 \
    # 
    pymysql
EXPOSE 80 22
CMD [ "python", "main.py" ]