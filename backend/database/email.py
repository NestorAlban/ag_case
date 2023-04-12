from fastapi import (
    BackgroundTasks,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
    status
)
import smtplib
import asyncio
import logging
import os
import jwt
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

from .token import Token

logger = logging.getLogger(__name__)
logger.level = logger.setLevel(logging.INFO)


from backend.models import User
from backend.schemas import EmailSchema

def create_conf():
    try:
        mail_username = os.getenv("EMAIL_FROM")
        mail_pass = os.getenv("EMAIL_PASSWORD")
        conf = ConnectionConfig(
            MAIL_USERNAME = mail_username,
            MAIL_PASSWORD = mail_pass,
            MAIL_FROM = mail_username,
            MAIL_PORT = 465,
            MAIL_SERVER = "smtp.gmail.com",
            # MAIL_TLS = True,
            # MAIL_SSL = False,
            MAIL_STARTTLS= False,
            MAIL_SSL_TLS = True,
            USE_CREDENTIALS = True,
            VALIDATE_CERTS = True
        )
        
    except Exception as database_exception:
        raise database_exception
    return conf


class EmailSend:
    
    async def send_email(email : EmailSchema, instance: User):
        email_to_use = email[0]
        token_data = {
            "id" : instance.user_id,
            "username" : instance.name,
            "email" : instance.mail
        }

        token = jwt.encode(token_data, os.getenv("SECRET_MAIL"), algorithm="HS256")

        template = f"""
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
                <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                    <h3> Account Verification </h3>
                    <br>
                    <p>Thanks for choosing AG page, please 
                    click on the link below to verify your account</p> 
                    <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                    href="http://localhost:8000/verification/?token={token}">
                        Verify your email
                    <a>
                    <p style="margin-top:1rem;">If you did not register for AG page, 
                    please kindly ignore this email and nothing will happen. Thanks<p>
                </div>
            </body>
            </html>
        """

        message = MessageSchema(
            subject="AG page Account Verification Mail",
            recipients=email,  # List of recipients, as many as you can pass 
            body=template,
            subtype="html"
        )
        conf = create_conf()
        
        fm = FastMail(conf)
        await asyncio.sleep(1)
        await fm.send_message(message)
        await asyncio.sleep(1)

    async def send_email_smt(email : EmailSchema, instance: User):
        success = False
        HOST = "smtp.gmail.com"
        PORT = 587
        s = smtplib.SMTP(HOST, PORT)
        s.starttls()

        mail_username = os.getenv("EMAIL_FROM")
        mail_pass = os.getenv("EMAIL_PASSWORD")
        s.login(mail_username, mail_pass)
        message = MIMEMultipart()
        email_to_use = email[0]
        message['From'] = mail_username
        message['To'] = email_to_use
        message['Subject'] = "AG page Account Verification Mail"
        
        
        token_data = {
            "id" : instance.user_id,
            "username" : instance.name,
            "email" : instance.mail
        }

        token = Token.create_access_token(token_data)

        template = f"""
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
                <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                    <h3> Account Verification </h3>
                    <br>
                    <p>Thanks for choosing AG page, please 
                    click on the link below to verify your account</p> 
                    <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                    href="http://142.93.115.61:8080//verification/?token={token}">
                        Verify your email
                    <a>
                    <p style="margin-top:1rem;">If you did not register for AG page, 
                    please kindly ignore this email and nothing will happen. Thanks<p>
                </div>
            </body>
            </html>
        """
        template_2 = 'Hello' 

        message.attach(MIMEText(template_2, 'plain'))
        message.attach(MIMEText(template, 'html'))

        texto = message.as_string()
        await asyncio.sleep(1)
        s.sendmail(mail_username, [email_to_use], texto)
        
        
        success = True

        s.quit()
        return success

