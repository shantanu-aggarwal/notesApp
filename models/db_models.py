#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 16:46:52 2024

@author: shantanuaggarwal
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from notesApp.database.init import Base

class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True, index=True)
    content = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="notes")
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    is_verified = Column(Boolean, default=True) # if user verified email
    
    notes = relationship("Note", back_populates="user" )

