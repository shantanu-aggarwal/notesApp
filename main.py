
"""
Created on Sat Jun  1 05:27:21 2024

@author: shantanuaggarwal
"""
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


from fastapi import FastAPI
from notesApp.routers import user_routes, note_routes
from notesApp.init import init

init()


app = FastAPI() ## add dependencies to check for token

app.include_router(user_routes.router)
app.include_router(note_routes.router)

@app.get('/')
async def app_root():
    return { "message" : "Welcome to AI assisted Notepad."}