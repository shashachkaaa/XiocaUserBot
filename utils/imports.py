import pip, os, re, random, importlib, subprocess, inspect, traceback, base64, threading, sys, string
from types import ModuleType
from typing import Dict
from pathlib import Path
from utils.db import db
req = ["fuzzywuzzy", "kurigram", "gtts", "pyttsx3", "psutil", "SpeechRecognition", 'pydub', "colorama", "unidecode", "pyfiglet", "pytz", "fade", "sympy"]
try:
	from fuzzywuzzy import process
	from pyrogram.handlers import MessageHandler
	from pyrogram import Client, filters, idle, errors, types
	from pyrogram.raw.functions.account import GetAuthorizations, DeleteAccount
	from pyrogram.types import ChatPermissions
	from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
	import sqlite3, logging, time, requests, asyncio, datetime, random, json, html, psutil, shutil, platform, pyfiglet, fade
	from datetime import datetime, timedelta
	from time import gmtime, strptime, strftime
	from io import StringIO
	from contextlib import redirect_stdout
	from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
	import pytz
	from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
	from pyrogram.raw.functions.account import ReportPeer
	from pyrogram.raw.types import *
	from unidecode import unidecode as ui
	from colorama import Fore, Style
	from pyrogram.types import Message, User, Chat
	from pyrogram.file_id import FileId, PHOTO_TYPES
	from types import FunctionType
	from typing import Any, List, Literal, Tuple, Union
except Exception as e:
	print(e)
	for i in req:
		subprocess.run(["pip", 'install', i])
	os.execvp(sys.executable, [sys.executable, "main.py"])