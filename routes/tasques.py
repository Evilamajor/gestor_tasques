from flask import Blueprint, jsonify, request
from db import get_db_connection

tasques_bp = Blueprint('tasques_bp', __name__)

# GET totes les tasques
@tasques_bp.route('/api/v1/tasques', methods=['GET'])
def get_tasques():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasques ORDER BY id;')
    tasques = cur.fetchall()
    cur.close()
    conn.close()

    tasques_list = []
    for t in tasques:
        tasques_list.append({
            'id': t[0],
            'titol': t[1],
            'descripcio': t[2],
            'data_venciment': str(t[3]) if t[3] else None,
            'completat': t[4]
        })
    return jsonify(tasques_list)

# GET una tasca per ID
@tasques_bp.route('/api/v1/tasques/<int:id>', methods=['GET'])
def get_tasca(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasques WHERE id = %s;', (id,))
    tasca = cur.fetchone()
    cur.close()
    conn.close()

    if tasca is None:
        return jsonify({'error': 'Tasca no trobada'}), 404

    return jsonify({
        'id': tasca[0],
        'titol': tasca[1],
        'descripcio': tasca[2],
        'data_venciment': str(tasca[3]) if tasca[3] else None,
        'completat': tasca[4]
    })

# POST nova tasca
@tasques_bp.route('/api/v1/tasques', methods=['POST'])
def crear_tasca():
    dades = request.get_json()
    titol = dades.get('titol')
    descripcio = dades.get('descripcio', '')
    data_venciment = dades.get('data_venciment')
    completat = dades.get('completat', False)

    if not titol:
        return jsonify({'error': 'El camp \"titol\" és obligatori'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tasques (titol, descripcio, data_venciment, completat)
        VALUES (%s, %s, %s, %s) RETURNING id;
    ''', (titol, descripcio, data_venciment, completat))
    nou_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'id': nou_id, 'missatge': 'Tasca creada correctament'}), 201

# PUT per actualitzar una tasca sencera
@tasques_bp.route('/api/v1/tasques/<int:id>', methods=['PUT'])
def actualitzar_tasca(id):
    dades = request.get_json()
    titol = dades.get('titol')
    descripcio = dades.get('descripcio')
    data_venciment = dades.get('data_venciment')
    completat = dades.get('completat')

    if not titol or completat is None:
        return jsonify({'error': 'Camps obligatoris: titol i completat'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE tasques
        SET titol = %s, descripcio = %s, data_venciment = %s, completat = %s
        WHERE id = %s RETURNING id;
    ''', (titol, descripcio, data_venciment, completat, id))
    resultat = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if resultat is None:
        return jsonify({'error': 'Tasca no trobada'}), 404

    return jsonify({'missatge': f'Tasca amb ID {id} actualitzada'})

# DELETE una tasca
@tasques_bp.route('/api/v1/tasques/<int:id>', methods=['DELETE'])
def eliminar_tasca(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasques WHERE id = %s RETURNING id;', (id,))
    resultat = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if resultat is None:
        return jsonify({'error': 'Tasca no trobada'}), 404

    return jsonify({'missatge': f'Tasca amb ID {id} eliminada'})
