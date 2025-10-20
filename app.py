# app.py (수정된 전체 코드)

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- Firebase Admin SDK 초기화 ---
try:
    key_file_name = 'holdemresult-8e89d-firebase-adminsdk-fbsvc-257ead2785.json'
    key_path = os.path.join(os.path.dirname(__file__), key_file_name)
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Firebase 초기화 실패: {e}")
    db = None
# ------------------------------------

app = Flask(__name__)
CORS(app)

# 기본 페이지('/') 렌더링
# 이제 하드코딩된 리스트를 전달하지 않습니다. 클라이언트에서 직접 Firebase 데이터를 가져옵니다.
@app.route('/')
def home():
    return render_template('index.html')

# ## 데이터 제공 API 엔드포인트 ##
@app.route('/api/game-data')
def get_game_data():
    if not db:
        return jsonify({"error": "Firebase is not initialized."}), 500

    try:
        doc_ref = db.collection('gameStates').document('latestState')
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({"error": "No data found"}), 404

        state = doc.to_dict()

        players_data = state.get('players', [])
        player_summary = []
        for index, player in enumerate(players_data):
            entries = player.get('entries', [])
            player_summary.append({
                "number": index + 1, "player": player.get('name', ''),
                "entry_fee": 'O' if player.get('entryFee') else 'X',
                "early": 'O' if player.get('earlyBird') else 'X',
                "buy_in": entries[0] if len(entries) > 0 else '',
                "rebuy1": entries[1] if len(entries) > 1 else '',
                "rebuy2": entries[2] if len(entries) > 2 else ''
            })

        total_buy_ins = sum(len(p.get('entries', [])) for p in players_data)
        total_prize = total_buy_ins * 250

        prize_summary = { "total_prize": total_prize }

        response_data = {
            "player_status": player_summary,
            "prize_status": prize_summary,
            "last_updated": state.get('date', 'N/A')
        }
        return jsonify(response_data)

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": "An error occurred on the server"}), 500


if __name__ == '__main__':
    app.run(debug=True)