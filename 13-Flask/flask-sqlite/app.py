from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import re
from contextlib import closing

app = Flask(__name__)

# Database setup
DATABASE = 'emaillist.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # returns rows as dictionaries(not tuples)
    return conn

def init_db():
    """Initialize database with email_list table"""
    with closing(get_db()) as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS email_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Initialize database on startup
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Display the email subscription form and handle submissions"""
    message = None
    message_type = None
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validation
        if not name:
            message = 'Name is required'
            message_type = 'error'
        elif not email:
            message = 'Email is required'
            message_type = 'error'
        elif not is_valid_email(email):
            message = 'Invalid email format'
            message_type = 'error'
        else:
            # Insert into database
            try:
                with closing(get_db()) as db:
                    db.execute('INSERT INTO email_list (name, email) VALUES (?, ?)', (name, email))
                    db.commit()
                message = 'Successfully subscribed!'
                message_type = 'success'
            except sqlite3.IntegrityError:
                message = 'Email already exists'
                message_type = 'error'
            except Exception as e:
                message = str(e)
                message_type = 'error'
    
    return render_template('index.html', message=message, message_type=message_type)

@app.route('/admin')
def admin():
    with closing(get_db()) as db:
        cursor = db.execute('SELECT id, name, email, created_at FROM email_list ORDER BY created_at DESC')
        subscribers = cursor.fetchall()
    return render_template('admin.html', subscribers=subscribers)

# API Routes
@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.form
    print(request.form)
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    
    # Validation
    if not name:
        return jsonify({'success': False, 'error': 'Name is required'}), 400
    
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400
    
    if not is_valid_email(email):
        return jsonify({'success': False, 'error': 'Invalid email format'}), 400
    
    # Insert into database
    try:
        with closing(get_db()) as db:
            db.execute('INSERT INTO email_list (name, email) VALUES (?, ?)', (name, email))
            db.commit()
        return jsonify({'success': True, 'message': 'Successfully subscribed!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/subscribers', methods=['GET'])
def get_subscribers():
    try:
        with closing(get_db()) as db:
            cursor = db.execute('SELECT id, name, email, created_at FROM email_list ORDER BY created_at DESC')
            print(dict(cursor.fetchall()[0]))
            subscribers = [dict(row) for row in cursor.fetchall()]
        return jsonify({'success': True, 'data': subscribers}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/delete/<int:subscriber_id>', methods=['POST'])
def delete_subscriber_form(subscriber_id):
    """Delete a subscriber and redirect back to admin page"""
    try:
        with closing(get_db()) as db:
            db.execute('DELETE FROM email_list WHERE id = ?', (subscriber_id,))
            db.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        return redirect(url_for('admin'))

@app.route('/api/subscribers/<int:subscriber_id>', methods=['DELETE'])
def delete_subscriber(subscriber_id):
    """API endpoint to delete a subscriber"""
    try:
        with closing(get_db()) as db:
            cursor = db.execute('DELETE FROM email_list WHERE id = ?', (subscriber_id,))
            db.commit()
            
            if cursor.rowcount == 0:
                return jsonify({'success': False, 'error': 'Subscriber not found'}), 404
            
        return jsonify({'success': True, 'message': 'Subscriber deleted'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

