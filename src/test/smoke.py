# 야채마을 빠른 점검: 가짜 DB(mockdb.js)로 주인장 모드 페이지를 열고 JS 오류가 없는지 확인한다.
# 사용법: python3 src/test/smoke.py   (저장소 루트에서, playwright 필요)
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MOCK = os.path.join(ROOT, 'src', 'test', 'mockdb.js')
owner = '--visitor' not in sys.argv

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1400, 'height': 950})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    if not owner:
        pg.add_init_script('window.__OWNER=false')
    pg.add_init_script(path=MOCK)
    # 진짜 Firebase 대신 가짜 DB를 쓰도록 설정 파일을 비운다
    pg.route('**/firebase-config.js', lambda r: r.fulfill(body='', content_type='text/javascript'))
    pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    pg.goto('file://' + os.path.join(ROOT, 'index.html'))
    pg.wait_for_timeout(1500)
    for w in ['w-me', 'w-proj', 'w-likes', 'w-docs', 'w-log', 'w-rank', 'w-hhome', 'w-pin', 'w-bub', 'w-map']:
        pg.evaluate(f"go('{w}')")
        pg.wait_for_timeout(300)
        pg.locator('#' + w).screenshot(path=os.path.join(ROOT, 'src', 'test', f'shot_{w}.png'))
    print('오류:', errs or '없음')
    b.close()
