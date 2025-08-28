# app.py

from flask import Flask, render_template

app = Flask(__name__)

# 플레이어 이름 목록을 정의
PLAYER_NAMES = [
    "강아지똥", "고구마", "귤", "나미", "나인", "노하", "돌멩이", "돌체", 
    "디네로", "뚜", "룰루", "림프", "망고", "문문", "상일", "세준", "송하", 
    "스냅", "승민", "안아줘요", "야도란", "영재", "예수", "오팔", "옥수수", 
    "용준", "우주", "유미", "의성", "이방인", "인사이더", "자쓰민", "장현", 
    "재혁", "지구", "지호", "진상", "찐빵", "철", "체크", "카피바라", "쿠쿠", 
    "태산", "팔팔", "팝스타", "팬더", "포카드", "하람", "현", "호준", "홍", 
    "환경", "황", "훈", "BOK", "DD", "DY", "HM", "KJ", "Lin"
]

# 딜러 이름 목록을 플레이어 이름 목록과 동일하게 설정
DEALER_NAMES = PLAYER_NAMES

@app.route('/')
def home():
    # 딜러 및 플레이어 목록 데이터를 index.html로 전달
    return render_template('index.html', dealers=DEALER_NAMES, players=PLAYER_NAMES)

if __name__ == '__main__':
    app.run(debug=True)