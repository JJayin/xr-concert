#!/usr/bin/env python3
"""
XR Concert React Presentation을 PDF로 변환하는 스크립트
각 슬라이드를 개별 PDF로 생성 후 병합
"""

import sys
import os
from pathlib import Path
import shutil
import json

def check_and_install_dependencies():
    """필요한 라이브러리 확인 및 설치 안내"""
    try:
        from playwright.sync_api import sync_playwright
        from PyPDF2 import PdfMerger, PdfReader, PdfWriter
        return True
    except ImportError:
        print("❌ 필요한 라이브러리가 설치되어 있지 않습니다.")
        print("📦 설치 중...")
        
        result_pw = os.system(f"{sys.executable} -m pip install playwright --user")
        if result_pw != 0:
            print("❌ playwright 설치 실패")
            return False
        result_pw_install = os.system(f"{sys.executable} -m playwright install chromium")
        if result_pw_install != 0:
            print("❌ Chromium 설치 실패")
            return False
        
        result_pypdf = os.system(f"{sys.executable} -m pip install PyPDF2 --user")
        if result_pypdf != 0:
            print("❌ PyPDF2 설치 실패")
            return False
            
        print("✅ 설치 완료! 다시 시도 중...")
        try:
            from playwright.sync_api import sync_playwright
            from PyPDF2 import PdfMerger, PdfReader, PdfWriter
            return True
        except ImportError:
            print("❌ 설치 후에도 라이브러리를 불러올 수 없습니다.")
            return False

