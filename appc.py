from flask import Flask, request, jsonify, render_template

import dbcommands
import systemc
import messagesc

app = Flask(__name__)

@app.route('/')
def index():
    user_id = request.remote_addr
    dbcommands.dump_chat_history(user_id, messagesc.START_HISTORY)
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def chat():
    data = request.get_json()

    user_message = data.get('message')
    user_id = request.remote_addr

    if not user_message:
        return jsonify({'error': 'Please provide a "message"'}), 400
    
    chat_history = dbcommands.load_chat_history(user_id)
    result, new_chat_history = systemc.new_pipeline(user_message, chat_history)

    dbcommands.dump_chat_history(user_id, new_chat_history)

    return jsonify({'user_id': user_id, 'message': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
