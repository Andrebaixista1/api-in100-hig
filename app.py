from flask import Flask, jsonify, request
from flask_cors import CORS  # Importe o CORS
import mysql.connector
from mysql.connector import pooling
import os

app = Flask(__name__)

# Habilita CORS para o domínio do front-end
CORS(app, resources={r"/api/*": {"origins": "https://vieirain100-2.vercel.app/"}})

# Configuração do pool de conexões MySQL
db_config = {
    'host': '45.179.91.180',
    'port': 3306,
    'user': 'andrefelipe',
    'password': '899605aA@',
    'database': 'vieira_online'
}

# Cria um pool de conexões
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

# Rota de teste
@app.route('/test', methods=['GET'])
def test():
    try:
        # Conectar ao MySQL
        connection = connection_pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM inss_higienizado LIMIT 1')
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return jsonify({'status': 'success', 'message': 'API está rodando e conectada ao MySQL!', 'data': result})
        else:
            return jsonify({'status': 'success', 'message': 'API está rodando, mas a tabela inss_higienizado está vazia.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Inserção com atualização se já existir o mesmo CPF e NB
@app.route('/api/insert', methods=['POST'])
def insert():
    data = request.json
    query = """
        INSERT INTO inss_higienizado (
            id, numero_beneficio, numero_documento, nome, estado, pensao, data_nascimento,
            tipo_bloqueio, data_concessao, tipo_credito, limite_cartao_beneficio, saldo_cartao_beneficio,
            status_beneficio, data_fim_beneficio, limite_cartao_consignado, saldo_cartao_consignado,
            saldo_credito_consignado, saldo_total_maximo, saldo_total_utilizado, saldo_total_disponivel,
            data_consulta, data_retorno_consulta, tempo_retorno_consulta, nome_representante_legal,
            banco_desembolso, agencia_desembolso, numero_conta_desembolso, digito_conta_desembolso,
            numero_portabilidades, ip_origem, data_hora_registro, nome_arquivo
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nome = VALUES(nome),
            estado = VALUES(estado),
            pensao = VALUES(pensao),
            data_nascimento = VALUES(data_nascimento),
            tipo_bloqueio = VALUES(tipo_bloqueio),
            data_concessao = VALUES(data_concessao),
            tipo_credito = VALUES(tipo_credito),
            limite_cartao_beneficio = VALUES(limite_cartao_beneficio),
            saldo_cartao_beneficio = VALUES(saldo_cartao_beneficio),
            status_beneficio = VALUES(status_beneficio),
            data_fim_beneficio = VALUES(data_fim_beneficio),
            limite_cartao_consignado = VALUES(limite_cartao_consignado),
            saldo_cartao_consignado = VALUES(saldo_cartao_consignado),
            saldo_credito_consignado = VALUES(saldo_credito_consignado),
            saldo_total_maximo = VALUES(saldo_total_maximo),
            saldo_total_utilizado = VALUES(saldo_total_utilizado),
            saldo_total_disponivel = VALUES(saldo_total_disponivel),
            data_consulta = VALUES(data_consulta),
            data_retorno_consulta = VALUES(data_retorno_consulta),
            tempo_retorno_consulta = VALUES(tempo_retorno_consulta),
            nome_representante_legal = VALUES(nome_representante_legal),
            banco_desembolso = VALUES(banco_desembolso),
            agencia_desembolso = VALUES(agencia_desembolso),
            numero_conta_desembolso = VALUES(numero_conta_desembolso),
            digito_conta_desembolso = VALUES(digito_conta_desembolso),
            numero_portabilidades = VALUES(numero_portabilidades),
            ip_origem = VALUES(ip_origem),
            data_hora_registro = VALUES(data_hora_registro),
            nome_arquivo = VALUES(nome_arquivo)
    """
    params = [
        data.get('id'),
        data.get('numero_beneficio'),
        data.get('numero_documento'),
        data.get('nome'),
        data.get('estado'),
        data.get('pensao'),
        data.get('data_nascimento'),
        data.get('tipo_bloqueio'),
        data.get('data_concessao'),
        data.get('tipo_credito'),
        data.get('limite_cartao_beneficio'),
        data.get('saldo_cartao_beneficio'),
        data.get('status_beneficio'),
        data.get('data_fim_beneficio'),
        data.get('limite_cartao_consignado'),
        data.get('saldo_cartao_consignado'),
        data.get('saldo_credito_consignado'),
        data.get('saldo_total_maximo'),
        data.get('saldo_total_utilizado'),
        data.get('saldo_total_disponivel'),
        data.get('data_consulta'),
        data.get('data_retorno_consulta'),
        data.get('tempo_retorno_consulta'),
        data.get('nome_representante_legal'),
        data.get('banco_desembolso'),
        data.get('agencia_desembolso'),
        data.get('numero_conta_desembolso'),
        data.get('digito_conta_desembolso'),
        data.get('numero_portabilidades'),
        data.get('ip_origem'),
        data.get('data_hora_registro'),
        data.get('nome_arquivo')
    ]
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'results': 'Dados inseridos/atualizados com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# DELETE: exclui todos os registros com o mesmo nome_arquivo
@app.route('/api/delete', methods=['DELETE'])
def delete():
    nome_arquivo = request.args.get('nome_arquivo')
    if not nome_arquivo:
        return jsonify({'success': False, 'message': 'nome_arquivo é obrigatório'}), 400
    query = 'DELETE FROM inss_higienizado WHERE nome_arquivo = %s'
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (nome_arquivo,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'results': f'{cursor.rowcount} registros excluídos'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# GET: retorna os registros com o mesmo nome_arquivo para download
@app.route('/api/download', methods=['GET'])
def download():
    nome_arquivo = request.args.get('nome_arquivo')
    if not nome_arquivo:
        return jsonify({'success': False, 'message': 'nome_arquivo é obrigatório'}), 400
    query = 'SELECT * FROM inss_higienizado WHERE nome_arquivo = %s'
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (nome_arquivo,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Iniciar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
