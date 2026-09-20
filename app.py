from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 机の初期状態（False=空席, True=使用中）
# id: 1~9(1~3列目の将棋), 10(4列目前 将棋), 11(オセロ), 12(囲碁), 13(4列目後 将棋)
desks = {str(i): False for i in range(1, 14)}

@app.route('/')
def index():
    # 画面を表示する
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def get_status():
    # 全ての机の現在の状態をJSONで返す
    return jsonify(desks)

@app.route('/toggle/<desk_id>', methods=['POST'])
def toggle(desk_id):
    # 指定された机の状態を反転させる
    if desk_id in desks:
        desks[desk_id] = not desks[desk_id]
        return jsonify({'status': 'success', 'state': desks[desk_id]})
    return jsonify({'status': 'error', 'message': 'Desk not found'}), 404

if __name__ == '__main__':
    # host='0.0.0.0' にすることで、同じWi-Fi内のスマホ等からもアクセス可能になります
    app.run(debug=True, host='0.0.0.0', port=5000)
