#!/usr/bin/env node

/**
 * XR Concert 웹페이지를 PDF로 변환하는 스크립트
 * 사용법: node generate-pdf.js
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generatePDF() {
  console.log('🚀 PDF 생성 시작...');
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // 로컬 파일 경로
  const filePath = path.join(__dirname, 'XR_1_bg.html');
  const fileUrl = `file://${filePath}`;
  
  console.log(`📄 파일 로드 중: ${fileUrl}`);
  
  await page.goto(fileUrl, {
    waitUntil: 'networkidle0',
    timeout: 60000
  });
  
  // 페이지가 완전히 로드될 때까지 대기
  await page.waitForTimeout(3000);
  
  // PDF 생성 옵션
  const pdfPath = path.join(__dirname, 'XR_Concert.pdf');
  
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '20mm',
      right: '20mm',
      bottom: '20mm',
      left: '20mm'
    },
    preferCSSPageSize: false,
    displayHeaderFooter: false
  });
  
  await browser.close();
  
  console.log(`✅ PDF 생성 완료: ${pdfPath}`);
  console.log(`📊 파일 크기: ${(fs.statSync(pdfPath).size / 1024 / 1024).toFixed(2)} MB`);
}

// 실행
generatePDF().catch(error => {
  console.error('❌ 오류 발생:', error);
  process.exit(1);
});

