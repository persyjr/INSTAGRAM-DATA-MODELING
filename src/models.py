import enum
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er
#usando Sql Alchemist para hacer consultas
Base = declarative_base()
#Estoy declarando mi base de datos.
#El primer paso es declarar nuestro modelo de user.

class User(Base):
    # Aquí definimos el nombre de la tabla user.
    __tablename__ = 'user'                                      #En SQL Alquemist el nombre mi tabla debe ir en minuscula
    # Aquí definimos mis parametros de mi tabla.
    # Ten en cuenta que cada columna es también un atributo normal de primera instancia de Pyth
    id = Column(Integer, primary_key=True)                      #declaro esta como mi clave primaria
    username = Column(String(250), nullable=False)              #declaro la columna username
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    def to_dict(self):                                          #defino el dictionary de mi clase para que le asigne las propiedades a mi objeto
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname" : self.lastname,
            "email" : self.email
        }

class Post(Base):
    #estoy creando una clase post que hereda el ID de mi tabla User y el ID de mi tabla Comment
    __tablename__ = 'post'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }
    
class MediaType(enum.Enum):
    #esta funcion me permite trabajar con tipo de dato enum en mi clase media.
    imagen=1
    video=2
    galeria=3
    
class Media(Base):
    #estoy creando una tabla media que hereda el ID de mi tabla Post
    __tablename__ = 'media'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    type = Column('type',Enum(MediaType))                                       #este tipo de dato me permite escoger en tre imagen video o galeria
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'))                            #estoy indicando que mi clave post id se relaciona con la clave id de post
    post = relationship(Post)                                                   #estoy relacionando la variable post  de la clase Post en mi clase Media.
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }

class Comment(Base):
    #estoy creando una tabla commment que esta heredando el ID del User y el ID del Post
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250))
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship(User)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post)

    def to_dict(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
    
class Follower(Base):
    #estoy creando una tabla Follower que esta heredando el ID del usuario y las estoy ingresando en mis dos parametros de mi tabla.
    __tablename__ = 'follower'
    id= Column (Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'))
    user_to_id = Column (Integer, ForeignKey('user.id'))
    user= relationship(User)
    def to_dict(self):
        return {
            'user_from_id': self.user_from_id,
            'user_to_id': self.user_to_id,
            "id": self.id

        }



## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e