from ligastorrinha import model 
from ligastorrinha.sql_db import db
from sqlalchemy import Column, Integer , String , Text, ForeignKey
from sqlalchemy.orm import relationship
from flask import url_for

class League(db.Model ,model.Model, model.Base):
    __tablename__ = 'leagues'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    picture = Column(Text)

    editions = relationship('Edition', back_populates='league')

    def full_image_url(self):
        return url_for('static', filename="images/Leagues/{url}".format(url=self.picture))