def generate_presentation_html():
    """React 프레젠테이션 데이터를 기반으로 정적 HTML 생성"""
    
    slides_data = [
        {
            'id': 1,
            'type': 'title',
            'title': 'XR CONCERT',
            'subtitle': 'Unreal Engine Project'
        },
        {
            'id': 2,
            'type': 'index',
            'title': 'INDEX',
            'items': ['1. Purpose', '2. Project Strategy', '3. Artist', '4. Levels']
        },
        {
            'id': 3,
            'type': 'content',
            'title': 'PURPOSE',
            'subtitle': '언리얼엔진으로 구현하는 XR콘서트의 목적',
            'body': '언리얼엔진은 사진처럼 사실적인 고품질 그래픽을 실시간으로 구현할 수 있는 게임 엔진 프로그램이다. 따라서 XR콘서트에서 언리얼엔진을 사용하는 목적과 이유는 사실적인 공간을 재현하는 무대를 구성하며, 현실과 가상을 넘나들기 위함일 것이다.',
            'highlight': '그렇다면 언리얼 환경에서 단상이 있는 XR 콘서트를 구현할 필요가 있는가?',
        },
        {
            'id': 4,
            'type': 'content',
            'title': '첫번째',
            'body': "리얼 타임으로 구현을 한다고 가정을 했을 때, 현재는 ICVFX, 즉 IN-Camera VFX 방식을 사용한 콘서트가 대다수이다 (이마저도 유튜브에 'XR콘서트'라고 검색어를 치면 참고할만한 자료가 3년 전.). 근데 이 ICVFX 스튜디오는 이미 LED 스크린으로 구성된 바닥과 벽이 이미 단상처럼 구성되어있다. 심지어 메인 조명도 언리얼 환경이 아닌 실제 환경에서 컨트롤 한다.",
            'highlight': "'X'라고 생각한다. 그 이유는 크게 두가지가 있다."
        },
        {
            'id': 5,
            'type': 'content',
            'title': '두번째',
            'body': "XR콘서트의 콘텐츠를 제공할 때, 대부분의 소비자들은 헤드마운트와 같은 기기를 사용할 것이다. 이를 보았을 때, 콘텐츠를 소비하는 사람들은 '과연 현실에 있는 무대를 원할까?' 아니면 '현실에서 느낄 수 없는 다른 차원의 것을 원할까?' 이를 고민해보았을 때, 역시나 후자가 더 많을 것이다.",
            'highlight': "현실에서 느낄 수 없는 다른 차원의 것을 원할까?"
        },
        {
            'id': 6,
            'type': 'content',
            'title': 'PROJECT STRATEGY',
            'body': '그렇기 때문에, 현실에서 만들어낼 수 없는 (혹은 실제 환경에서 표현하기 어려운) 요소와 구성을 넣는 것이 필요하다고 생각했다.',
            'links': [
                {'text': '참고 자료 보기 →', 'url': 'https://www.instagram.com/p/DFCkAR1ytkA/'},
                {'text': 'Rolling Stone Korea 기사 보기 →', 'url': 'https://rollingstone.co.kr/main/$/21209'}
            ],
            'highlight': '그래서 프로젝트 안에 여러 개의 컨셉적인 테마를 가진 각각의 레벨을 제작을 하였다. 이는 하나의 스튜디오에 여러개의 세트장이 있는 효과를 낼 수 있다.'
        },
        {
            'id': 7,
            'type': 'profile',
            'title': 'ARTIST',
            'subtitle': '아티스트 소개 및 콘서트 로그라인',
            'body': '아티스트에 대한 조사를 한 뒤, 아티스트의 컨셉과 어울리는 콘서트 제작을 계획하였다.',
            'highlight': '아티스트 소개'
        },
        {
            'id': 8,
            'type': 'profile-detail',
            'title': '딘(Dean)',
            'items': [
                'GENRE: Alternative RnB, Future RnB',
                'CONCEPT: Distopia / 신비주의 / 도시적인 / 몽환 <1984>',
                '그 외 특징: 인스타 계정 이름도 뒤에 trbl(Trouble)을 붙이며, 특유의 우울함을 추구'
            ],
            'links': [
                {'text': 'Instagram 프로필 보기 →', 'url': 'https://www.instagram.com/deantrbl/'}
            ]
        },
        {
            'id': 9,
            'type': 'quote',
            'title': '콘서트 로그라인',
            'highlight': '"무너져가는 디스토피아에서 불안정함을 노래하다."'
        },
        {
            'id': 10,
            'type': 'image-grid',
            'title': '4. Levels',
            'body': '노래에 어울리는 컨셉과 관련된 내용으로 레벨을 제작하였다.',
            'items': ["Howlin' 404", 'NASA', 'Bonnie & Clyde', 'Nocturne 07']
        }
    ]
    
    html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>XR Concert Presentation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@300;500;800&family=Noto+Sans+KR:wght@300;500;700;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-color: #050505;
      --text-main: #ffffff;
      --accent-acid: #CCFF00;
      --accent-red: #ff3b3b;
      --font-head: 'Archivo Black', sans-serif;
      --font-ui: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;
    }}
    
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    
    body {{
      background: var(--bg-color);
      color: var(--text-main);
      font-family: var(--font-ui);
      -webkit-font-smoothing: antialiased;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    }}
    
    .slide-container {{
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 60px;
      position: relative;
      background: var(--bg-color);
    }}
    
    /* Decorative orbs */
    .orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.55;
      pointer-events: none;
    }}
    
    .orb-1 {{
      top: 10%;
      left: 8%;
      width: 360px;
      height: 360px;
      background: radial-gradient(circle, var(--accent-acid), transparent 70%);
    }}
    
    .orb-2 {{
      bottom: 8%;
      right: 6%;
      width: 520px;
      height: 520px;
      background: radial-gradient(circle, #4b0082, transparent 70%);
    }}
    
    .orb-3 {{
      top: 62%;
      left: 52%;
      width: 220px;
      height: 220px;
      background: radial-gradient(circle, #001f3f, transparent 70%);
    }}
    
    /* Glassmorphism */
    .glass {{
      background: rgba(255, 255, 255, 0.02);
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 48px;
    }}
    
    h1, h2, h3 {{
      font-family: var(--font-head);
    }}
    
    .title-slide h1 {{
      font-size: 6rem;
      font-weight: 900;
      text-transform: uppercase;
      color: var(--text-main);
      text-align: center;
      position: relative;
      z-index: 3;
    }}
    
    .glitch-layer {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }}
    
    .glitch-green {{
      color: var(--accent-acid);
      z-index: 1;
      transform: translate3d(-4px, 0, 0);
      opacity: 0.9;
      mix-blend-mode: screen;
    }}
    
    .glitch-red {{
      color: var(--accent-red);
      z-index: 2;
      transform: translate3d(4px, 0, 0);
      opacity: 0.9;
      mix-blend-mode: screen;
    }}
    
    .index-slide {{
      text-align: center;
    }}
    
    .index-slide .bg-title {{
      position: absolute;
      font-size: 120px;
      color: rgba(255, 255, 255, 0.05);
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      z-index: 0;
    }}
    
    .index-slide ul {{
      list-style: none;
      position: relative;
      z-index: 10;
    }}
    
    .index-slide li {{
      font-size: 3rem;
      font-weight: 900;
      color: var(--text-main);
      margin: 18px 0;
    }}
    
    .content-slide h2 {{
      font-size: 3rem;
      font-weight: 900;
      color: var(--accent-acid);
      text-transform: uppercase;
      margin-bottom: 24px;
      text-shadow: 0 0 30px rgba(204, 255, 0, 0.4);
    }}
    
    .content-slide p {{
      font-size: 1.2rem;
      line-height: 2;
      color: var(--text-main);
      margin-bottom: 24px;
      opacity: 0.95;
    }}
    
    .content-slide .highlight {{
      background: rgba(204, 255, 0, 0.03);
      border-left: 4px solid rgba(204, 255, 0, 0.3);
      padding: 24px 32px;
      margin: 32px 0;
      border-radius: 16px;
      font-size: 1.4rem;
      font-weight: 600;
      color: var(--accent-acid);
      font-style: italic;
      text-align: center;
    }}
    
    .content-slide a {{
      color: var(--accent-acid);
      text-decoration: none;
      font-weight: 700;
      display: inline-block;
      margin: 12px 0;
    }}
    
    .content-slide ul {{
      list-style: none;
      margin: 24px 0;
    }}
    
    .content-slide ul li {{
      border-left: 4px solid rgba(255, 255, 255, 0.2);
      padding-left: 16px;
      margin: 16px 0;
      font-size: 1.1rem;
    }}
    
    .profile-detail {{
      text-align: center;
    }}
    
    .profile-detail img {{
      width: 200px;
      height: 200px;
      border-radius: 50%;
      object-fit: cover;
      border: 3px solid rgba(204, 255, 0, 0.3);
      margin-bottom: 24px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }}
    
    .profile-detail h2 {{
      font-size: 2.4rem;
      color: var(--accent-acid);
      margin-bottom: 32px;
    }}
    
    .profile-item {{
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding: 20px 0;
      text-align: left;
    }}
    
    .profile-label {{
      font-size: 0.9rem;
      color: rgba(255, 255, 255, 0.5);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }}
    
    .profile-value {{
      font-size: 1.2rem;
      color: var(--text-main);
    }}
    
    .quote-slide {{
      text-align: center;
    }}
    
    .quote-slide .quote-title {{
      font-size: 0.9rem;
      color: rgba(255, 255, 255, 0.5);
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 24px;
    }}
    
    .quote-slide .quote-text {{
      font-size: 2.5rem;
      font-weight: 600;
      color: var(--accent-acid);
      line-height: 1.4;
    }}
    
    .image-grid-slide h2 {{
      font-size: 3rem;
      color: var(--accent-acid);
      margin-bottom: 24px;
    }}
    
    .image-grid-slide p {{
      font-size: 1.1rem;
      color: rgba(255, 255, 255, 0.8);
      margin-bottom: 32px;
    }}
    
    .image-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-bottom: 32px;
    }}
    
    .image-grid img {{
      width: 100%;
      height: auto;
      border-radius: 16px;
      object-fit: cover;
    }}
    
    .level-cards {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
      margin-top: 32px;
    }}
    
    .level-card {{
      border-radius: 20px;
      overflow: hidden;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    
    .level-card-header {{
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem;
      font-weight: 900;
      color: var(--accent-acid);
      text-transform: uppercase;
    }}
    
    .level-card-body {{
      padding: 24px;
      background: #1a1a1a;
    }}
    
    .level-card-title {{
      font-size: 1.8rem;
      font-weight: 900;
      color: var(--accent-acid);
      text-transform: uppercase;
    }}
  </style>
</head>
<body>
  <div class="slide-container">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    {slide_content}
  </div>
</body>
</html>"""
    
    def render_slide(slide):
        slide_type = slide.get('type', 'content')
        
        if slide_type == 'title':
            return f"""
    <div class="title-slide">
      <h1>{slide.get('title', '')}</h1>
      <h2 style="font-family: var(--font-ui); font-size: 1.5rem; font-weight: 300; color: var(--text-main); margin-top: 24px; letter-spacing: 0.05em;">{slide.get('subtitle', '')}</h2>
    </div>"""
        
        elif slide_type == 'index':
            items_html = ''.join([f'<li>{item}</li>' for item in slide.get('items', [])])
            return f"""
    <div class="index-slide glass" style="max-width: 800px; width: 100%;">
      <ul>{items_html}</ul>
    </div>"""
        
        elif slide_type == 'content':
            body_html = f'<p>{slide.get("body", "")}</p>' if slide.get('body') else ''
            items_html = ''
            if slide.get('items'):
                items_html = '<ul>' + ''.join([f'<li>{item}</li>' for item in slide['items']]) + '</ul>'
            links_html = ''
            if slide.get('links'):
                links_html = '<div>' + ''.join([f'<a href="{link["url"]}" target="_blank">{link["text"]}</a>' for link in slide['links']]) + '</div>'
            highlight_html = f'<div class="highlight">{slide.get("highlight", "")}</div>' if slide.get('highlight') else ''
            subtitle_html = f'<h3 style="font-size: 1.5rem; color: var(--text-main); margin-bottom: 24px;">{slide.get("subtitle", "")}</h3>' if slide.get('subtitle') else ''
            
            return f"""
    <div class="content-slide glass" style="max-width: 900px; width: 100%;">
      <h2>{slide.get('title', '')}</h2>
      {subtitle_html}
      {body_html}
      {items_html}
      {links_html}
      {highlight_html}
    </div>"""
        
        elif slide_type == 'profile':
            subtitle_html = f'<h3 style="font-size: 1.5rem; color: var(--text-main); margin-bottom: 24px;">{slide.get("subtitle", "")}</h3>' if slide.get('subtitle') else ''
            body_html = f'<p>{slide.get("body", "")}</p>' if slide.get('body') else ''
            highlight_html = f'<div style="font-size: 1.5rem; color: var(--accent-acid); margin-top: 24px;">{slide.get("highlight", "")}</div>' if slide.get('highlight') else ''
            
            return f"""
    <div class="content-slide glass" style="max-width: 900px; width: 100%;">
      <h2>{slide.get('title', '')}</h2>
      {subtitle_html}
      {body_html}
      {highlight_html}
    </div>"""
        
        elif slide_type == 'profile-detail':
            items_html = ''
            if slide.get('items'):
                for item in slide['items']:
                    parts = item.split(': ', 1)
                    if len(parts) == 2:
                        label, value = parts
                        items_html += f'''
        <div class="profile-item">
          <div class="profile-label">{label}</div>
          <div class="profile-value">{value}</div>
        </div>'''
            links_html = ''
            if slide.get('links'):
                links_html = '<div style="margin-top: 24px;">' + ''.join([f'<a href="{link["url"]}" target="_blank">{link["text"]}</a>' for link in slide['links']]) + '</div>'
            
            return f"""
    <div class="profile-detail glass" style="max-width: 600px; width: 100%;">
      <img src="deantrbl-profile.webp" alt="딘(Dean) 프로필" onerror="this.style.display='none'">
      <h2>{slide.get('title', '')}</h2>
      {items_html}
      {links_html}
    </div>"""
        
        elif slide_type == 'quote':
            return f"""
    <div class="quote-slide glass" style="max-width: 800px; width: 100%;">
      <div class="quote-title">{slide.get('title', '')}</div>
      <div class="quote-text">{slide.get('highlight', '')}</div>
    </div>"""
        
        elif slide_type == 'image-grid':
            body_html = f'<p>{slide.get("body", "")}</p>' if slide.get('body') else ''
            
            # Project Strategy images
            images_html = '<div class="image-grid">'
            for i in range(1, 6):
                images_html += f'<img src="project-strategy-{i}.jpeg" alt="Project Strategy {i}" onerror="this.style.display=\'none\'">'
            images_html += '</div>'
            
            # Level cards
            level_cards_html = ''
            if slide.get('items'):
                gradients = [
                    'background: linear-gradient(135deg, rgba(139,69,19,0.6), rgba(75,0,130,0.6));',
                    'background: linear-gradient(135deg, rgba(70,130,180,0.6), rgba(176,196,222,0.6));',
                    'background: linear-gradient(135deg, rgba(139,69,19,0.6), rgba(160,82,45,0.6));',
                    'background: linear-gradient(135deg, rgba(25,25,112,0.6), rgba(70,130,180,0.6));'
                ]
                level_cards_html = '<div class="level-cards">'
                for idx, item in enumerate(slide['items']):
                    grad = gradients[idx] if idx < len(gradients) else 'background: #222;'
                    level_cards_html += f'''
        <div class="level-card">
          <div class="level-card-header" style="{grad}">{item}</div>
          <div class="level-card-body">
            <div class="level-card-title">{item}</div>
          </div>
        </div>'''
                level_cards_html += '</div>'
            
            return f"""
    <div class="image-grid-slide glass" style="max-width: 1000px; width: 100%; max-height: 90vh; overflow-y: auto;">
      <h2>{slide.get('title', '')}</h2>
      {body_html}
      {images_html}
      {level_cards_html}
    </div>"""
        
        return ''
    
    return html_template.format(slide_content=render_slide(slides_data[0]))

def generate_pdf():
    """PDF 생성 함수"""
    try:
        from playwright.sync_api import sync_playwright
        from PyPDF2 import PdfMerger, PdfReader, PdfWriter
    except ImportError:
        print("❌ 라이브러리를 불러올 수 없습니다. 다시 시도해주세요.")
        return False
    
    print("🚀 PDF 생성 시작...")
    
    script_dir = Path(__file__).parent
    pdf_file = script_dir / "XR_Concert_Presentation.pdf"
    temp_dir = script_dir / "temp_pdf_parts"
    
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # 슬라이드 데이터
    slides_data = [
        {'id': 1, 'type': 'title', 'title': 'XR CONCERT', 'subtitle': 'Unreal Engine Project'},
        {'id': 2, 'type': 'index', 'items': ['1. Purpose', '2. Project Strategy', '3. Artist', '4. Levels']},
        {'id': 3, 'type': 'content', 'title': 'PURPOSE', 'subtitle': '언리얼엔진으로 구현하는 XR콘서트의 목적', 'body': '언리얼엔진은 사진처럼 사실적인 고품질 그래픽을 실시간으로 구현할 수 있는 게임 엔진 프로그램이다. 따라서 XR콘서트에서 언리얼엔진을 사용하는 목적과 이유는 사실적인 공간을 재현하는 무대를 구성하며, 현실과 가상을 넘나들기 위함일 것이다.', 'highlight': "그렇다면 언리얼 환경에서 단상이 있는 XR 콘서트를 구현할 필요가 있는가? 'X'라고 생각한다. 그 이유는 크게 두가지가 있다."},
        {'id': 4, 'type': 'content', 'title': '첫번째', 'body': "리얼 타임으로 구현을 한다고 가정을 했을 때, 현재는 ICVFX, 즉 IN-Camera VFX 방식을 사용한 콘서트가 대다수이다 (이마저도 유튜브에 'XR콘서트'라고 검색어를 치면 참고할만한 자료가 3년 전.). 근데 이 ICVFX 스튜디오는 이미 LED 스크린으로 구성된 바닥과 벽이 이미 단상처럼 구성되어있다. 심지어 메인 조명도 언리얼 환경이 아닌 실제 환경에서 컨트롤 한다.", 'highlight': 'ICVFX 방식을 고려했을 때, 무대의 형태에 제한을 두지 않는 것이 효과적이다.'},
        {'id': 5, 'type': 'content', 'title': '두번째', 'body': "XR콘서트의 콘텐츠를 제공할 때, 대부분의 소비자들은 헤드마운트와 같은 기기를 사용할 것이다. 이를 보았을 때, 콘텐츠를 소비하는 사람들은 '과연 현실에 있는 무대를 원할까?' 아니면 '현실에서 느낄 수 없는 다른 차원의 것을 원할까?' 이를 고민해보았을 때, 역시나 후자가 더 많을 것이다.", 'highlight': "대중들은 현실에서 느낄 수 없는 다양한 경험을 원한다."},
        {'id': 6, 'type': 'content', 'title': 'PROJECT STRATEGY', 'body': '그렇기 때문에, 현실에서 만들어낼 수 없는 (혹은 실제 환경에서 표현하기 어려운) 요소와 구성을 넣는 것이 필요하다고 생각했다.', 'links': [{'text': '참고 자료 보기 →', 'url': 'https://www.instagram.com/p/DFCkAR1ytkA/'}, {'text': 'Rolling Stone Korea 기사 보기 →', 'url': 'https://rollingstone.co.kr/main/$/21209'}], 'highlight': '그래서 프로젝트 안에 여러 개의 컨셉적인 테마를 가진 각각의 레벨을 제작을 하였다. 이는 하나의 스튜디오에 여러개의 세트장이 있는 것과 같은 효과를 낼 수 있다.'},
        {'id': 7, 'type': 'profile-combined', 'title': 'ARTIST', 'subtitle': '아티스트 소개 및 콘서트 로그라인', 'body': '아티스트에 대한 조사를 한 뒤, 아티스트의 컨셉과 어울리는 콘서트 제작을 계획하였다.', 'profile_name': '딘(Dean)', 'items': ['GENRE: Alternative RnB, Future RnB', 'CONCEPT: Distopia / 신비주의 / 도시적인 / 몽환 <1984>', '그 외 특징: 인스타 계정 이름도 뒤에 trbl(Trouble)을 붙이며, 특유의 우울함을 추구'], 'links': [{'text': 'Instagram 프로필 보기 →', 'url': 'https://www.instagram.com/deantrbl/'}]},
        {'id': 8, 'type': 'quote', 'title': '콘서트 로그라인', 'highlight': '"무너져가는 디스토피아에서<br><br>불안정함을 노래하다."'},
        {'id': 10, 'type': 'image-grid', 'title': '4. Levels', 'body': '노래에 어울리는 컨셉과 관련된 내용으로 레벨을 제작하였다.', 'items': [
            {"name": "Howlin' 404", "desc": "디스토피아적인 공간에서 판타지적인 느낌과 약간의 그로테스크한 색감을 가져갔다."},
            {"name": "NASA", "desc": "페허가 된 도시적인 공간에 눈이 내리는 감성적인 디스토피아 세계관을 제작하였다."},
            {"name": "Bonnie & Clyde", "desc": "무너져가는 건물을 두 개의 층으로 나눠 윗층을 빈티지적인, 아무도 드나들지 않은 페허가 된 공간으로 구성하였다."},
            {"name": "Nocturne 07", "desc": "3번째의 레벨과 같은 건물의 마지막 공간으로, 아래층을 차가운 분위기의 수영장으로 구성하였다."}
        ]}
    ]
    
    # HTML 템플릿 (위의 generate_presentation_html 함수와 동일)
    html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>XR Concert Presentation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@300;500;800&family=Noto+Sans+KR:wght@300;500;700;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-color: #050505;
      --text-main: #ffffff;
      --accent-acid: #CCFF00;
      --accent-red: #ff3b3b;
      --font-head: 'Archivo Black', sans-serif;
      --font-ui: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;
    }}
    
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    
    body {{
      background: var(--bg-color) !important;
      background-color: var(--bg-color) !important;
      color: var(--text-main) !important;
      font-family: var(--font-ui);
      -webkit-font-smoothing: antialiased;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    }}
    
    .slide-container {{
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 60px;
      position: relative;
      background: var(--bg-color) !important;
      background-color: var(--bg-color) !important;
    }}
    
    .orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.55;
      pointer-events: none;
    }}
    
    .orb-1 {{
      top: 10%;
      left: 8%;
      width: 360px;
      height: 360px;
      background: radial-gradient(circle, var(--accent-acid), transparent 70%);
    }}
    
    .orb-2 {{
      bottom: 8%;
      right: 6%;
      width: 520px;
      height: 520px;
      background: radial-gradient(circle, #4b0082, transparent 70%);
    }}
    
    .orb-3 {{
      top: 62%;
      left: 52%;
      width: 220px;
      height: 220px;
      background: radial-gradient(circle, #001f3f, transparent 70%);
    }}
    
    .glass {{
      background: rgba(255, 255, 255, 0.02) !important;
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 48px;
    }}
    
    h1, h2, h3 {{
      font-family: var(--font-head) !important;
      color: var(--text-main) !important;
    }}
    
    .title-slide {{
      text-align: center;
    }}
    
    .title-slide h1 {{
      font-size: 6rem !important;
      font-weight: 900 !important;
      text-transform: uppercase !important;
      color: var(--text-main) !important;
      position: relative;
      z-index: 3;
    }}
    
    .glitch-layer {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      font-size: 6rem !important;
      font-weight: 900 !important;
      text-transform: uppercase !important;
    }}
    
    .glitch-green {{
      color: var(--accent-acid) !important;
      z-index: 1;
      transform: translate3d(-4px, 0, 0);
      opacity: 0.9;
      mix-blend-mode: screen;
    }}
    
    .glitch-red {{
      color: var(--accent-red) !important;
      z-index: 2;
      transform: translate3d(4px, 0, 0);
      opacity: 0.9;
      mix-blend-mode: screen;
    }}
    
    .index-slide {{
      text-align: center;
      max-width: 800px;
      width: 100%;
    }}
    
    .index-slide .bg-title {{
      position: absolute;
      font-size: 120px;
      color: rgba(255, 255, 255, 0.05) !important;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      z-index: 0;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }}
    
    .index-slide ul {{
      list-style: none;
      position: relative;
      z-index: 10;
    }}
    
    .index-slide li {{
      font-size: 3rem !important;
      font-weight: 900 !important;
      color: var(--text-main) !important;
      margin: 18px 0;
      font-family: var(--font-head) !important;
    }}
    
    .content-slide h2 {{
      font-size: 3rem !important;
      font-weight: 900 !important;
      color: var(--accent-acid) !important;
      text-transform: uppercase !important;
      margin-bottom: 24px;
      text-shadow: 0 0 30px rgba(204, 255, 0, 0.4);
    }}
    
    .content-slide p {{
      font-size: 1.2rem !important;
      line-height: 2 !important;
      color: var(--text-main) !important;
      margin-bottom: 24px;
      opacity: 0.95;
    }}
    
    .content-slide .highlight {{
      background: rgba(204, 255, 0, 0.03) !important;
      border-left: 4px solid rgba(204, 255, 0, 0.3) !important;
      padding: 24px 32px;
      margin: 32px 0;
      border-radius: 16px;
      font-size: 1.4rem !important;
      font-weight: 600 !important;
      color: var(--accent-acid) !important;
      font-style: italic;
      text-align: center;
    }}
    
    .content-slide a {{
      color: var(--accent-acid) !important;
      text-decoration: none;
      font-weight: 700;
      display: inline-block;
      margin: 12px 0;
    }}
    
    .content-slide ul {{
      list-style: none;
      margin: 24px 0;
    }}
    
    .content-slide ul li {{
      border-left: 4px solid rgba(255, 255, 255, 0.2);
      padding-left: 16px;
      margin: 16px 0;
      font-size: 1.1rem !important;
      color: var(--text-main) !important;
    }}
    
    .profile-detail {{
      text-align: center;
      max-width: 600px;
      width: 100%;
    }}
    
    .profile-detail img {{
      width: 200px;
      height: 200px;
      border-radius: 50%;
      object-fit: cover;
      border: 3px solid rgba(204, 255, 0, 0.3);
      margin-bottom: 24px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }}
    
    .profile-detail h2 {{
      font-size: 2.4rem !important;
      color: var(--accent-acid) !important;
      margin-bottom: 32px;
    }}
    
    .profile-item {{
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding: 20px 0;
      text-align: left;
    }}
    
    .profile-label {{
      font-size: 0.9rem !important;
      color: rgba(255, 255, 255, 0.5) !important;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }}
    
    .profile-value {{
      font-size: 1.2rem !important;
      color: var(--text-main) !important;
    }}
    
    .quote-slide {{
      text-align: center;
      max-width: 800px;
      width: 100%;
    }}
    
    .quote-slide .quote-title {{
      font-size: 0.9rem !important;
      color: rgba(255, 255, 255, 0.5) !important;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 24px;
    }}
    
    .quote-slide .quote-text {{
      font-size: 2.5rem !important;
      font-weight: 600 !important;
      color: var(--accent-acid) !important;
      line-height: 1.4;
    }}
    
    .image-grid-slide h2 {{
      font-size: 3rem !important;
      color: var(--accent-acid) !important;
      margin-bottom: 24px;
    }}
    
    .image-grid-slide p {{
      font-size: 1.1rem !important;
      color: rgba(255, 255, 255, 0.8) !important;
      margin-bottom: 32px;
    }}
    
    .image-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-bottom: 32px;
    }}
    
    .image-grid img {{
      width: 100%;
      height: auto;
      border-radius: 16px;
      object-fit: cover;
    }}
    
    .level-cards {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
      margin-top: 32px;
    }}
    
    .level-card {{
      border-radius: 20px;
      overflow: hidden;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    
    .level-card-header {{
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem !important;
      font-weight: 900 !important;
      color: var(--accent-acid) !important;
      text-transform: uppercase;
      font-family: var(--font-head) !important;
    }}
    
    .level-card-body {{
      padding: 24px;
      background: #1a1a1a;
    }}
    
    .level-card-title {{
      font-size: 1.8rem !important;
      font-weight: 900 !important;
      color: var(--accent-acid) !important;
      text-transform: uppercase;
      font-family: var(--font-head) !important;
    }}
  </style>
</head>
<body>
  <div class="slide-container">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    {slide_content}
  </div>
</body>
</html>"""
    
    def render_slide(slide):
        slide_type = slide.get('type', 'content')
        
        if slide_type == 'title':
            return f"""
    <div class="title-slide">
      <h1>{slide.get('title', '')}</h1>
      <h2 style="font-family: var(--font-ui); font-size: 1.5rem; font-weight: 300; color: var(--text-main); margin-top: 24px; letter-spacing: 0.05em;">{slide.get('subtitle', '')}</h2>
    </div>"""
        
        elif slide_type == 'index':
            items_html = ''.join([f'<li>{item}</li>' for item in slide.get('items', [])])
            return f"""
    <div class="index-slide glass">
      <ul>{items_html}</ul>
    </div>"""
        
        elif slide_type == 'content':
            body_html = f'<p>{slide.get("body", "")}</p>' if slide.get('body') else ''
            items_html = ''
            if slide.get('items'):
                items_html = '<ul>' + ''.join([f'<li>{item}</li>' for item in slide['items']]) + '</ul>'
            links_html = ''
            if slide.get('links'):
                # Special handling for slide 6 - separate links with spacing
                if slide.get('id') == 6:
                    links_html = '<div>' + ''.join([f'<div style="margin-bottom: 12px;"><a href="{link["url"]}" target="_blank">{link["text"]}</a></div>' for link in slide['links']]) + '</div>'
                else:
                    links_html = '<div>' + ''.join([f'<a href="{link["url"]}" target="_blank">{link["text"]}</a>' for link in slide['links']]) + '</div>'
            
            # Special handling for slide 3 (PURPOSE) - split highlight into question and answer
            highlight_html = ''
            if slide.get('highlight'):
                highlight_text = slide.get('highlight', '')
                # Check if this is slide 3 (PURPOSE) with the question
                if slide.get('id') == 3 and '그렇다면 언리얼 환경에서 단상이 있는 XR 콘서트를 구현할 필요가 있는가?' in highlight_text:
                    # Split into question and answer
                    parts = highlight_text.split("'X'라고 생각한다.")
                    question = parts[0].strip()
                    answer = "'X'라고 생각한다." + (parts[1] if len(parts) > 1 else '')
                    highlight_html = f'''
      <div class="highlight" style="font-size: 1.8rem !important; color: var(--accent-acid) !important; font-weight: 700 !important; margin-bottom: 24px;">
        {question}
      </div>
      <div class="highlight">
        {answer}
      </div>'''
                # Special handling for slide 6 (PROJECT STRATEGY) - split highlight with white text for second part
                elif slide.get('id') == 6 and '이는 하나의 스튜디오에' in highlight_text:
                    # Split into two parts
                    parts = highlight_text.split('이는 하나의 스튜디오에')
                    first_part = parts[0].strip()
                    second_part = '이는 하나의 스튜디오에' + (parts[1] if len(parts) > 1 else '')
                    highlight_html = f'''
      <div class="highlight">
        <span style="color: var(--accent-acid) !important;">{first_part}</span><br><br>
        <span style="color: var(--text-main) !important;">{second_part}</span>
      </div>'''
                else:
                    highlight_html = f'<div class="highlight">{highlight_text}</div>'
            
            subtitle_html = f'<h3 style="font-size: 1.5rem; color: var(--text-main); margin-bottom: 24px;">{slide.get("subtitle", "")}</h3>' if slide.get('subtitle') else ''
            
            # Special handling for slide 6 - add image grid
            images_html = ''
            if slide.get('id') == 6:
                images_html = '''
      <div class="image-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 24px 0;">
        <img src="project-strategy-1.jpeg" alt="Project Strategy 1" style="width: 100%; height: auto; border-radius: 16px; object-fit: cover;" onerror="this.style.display=\'none\'">
        <img src="project-strategy-2.jpeg" alt="Project Strategy 2" style="width: 100%; height: auto; border-radius: 16px; object-fit: cover;" onerror="this.style.display=\'none\'">
        <img src="project-strategy-3.jpeg" alt="Project Strategy 3" style="width: 100%; height: auto; border-radius: 16px; object-fit: cover;" onerror="this.style.display=\'none\'">
        <img src="project-strategy-4.jpeg" alt="Project Strategy 4" style="width: 100%; height: auto; border-radius: 16px; object-fit: cover;" onerror="this.style.display=\'none\'">
        <img src="project-strategy-5.jpeg" alt="Project Strategy 5" style="width: 100%; height: auto; border-radius: 16px; object-fit: cover; grid-column: 1 / -1; max-width: 50%; margin: 16px auto 0;" onerror="this.style.display=\'none\'">
      </div>'''
            
            return f"""
    <div class="content-slide glass" style="max-width: 900px; width: 100%;">
      <h2>{slide.get('title', '')}</h2>
      {subtitle_html}
      {body_html}
      {items_html}
      {links_html}
      {images_html}
      {highlight_html}
    </div>"""
        
        elif slide_type == 'profile':
            subtitle_html = f'<h3 style="font-size: 1.5rem; color: var(--text-main); margin-bottom: 24px;">{slide.get("subtitle", "")}</h3>' if slide.get('subtitle') else ''
            body_html = f'<p>{slide.get("body", "")}</p>' if slide.get('body') else ''
            highlight_html = f'<div style="font-size: 1.5rem; color: var(--accent-acid); margin-top: 24px;">{slide.get("highlight", "")}</div>' if slide.get('highlight') else ''
            
            return f"""
    <div class="content-slide glass" style="max-width: 900px; width: 100%;">
      <h2>{slide.get('title', '')}</h2>
      {subtitle_html}
      {body_html}
      {highlight_html}
    </div>"""
        
        elif slide_type == 'profile-combined':
            subtitle_html = f'<h3 style="font-size: 1.5rem; color: var(--text-main); margin-bottom: 24px;">{slide.get("subtitle", "")}</h3>' if slide.get('subtitle') else ''
            body_html = f'<p>{slide.get("body", "")}</p>' if slide.get('body') else ''
            
            # Profile image and name
            profile_name = slide.get('profile_name', '')
            profile_image_html = f'''
      <div style="text-align: center; margin: 32px 0;">
        <img src="deantrbl-profile.webp" alt="딘(Dean) 프로필" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; border: 3px solid rgba(204, 255, 0, 0.3); margin-bottom: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);" onerror="this.style.display='none'">
        <h3 style="font-size: 2.4rem; color: var(--accent-acid); font-weight: 700; text-shadow: 0 0 20px rgba(204, 255, 0, 0.4); font-family: var(--font-head);">{profile_name}</h3>
      </div>'''
            
            # Profile items
            items_html = ''
            if slide.get('items'):
                for item in slide['items']:
                    parts = item.split(': ', 1)
                    if len(parts) == 2:
                        label, value = parts
                        items_html += f'''
        <div class="profile-item" style="border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding: 20px 0; text-align: left;">
          <div class="profile-label" style="font-size: 0.9rem !important; color: rgba(255, 255, 255, 0.5) !important; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">{label}</div>
          <div class="profile-value" style="font-size: 1.2rem !important; color: var(--text-main) !important;">{value}</div>
        </div>'''
            
            # Links
            links_html = ''
            if slide.get('links'):
                links_html = '<div style="margin-top: 24px;">' + ''.join([f'<a href="{link["url"]}" target="_blank" style="color: var(--accent-acid) !important; text-decoration: none; font-weight: 700; display: inline-block; margin: 12px 0;">{link["text"]}</a>' for link in slide['links']]) + '</div>'
            
            return f"""
    <div class="content-slide glass" style="max-width: 900px; width: 100%; max-height: 90vh; overflow-y: auto;">
      <h2>{slide.get('title', '')}</h2>
      {subtitle_html}
      {body_html}
      {profile_image_html}
      <div style="margin-top: 32px;">
        {items_html}
        {links_html}
      </div>
    </div>"""
        
        elif slide_type == 'profile-detail':
            items_html = ''
            if slide.get('items'):
                for item in slide['items']:
                    parts = item.split(': ', 1)
                    if len(parts) == 2:
                        label, value = parts
                        items_html += f'''
        <div class="profile-item">
          <div class="profile-label">{label}</div>
          <div class="profile-value">{value}</div>
        </div>'''
            links_html = ''
            if slide.get('links'):
                links_html = '<div style="margin-top: 24px;">' + ''.join([f'<a href="{link["url"]}" target="_blank">{link["text"]}</a>' for link in slide['links']]) + '</div>'
            
            return f"""
    <div class="profile-detail glass">
      <img src="deantrbl-profile.webp" alt="딘(Dean) 프로필" onerror="this.style.display='none'">
      <h2>{slide.get('title', '')}</h2>
      {items_html}
      {links_html}
    </div>"""
        
        elif slide_type == 'quote':
            return f"""
    <div class="quote-slide glass">
      <div class="quote-title">{slide.get('title', '')}</div>
      <div class="quote-text">{slide.get('highlight', '')}</div>
    </div>"""
        
        elif slide_type == 'image-grid':
            body_html = f'<p>{slide.get("body", "")}</p>' if slide.get('body') else ''
            
            images_html = '<div class="image-grid">'
            for i in range(1, 6):
                images_html += f'<img src="project-strategy-{i}.jpeg" alt="Project Strategy {i}" onerror="this.style.display=\'none\'">'
            images_html += '</div>'
            
            level_cards_html = ''
            if slide.get('items'):
                gradients = [
                    'background: linear-gradient(135deg, rgba(139,69,19,0.6), rgba(75,0,130,0.6));',
                    'background: linear-gradient(135deg, rgba(70,130,180,0.6), rgba(176,196,222,0.6));',
                    'background: linear-gradient(135deg, rgba(139,69,19,0.6), rgba(160,82,45,0.6));',
                    'background: linear-gradient(135deg, rgba(25,25,112,0.6), rgba(70,130,180,0.6));'
                ]
                level_cards_html = '<div class="level-cards">'
                for idx, item in enumerate(slide['items']):
                    grad = gradients[idx] if idx < len(gradients) else 'background: #222;'
                    # item이 딕셔너리인지 문자열인지 확인
                    if isinstance(item, dict):
                        item_name = item.get('name', '')
                        item_desc = item.get('desc', '')
                    else:
                        item_name = item
                        item_desc = ''
                    
                    # 제목을 헤더로 이동, 본문에는 설명만
                    level_cards_html += f'''
        <div class="level-card">
          <div class="level-card-header" style="{grad}; text-align: center !important; display: flex; align-items: center; justify-content: center; color: var(--accent-acid) !important; font-size: 2rem !important; font-weight: 700 !important;">{item_name}</div>
          <div class="level-card-body">
            {f'<div class="level-card-desc" style="font-size: 1rem !important; color: rgba(255, 255, 255, 0.8) !important; margin-bottom: 16px; line-height: 1.6; text-align: left;">{item_desc}</div>' if item_desc else ''}
          </div>
        </div>'''
                level_cards_html += '</div>'
            
            return f"""
    <div class="image-grid-slide glass" style="max-width: 1000px; width: 100%; max-height: 90vh; overflow-y: auto;">
      <h2>{slide.get('title', '')}</h2>
      {body_html}
      {images_html}
      {level_cards_html}
    </div>"""
        
        return ''
    
    with sync_playwright() as p:
        print("🌐 브라우저 시작 중...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
            color_scheme="dark"
        )
        page = context.new_page()
        
        pdf_parts = []
        
        for idx, slide in enumerate(slides_data):
            print(f"📄 슬라이드 {idx + 1}/{len(slides_data)} 생성 중...")
            
            html_content = html_template.format(slide_content=render_slide(slide))
            
            # 임시 HTML 파일 생성
            temp_html = temp_dir / f"slide_{idx + 1}.html"
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            file_url = f"file://{temp_html.absolute()}"
            page.goto(file_url, wait_until="domcontentloaded", timeout=30000)
            
            # 이미지 로드 대기
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            
            # 이미지 로드 확인
            page.evaluate("""
                () => {
                    return Promise.all(
                        Array.from(document.images).map(img => {
                            if (img.complete) return Promise.resolve();
                            return new Promise((resolve, reject) => {
                                img.onload = resolve;
                                img.onerror = resolve;
                                setTimeout(resolve, 3000);
                            });
                        })
                    );
                }
            """)
            page.wait_for_timeout(1000)
            
            slide_pdf = temp_dir / f"slide_{idx + 1}.pdf"
            page.pdf(
                path=str(slide_pdf),
                format="A4",
                print_background=True,
                margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
                prefer_css_page_size=False
            )
            pdf_parts.append(slide_pdf)
        
        browser.close()
        
        # PDF 병합
        print("📚 PDF 파일 합치는 중...")
        merger = PdfMerger()
        
        for pdf_path in pdf_parts:
            if pdf_path.exists() and pdf_path.stat().st_size > 0:
                try:
                    reader = PdfReader(str(pdf_path))
                    if len(reader.pages) > 0:
                        merger.append(str(pdf_path))
                        print(f"   ✅ {pdf_path.name} 추가됨")
                except Exception as e:
                    print(f"⚠️ {pdf_path.name} 병합 중 오류: {e}")
        
        merger.write(str(pdf_file))
        merger.close()
        
        # 임시 파일 삭제
        for pdf_path in pdf_parts:
            if pdf_path.exists():
                pdf_path.unlink()
        for html_file in temp_dir.glob("*.html"):
            if html_file.exists():
                html_file.unlink()
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
        
        if pdf_file.exists():
            size_mb = pdf_file.stat().st_size / 1024 / 1024
            print(f"✅ PDF 생성 완료: {pdf_file}")
            print(f"📊 파일 크기: {size_mb:.2f} MB")
            print(f"📄 총 {len(slides_data)}개 슬라이드")
            return True
        else:
            print("❌ PDF 파일이 생성되지 않았습니다.")
            return False

if __name__ == "__main__":
    print("=" * 50)
    print("XR Concert Presentation PDF 생성기")
    print("=" * 50)
    
    if check_and_install_dependencies():
        success = generate_pdf()
        if success:
            print("\n🎉 완료!")
            sys.exit(0)
        else:
            print("\n❌ PDF 생성 실패")
            sys.exit(1)
    else:
        print("\n❌ 의존성 설치 실패")
        sys.exit(1)

