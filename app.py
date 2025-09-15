# app.py (수정된 전체 코드)

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- Firebase Admin SDK 초기화 ---
# ‼️ 중요: 'your-key-file.json' 부분을 실제 다운로드한 키 파일 이름으로 변경하세요.
try:
    key_file_name = 'holdemresult-8e89d-firebase-adminsdk-fbsvc-257ead2785.json' # 예시 파일 이름
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

PLAYER_NAMES = [
    "강아지똥", "고구마", "귤", "나미", "나인", "노하", "돌멩이", "돌체", "디네로", "뚜", "룰루", "림프", "망고", "문문", "상일", "세준", "송하", "스냅", "승민", "안아줘요", "야도란", "영재", "영준", "예수", "오팔", "옥수수", "용준", "우주", "유미", "의성", "이방인", "인사이더", "자쓰민", "장현", "재혁", "재형", "지구", "지호", "진상", "찐빵", "철", "체크", "카피바라", "쿠쿠", "태산", "태은", "티라미슈", "팔팔", "팝스타", "팬더", "포카드", "하람", "현", "호준", "홍", "환경", "황", "훈", "BOK", "DD", "DY", "HM", "KJ", "Lin"
]
DEALER_NAMES = PLAYER_NAMES

# 기본 페이지('/') 렌더링
@app.route('/')
def home():
    return render_template('index.html', dealers=DEALER_NAMES, players=PLAYER_NAMES)

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