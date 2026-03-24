from playwright.sync_api import sync_playwright
import json

play = sync_playwright().start()
browser = play.chromium.launch(headless=False, args=["--start-maximized"])
page = browser.new_page(no_viewport=True)

page.goto("https://finance.naver.com/")
# 리서치 클릭 -> 종목분석 리포트 클릭
page.get_by_role("link", name="리서치").click()
page.get_by_role("link", name="종목분석 리포트").click()

# 1. 테이블 타겟팅
tag_table = page.locator("table.type_1")

# 2. 헤더 추출
tag_header = tag_table.locator("th").all_inner_texts()
print("헤더:", tag_header)

# 3. 바디 추출: tbody 안에 있는 tr 타겟팅합니다.
tag_body = []
rows = tag_table.locator("tbody > tr").all()

for tag_tr in rows:
    # 각 행에서 td만 추출
    tag_td = tag_tr.locator("td").all_inner_texts()
    
    if tag_td and tag_td[0].strip():
        cleaned_td = [td.strip() for td in tag_td]
        tag_body.append(cleaned_td)
        print(cleaned_td)


dumped = json.dumps({"header": tag_header, "body": tag_body}, indent=2, ensure_ascii=False)
with open("page_3.json", "w", encoding="utf-8") as fp:
    fp.write(dumped)


