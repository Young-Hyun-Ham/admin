# React Admin Frontend

이 프로젝트는 React, TypeScript, Vite 기반의 React-Admin 프론트엔드입니다.

## 폴더 구조

```
frontend/
├── public/                # 정적 파일
├── src/                   # 소스 코드
│   ├── admin/             # react-admin 관련 파일 (dataProvider 등)
│   ├── components/        # 공통 컴포넌트
│   ├── pages/             # 페이지 컴포넌트
│   ├── App.tsx            # 앱 엔트리
│   └── main.tsx           # 진입점
├── index.html             # 메인 HTML
├── package.json           # 프로젝트 설정
├── vite.config.ts         # Vite 설정
├── tailwind.config.js     # TailwindCSS 설정
├── postcss.config.js      # PostCSS 설정
├── tsconfig.json          # TypeScript 설정
└── README.md              # 프로젝트 설명
```

## 개발 환경 설정

1. 의존성 설치
   ```bash
   npm install
   ```

2. 개발 서버 실행
   ```bash
   npm run dev
   ```
   기본 포트는 5173입니다. (vite.config.ts에서 변경 가능)

3. 빌드
   ```bash
   npm run build
   ```

4. 린트
   ```bash
   npm run lint
   ```

## 주요 라이브러리

- [react-admin](https://marmelab.com/react-admin/) : 어드민 UI 프레임워크
- [Vite](https://vitejs.dev/) : 빠른 프론트엔드 빌드 도구
- [TypeScript](https://www.typescriptlang.org/) : 타입스크립트
- [TailwindCSS](https://tailwindcss.com/) : 유틸리티 기반 CSS 프레임워크

## ESLint 확장

프로덕션 환경에서는 타입 인식 린트 규칙을 활성화하는 것이 좋습니다.

```js
export default tseslint.config([
  globalIgnores(['dist']),
])
```

React 관련 린트 플러그인:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config([
  // ...
])
```
