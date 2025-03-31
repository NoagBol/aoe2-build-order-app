import sqlite3
import json
from datetime import datetime
from pathlib import Path

def get_db_path():
    """Get the path to the SQLite database file."""
    db_dir = Path(__file__).parent.parent.parent / 'data'
    db_dir.mkdir(exist_ok=True)
    return db_dir / 'aoe2_builds.db'

def init_db():
    """Initialize the database with required tables."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            aoe2_username TEXT,
            aoe2_platform TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create build_orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS build_orders (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            type TEXT,
            difficulty TEXT,
            primary_goal TEXT,
            execution_time TEXT,
            resource_allocation TEXT,
            steps TEXT,
            ideal_civilizations TEXT,
            suitable_maps TEXT,
            tips TEXT,
            video_url TEXT,
            notes TEXT,
            creator_id TEXT,
            is_public BOOLEAN DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users (id)
        )
    ''')
    
    # Create shared_build_orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS shared_build_orders (
            build_order_id TEXT,
            shared_with_id TEXT,
            shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (build_order_id, shared_with_id),
            FOREIGN KEY (build_order_id) REFERENCES build_orders (id),
            FOREIGN KEY (shared_with_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user(user_id):
    """Get user by ID."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, email, password_hash, aoe2_username=None, aoe2_platform=None):
    """Create a new user."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    user_id = f"user_{datetime.now().timestamp()}"
    c.execute('''
        INSERT INTO users (id, username, email, password_hash, aoe2_username, aoe2_platform)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, email, password_hash, aoe2_username, aoe2_platform))
    conn.commit()
    conn.close()
    return user_id

def save_build_order(build_order, user_id):
    """Save a build order to the database."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    
    # Generate a unique ID if not provided
    if 'id' not in build_order:
        build_order['id'] = f"bo_{datetime.now().timestamp()}"
    
    # Convert lists and dicts to JSON strings
    build_order['resource_allocation'] = json.dumps(build_order['resource_allocation'])
    build_order['steps'] = json.dumps(build_order['steps'])
    build_order['ideal_civilizations'] = json.dumps(build_order['ideal_civilizations'])
    build_order['suitable_maps'] = json.dumps(build_order['suitable_maps'])
    
    c.execute('''
        INSERT INTO build_orders (
            id, name, description, type, difficulty, primary_goal,
            execution_time, resource_allocation, steps, ideal_civilizations,
            suitable_maps, tips, video_url, notes, creator_id, is_public, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        build_order['id'], build_order['name'], build_order['description'],
        build_order['type'], build_order['difficulty'], build_order['primary_goal'],
        build_order['execution_time'], build_order['resource_allocation'],
        build_order['steps'], build_order['ideal_civilizations'],
        build_order['suitable_maps'], build_order['tips'],
        build_order.get('video_url'), build_order.get('notes'),
        user_id, build_order.get('is_public', False),
        build_order.get('status', 'pending')
    ))
    
    conn.commit()
    conn.close()
    return build_order['id']

def get_user_build_orders(user_id, include_shared=True):
    """Get all build orders for a user, including shared ones if requested."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    
    if include_shared:
        c.execute('''
            SELECT bo.* FROM build_orders bo
            LEFT JOIN shared_build_orders sbo ON bo.id = sbo.build_order_id
            WHERE bo.creator_id = ? OR sbo.shared_with_id = ?
        ''', (user_id, user_id))
    else:
        c.execute('SELECT * FROM build_orders WHERE creator_id = ?', (user_id,))
    
    build_orders = []
    for row in c.fetchall():
        bo = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'type': row[3],
            'difficulty': row[4],
            'primary_goal': row[5],
            'execution_time': row[6],
            'resource_allocation': json.loads(row[7]),
            'steps': json.loads(row[8]),
            'ideal_civilizations': json.loads(row[9]),
            'suitable_maps': json.loads(row[10]),
            'tips': row[11],
            'video_url': row[12],
            'notes': row[13],
            'creator_id': row[14],
            'is_public': bool(row[15]),
            'status': row[16],
            'created_at': row[17],
            'updated_at': row[18]
        }
        build_orders.append(bo)
    
    conn.close()
    return build_orders

def update_build_order(build_order_id, updates, user_id):
    """Update a build order."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    
    # Verify ownership
    c.execute('SELECT creator_id FROM build_orders WHERE id = ?', (build_order_id,))
    result = c.fetchone()
    if not result or result[0] != user_id:
        conn.close()
        return False
    
    # Convert lists and dicts to JSON strings
    for key in ['resource_allocation', 'steps', 'ideal_civilizations', 'suitable_maps']:
        if key in updates:
            updates[key] = json.dumps(updates[key])
    
    # Build update query
    update_fields = []
    values = []
    for key, value in updates.items():
        update_fields.append(f"{key} = ?")
        values.append(value)
    
    values.append(datetime.now().isoformat())  # updated_at
    values.append(build_order_id)
    values.append(user_id)
    
    query = f'''
        UPDATE build_orders 
        SET {', '.join(update_fields)}, updated_at = ?
        WHERE id = ? AND creator_id = ?
    '''
    
    c.execute(query, values)
    conn.commit()
    conn.close()
    return True

def share_build_order(build_order_id, shared_with_email, user_id):
    """Share a build order with another user."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    
    # Verify ownership
    c.execute('SELECT creator_id FROM build_orders WHERE id = ?', (build_order_id,))
    result = c.fetchone()
    if not result or result[0] != user_id:
        conn.close()
        return False, "Not authorized to share this build order"
    
    # Get shared_with user ID
    c.execute('SELECT id FROM users WHERE email = ?', (shared_with_email,))
    shared_with = c.fetchone()
    if not shared_with:
        conn.close()
        return False, "User not found"
    
    # Share the build order
    c.execute('''
        INSERT OR IGNORE INTO shared_build_orders (build_order_id, shared_with_id)
        VALUES (?, ?)
    ''', (build_order_id, shared_with[0]))
    
    conn.commit()
    conn.close()
    return True, "Build order shared successfully" 