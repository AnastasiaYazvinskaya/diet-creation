import sqlite3
from flask import render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError, abort

# Get connection to db
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn