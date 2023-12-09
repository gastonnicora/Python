from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.users import User
import datetime
from app.helpers.modelosPlanos.confirmEmail import ConfirmEmail as C

class Company(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    owner= db.Column(
        db.String(255),
        ForeignKey(User.uuid),
        nullable= True
    ) 
    name= db.Column(
        db.String(255),
        nullable=True
    )
    address=db.Column(
        db.String(255),
        nullable=True
    )
    removed =db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    confirmed =db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    dateOfCreate=db.Column(
        db.String(255),
        nullable=True
    )
    dateOfUpdate=db.Column(
        db.String(255),
        nullable=True,
        default=None
    )