import pip, os, re, random, importlib
try:
	from pyrogram.handlers import MessageHandler
	from pyrogram import Client, filters, idle
	from pyrogram.raw.functions.account import GetAuthorizations, DeleteAccount
	from pyrogram.types import ChatPermissions
	from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
	from gtts import gTTS
	import sqlite3, logging, time, requests, asyncio, pyttsx3, datetime, random, json, g4f, html, psutil, platform, sys, pyfiglet
	from datetime import datetime, timedelta
	from time import gmtime, strptime, strftime
	from io import StringIO
	from contextlib import redirect_stdout
	import subprocess
	import speech_recognition as sr
	from pydub import AudioSegment
	from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
	import pytz
	from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
	from pyrogram.raw.functions.account import ReportPeer
	from pyrogram.raw.types import *
	from unidecode import unidecode as ui
	from colorama import Fore, Style
except Exception as e:
	print(e)
	pip.main(['install', '-r', 'requirements.txt'])
	os.execvp(sys.executable, [sys.executable, "main.py"])