import os
import base64
import requests

BASE_URL = "https://solved.ac/api/v3"

# ───────────────────────────────
# solved.ac 유저 정보 가져오기
# ───────────────────────────────
def get_user_info(username):
    url = f"{BASE_URL}/search/user"
    params = {"query": username}
    headers = {"Accept": "application/json"}
    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data["count"] > 0:
            return data["items"][0]
    return None

# ───────────────────────────────
# 티어 SVG Base64 인코딩
# ───────────────────────────────
def encode_tier_svg(tier, tier_svg_dir="tiers"):
    path = f"{tier_svg_dir}/tier_{tier}.svg"
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ {path} 없음")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/svg+xml;base64,{encoded}"

# ───────────────────────────────
# 배지 생성 함수
# ───────────────────────────────
def generate_boj_badge(user_info, username, output_dir="badge", tier_svg_dir="tiers"):
    os.makedirs(output_dir, exist_ok=True)

    tier = user_info["tier"]
    rating = user_info["rating"]
    logo_data_uri = encode_tier_svg(tier, tier_svg_dir)

    # 출력 경로 (유저명 기반)
    output_path = os.path.join(output_dir, f"boj_{username}.svg")

    # SVG 설정
    badge_width = 50
    badge_height = 20
    logo_size = 13
    logo_x = 6
    logo_y = 4

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{badge_width}" height="{badge_height}">
  <!-- 전체 배경 + 테두리 -->
  <rect x="0.5" y="0.5"
        width="{badge_width - 1}" height="{badge_height - 1}"
        rx="4" fill="#FFFFFF"
        stroke="#000000" stroke-width="0.1"
        vector-effect="non-scaling-stroke"/>

  <!-- 티어 아이콘 -->
  <image href="{logo_data_uri}" x="{logo_x}" y="{logo_y}"
         width="{logo_size}" height="{logo_size}" />

  <!-- 레이팅 숫자 -->
  <text x="{logo_x + logo_size + 4}" y="14.5"
        fill="#000000" font-family="Arial, sans-serif" font-size="12" font-weight="bold">{rating}</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"✅ '{username}'의 배지 생성 완료 → {output_path}")

# ───────────────────────────────
# 실행 부분
# ───────────────────────────────
if __name__ == "__main__":
    username = input("BOJ 유저명: ").strip()
    if not username:
        print("❌ 유저명을 입력하세요.")
    else:
        user_info = get_user_info(username)
        if user_info:
            generate_boj_badge(user_info, username)
        else:
            print(f"❌ '{username}' 유저를 찾을 수 없습니다.")
