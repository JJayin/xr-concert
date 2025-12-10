# XR Concert Presentation App

React/TypeScript 기반 프레젠테이션 앱입니다. HTML 디자인과 동일한 스타일을 적용했습니다.

## 설치 방법

```bash
# 프로젝트 초기화 (아직 안 했다면)
npm init -y

# React 및 TypeScript 설치
npm install react react-dom
npm install -D @types/react @types/react-dom typescript

# Lucide React 아이콘 설치
npm install lucide-react

# Tailwind CSS 설치 (스타일링용)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Tailwind 설정

`tailwind.config.js` 파일에 다음 내용 추가:

```js
module.exports = {
  content: [
    "./PresentationApp.tsx",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'head': ['Archivo Black', 'sans-serif'],
        'ui': ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        'accent': '#CCFF00',
        'accent-red': '#ff3b3b',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
```

## 사용 방법

1. `PresentationApp.tsx`를 React 프로젝트에 추가
2. 필요한 이미지 파일들이 같은 디렉토리에 있는지 확인:
   - `deantrbl-profile.webp`
   - `project-strategy-1.jpeg` ~ `project-strategy-5.jpeg`
3. 컴포넌트를 import하여 사용:

```tsx
import PresentationApp from './PresentationApp';

function App() {
  return <PresentationApp />;
}
```

## 주요 변경사항

- ✅ HTML과 동일한 색상 스키마 적용 (#050505 배경, #CCFF00 액센트)
- ✅ Archivo Black, Inter 폰트 적용
- ✅ 글래스모피즘 효과 추가
- ✅ 글리치 효과 (타이틀)
- ✅ 프로필 이미지 추가
- ✅ 프로젝트 전략 이미지 그리드 추가
- ✅ 레벨 카드 스타일링

## 키보드 단축키

- `→` 또는 `Space`: 다음 슬라이드
- `←`: 이전 슬라이드
- `F`: 전체화면 토글

