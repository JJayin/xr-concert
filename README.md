https://jjayin.github.io/xr-concert/XR_1_bg.html
XR 콘서트 설명을 위한 사이트입니다.

## PDF 생성 방법

### 방법 1: 브라우저 인쇄 기능 (가장 간단)
1. 웹페이지를 브라우저에서 열기
2. `Cmd+P` (Mac) 또는 `Ctrl+P` (Windows) 누르기
3. "PDF로 저장" 선택

### 방법 2: Puppeteer 스크립트 사용
1. Node.js가 설치되어 있어야 합니다
2. 의존성 설치:
   ```bash
   npm install puppeteer
   ```
3. 스크립트 실행:
   ```bash
   node generate-pdf.js
   ```
4. 생성된 `XR_Concert.pdf` 파일 확인
