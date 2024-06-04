#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 16:43:28 2024

@author: shantanuaggarwal
"""

from pydantic import BaseModel

class Note:
    id    : str
    title : str 
    body  : str
