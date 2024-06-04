#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 01:00:25 2024

@author: shantanuaggarwal
"""

from enum import Enum

class Status(Enum):
    ERROR = 0
    USER_UNDEFINED = -1
    SUCCESS  = 1
    INVALID_OPERATION = -2

class Roles(Enum):
    ADMIN = 'admin'
    USER = 'user'