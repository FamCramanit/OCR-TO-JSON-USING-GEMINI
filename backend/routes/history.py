from flask import Blueprint, request, jsonify
from database import get_db_connection

history_bp = Blueprint('history', __name__)  # กำหนด Blueprint สำหรับจัดการ API

# API ดึงข้อมูลผู้ใช้ทั้งหมด
@history_bp.route('/api/history', methods=['GET'])
def get_history():
    conn = get_db_connection()
    histories = conn.execute('SELECT * FROM history_extract').fetchall()
    result = []

    for history in histories:
        items = conn.execute('SELECT * FROM items WHERE receipt_number = ? ', (history['receipt_number'],)).fetchall()
        history_dict = dict(history)  # Convert Row object to a dictionary
        history_dict['items'] = [dict(item) for item in items]  # Convert items to dictionaries
        result.append(history_dict)
    
    conn.close()
    return jsonify(result)

# API เพิ่มผู้ใช้ใหม่
@history_bp.route('/api/history_new', methods=['POST'])
def newHistory():
    history = request.get_json()
    store_name = history['store_name']
    date_time = history['date_time']
    receipt_number = history['receipt_number']
    items = history['items']
    vat = history['vat']
    total = history['total']
    image_receipt = history['image_receipt']

    conn = get_db_connection()
    conn.execute('INSERT INTO history_extract (store_name, date_time, receipt_number, vat, total, image_receipt) VALUES (?, ?, ?, ?, ?, ?)', (store_name, date_time, receipt_number, vat, total, image_receipt))

    for item in items:
        conn.execute('INSERT INTO items (receipt_number, item_name, quantity, price) VALUES (?, ?, ?, ?)', (receipt_number, item['item_name'], item['quantity'], item['price']))

    conn.commit()
    conn.close()
    
    return jsonify(history), 201

# API ลบข้อมูล
@history_bp.route('/api/history/<string:receipt_number>', methods=['DELETE'])
def deleteHistory(receipt_number):
    conn = get_db_connection()

    # ลบข้อมูลจาก items ที่เกี่ยวข้องกับ receipt_number ก่อน
    conn.execute('DELETE FROM items WHERE receipt_number = ?', (receipt_number,))
    # ลบข้อมูลจาก history_extract
    conn.execute('DELETE FROM history_extract WHERE receipt_number = ?', (receipt_number,))

    conn.commit()
    conn.close()
    
    return jsonify({'message': f'History with receipt_number {receipt_number} has been deleted successfully'}), 200

@history_bp.route('/api/history/<string:receipt_number>', methods=['PUT'])
def updateHistory(receipt_number):
    history = request.get_json()
    store_name = history.get('store_name')
    date_time = history.get('date_time')
    vat = history.get('vat')
    total = history.get('total')
    items = history.get('items', [])

    conn = get_db_connection()
    cur = conn.cursor()

    # อัปเดตข้อมูลใน history_extract
    cur.execute('''
        UPDATE history_extract
        SET store_name = ?, date_time = ?, vat = ?, total = ?
        WHERE receipt_number = ?
    ''', (store_name, date_time, vat, total, receipt_number))

    # ลบรายการเก่าออกก่อนแล้วค่อยเพิ่มใหม่
    cur.execute('DELETE FROM items WHERE receipt_number = ?', (receipt_number,))

    for item in items:
        cur.execute('''
            INSERT INTO items (receipt_number, item_name, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (receipt_number, item['item_name'], item['quantity'], item['price']))

    conn.commit()
    conn.close()

    return jsonify({'message': f'History with receipt_number {receipt_number} has been updated successfully'}), 200
# API อัปเดตข้อมูล
# @history_bp.route('/api/history/<string:receipt_number>', methods=['PUT'])
# def updateHistory(receipt_number):
#     history = request.get_json()
#     store_name = history.get('store_name')
#     date_time = history.get('date_time')
#     vat = history.get('vat')
#     total = history.get('total')
#     items = history.get('items', [])

#     conn = get_db_connection()
#     cur = conn.cursor()

#     try:
#         # อัปเดตข้อมูลใน history_extract
#         cur.execute('''
#             UPDATE history_extract
#             SET store_name = ?, date_time = ?, vat = ?, total = ?
#             WHERE receipt_number = ?
#         ''', (store_name, date_time, vat, total, receipt_number))

#         # อัปเดตรายการสินค้า
#         for item in items:
#             # ตรวจสอบว่ามีรายการสินค้านี้อยู่แล้วหรือไม่
#             cur.execute('''
#                 SELECT COUNT(*) FROM items 
#                 WHERE receipt_number = ? AND item_name = ?
#             ''', (receipt_number, item['item_name']))
            
#             exists = cur.fetchone()[0] > 0
            
#             if exists:
#                 # อัปเดตรายการที่มีอยู่
#                 cur.execute('''
#                     UPDATE items 
#                     SET quantity = ?, price = ?
#                     WHERE receipt_number = ? AND item_name = ?
#                 ''', (item['quantity'], item['price'], receipt_number, item['item_name']))
#             else:
#                 # เพิ่มรายการใหม่
#                 cur.execute('''
#                     INSERT INTO items (receipt_number, item_name, quantity, price)
#                     VALUES (?, ?, ?, ?)
#                 ''', (receipt_number, item['item_name'], item['quantity'], item['price']))

#         conn.commit()
#         return jsonify({'message': f'History with receipt_number {receipt_number} has been updated successfully'}), 200
    
#     except Exception as e:
#         conn.rollback()
#         return jsonify({'error': str(e)}), 500
#     finally:
#         conn.close()
