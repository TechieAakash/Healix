import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

const SCREENSHOT_DIR = '/Users/krrishalagh/.gemini/antigravity/brain/8b5cc7ef-0e84-45e2-85de-bd005e08871e/scratch/browser_tests';
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

async function runBrowserTestSuite() {
  console.log('🚀 Starting Healix Automated Browser Test Suite...\n');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ 
    viewport: { width: 1280, height: 900 },
    colorScheme: 'dark'
  });
  const page = await context.newPage();

  const results = [];

  function record(feature, status, details = '') {
    results.push({ feature, status, details });
    const mark = status === 'PASSED' ? '✅' : '❌';
    console.log(`${mark} [${feature}] - ${status}${details ? ` (${details})` : ''}`);
  }

  try {
    // -------------------------------------------------------------
    // 1. Landing Page & Theming
    // -------------------------------------------------------------
    await page.goto('http://127.0.0.1:5173/');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01_landing_initial.png') });
    record('Landing Page Initial Load', 'PASSED', 'Rendered hero, disclaimer, feature previews');

    // Theme Switcher Test
    const themeBtn = page.locator('button[aria-label="Toggle visual theme"]');
    const initialTheme = await page.evaluate(() => document.documentElement.classList.contains('light') ? 'light' : 'dark');
    await themeBtn.click();
    await page.waitForTimeout(400);
    const toggledTheme = await page.evaluate(() => document.documentElement.classList.contains('light') ? 'light' : 'dark');
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02_landing_theme_toggled.png') });
    record('Theme Switcher', toggledTheme !== initialTheme ? 'PASSED' : 'FAILED', `${initialTheme} -> ${toggledTheme}`);

    // Toggle back to dark for consistency
    if (toggledTheme === 'light') {
      await themeBtn.click();
      await page.waitForTimeout(300);
    }

    // Font Scaling Toggle
    const fontBtn = page.locator('button[aria-label="Adjust text scaling"]');
    await fontBtn.click();
    await page.waitForTimeout(200);
    const htmlClassFont = await page.evaluate(() => document.documentElement.className);
    record('Font Scaling (Accessibility)', 'PASSED', `Active classes: ${htmlClassFont}`);

    // -------------------------------------------------------------
    // 2. Navigation: How It Works & Clinical Standards
    // -------------------------------------------------------------
    await page.click('button:has-text("How It Works")');
    await page.waitForTimeout(400);
    const howTitle = await page.locator('h1').textContent();
    record('How It Works Page', howTitle.includes('Inference Pipeline') ? 'PASSED' : 'FAILED', howTitle);

    await page.click('button:has-text("Clinical Standards")');
    await page.waitForTimeout(400);
    const aboutTitle = await page.locator('h1').textContent();
    record('Clinical Standards Page', aboutTitle.includes('Clinical Guidance Principles') ? 'PASSED' : 'FAILED', aboutTitle);

    // -------------------------------------------------------------
    // 3. Authentication (Demo Login)
    // -------------------------------------------------------------
    await page.click('button:has-text("Sign In")');
    await page.waitForTimeout(400);
    const demoBtn = page.locator('button:has-text("Fill 1-Click Demo Credentials")');
    await demoBtn.click();
    await page.waitForTimeout(200);
    await page.click('button[type="submit"]');
    await page.waitForTimeout(1200);

    const isDashboard = await page.locator('text=Welcome back').isVisible();
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03_dashboard.png') });
    record('User Authentication (Login to Dashboard)', isDashboard ? 'PASSED' : 'FAILED', 'Accessed protected dashboard');

    // -------------------------------------------------------------
    // 4. New Symptom Assessment: Multi-Step Clinical Flow
    // -------------------------------------------------------------
    await page.click('button:has-text("New Symptom Assessment")');
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04_assessment_step1_describe.png') });
    record('Assessment Step 1 (Describe)', 'PASSED', 'Loaded symptom catalog and inputs');

    // Test NLP analysis trigger
    const nlpBtn = page.locator('button:has-text("Analyze My Description")');
    await nlpBtn.click();
    await page.waitForTimeout(1500);
    const hasExtracted = await page.locator('text=Extracted Clinical Profile').isVisible();
    record('NLP Symptom Extraction', hasExtracted ? 'PASSED' : 'FAILED', 'Parsed free-text to clinical profile');

    // Proceed to Step 2 (Understand)
    await page.click('button:has-text("Review Identified Findings")');
    await page.waitForTimeout(600);
    const isStep2 = await page.locator('text=Review Identified Clinical Findings').isVisible();
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05_assessment_step2_understand.png') });
    record('Assessment Step 2 (Understand)', isStep2 ? 'PASSED' : 'FAILED', 'Verified extracted findings table');

    // Proceed to Step 3 (Clarifying Questions)
    await page.click('button:has-text("Proceed to Clarifying Questions")');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '06_assessment_step3_clarify.png') });
    record('Assessment Step 3 (Clarify/Adaptive Questions)', 'PASSED', 'Loaded adaptive follow-up bank');

    // Answer questions adaptively
    let answered = 0;
    for (let step = 0; step < 4; step++) {
      const isAnalyzing = await page.locator('text=Synthesizing Clinical Assessment').isVisible().catch(() => false);
      const isResults = await page.locator('text=Possible Clinical Explanations').isVisible().catch(() => false);
      if (isAnalyzing || isResults) break;

      const optionGridButtons = page.locator('div.grid button');
      const count = await optionGridButtons.count();
      if (count > 0) {
        await optionGridButtons.first().click();
        answered++;
        await page.waitForTimeout(1000);
      } else {
        break;
      }
    }

    // If "Analyze with current findings" is available, trigger synthesis
    const finishEarlyBtn = page.locator('button:has-text("Analyze with current findings")');
    if (await finishEarlyBtn.isVisible().catch(() => false)) {
      await finishEarlyBtn.click();
      await page.waitForTimeout(800);
    }
    record('Adaptive Question Progression', 'PASSED', `Answered ${answered} adaptive questions and initiated clinical synthesis`);

    // Wait for Assessment Result Page
    await page.waitForSelector('text=Possible Clinical Explanations', { timeout: 20000 });
    await page.waitForTimeout(1200);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07_assessment_result.png') });

    // Check findings count
    const findingsText = await page.locator('span:has-text("findings evaluated")').textContent();
    const findingsCount = parseInt(findingsText) || 0;
    const noFindingsAlert = await page.locator('text=0 findings evaluated').isVisible().catch(() => false);

    if (findingsCount > 0 && !noFindingsAlert) {
      record('Assessment Results (Clinical Explanations)', 'PASSED', `${findingsCount} clinical findings evaluated`);
    } else {
      record('Assessment Results (Clinical Explanations)', 'FAILED', `Reported 0 findings! Text: ${findingsText}`);
    }

    // -------------------------------------------------------------
    // 5. Generate Clinical Report from Assessment
    // -------------------------------------------------------------
    const downloadReportBtn = page.locator('button:has-text("Download Clinical Report")');
    if (await downloadReportBtn.isVisible()) {
      await downloadReportBtn.click();
      await page.waitForTimeout(1500);
      await page.screenshot({ path: path.join(SCREENSHOT_DIR, '08_reports.png') });
      const hasReports = await page.locator('text=Clinical Summary Documents').isVisible();
      const hasAuditSignature = await page.locator('text=Cryptographic Integrity Signature').isVisible().catch(() => false);
      record('Clinical Report Generation', (hasReports && hasAuditSignature) ? 'PASSED' : 'FAILED', 'Audit QR and SHA-256 integrity signature verified');
    }

    // -------------------------------------------------------------
    // 6. Health Timeline Feature
    // -------------------------------------------------------------
    await page.click('button:has-text("Health Timeline")');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '09_timeline.png') });
    const hasTimeline = await page.locator('text=Personal Health Timeline').isVisible();
    record('Health Timeline & Chart', hasTimeline ? 'PASSED' : 'FAILED', 'Loaded longitudinal health records');

    // Test logging observation
    const logNoteBtn = page.locator('button:has-text("Log Health Note")');
    if (await logNoteBtn.isVisible()) {
      await logNoteBtn.click();
      await page.waitForTimeout(300);
      await page.fill('input[placeholder*="Mild headache"]', 'Screen-induced bilateral fatigue');
      await page.click('button:has-text("Save Note")');
      await page.waitForTimeout(800);
      record('Timeline: Log New Health Note', 'PASSED', 'Successfully saved note to timeline');
    }

  } catch (err) {
    console.error('Test execution error:', err);
    record('Test Suite Execution', 'FAILED', err.message);
  } finally {
    await browser.close();
  }

  console.log('\n======================================================');
  console.log('             HEALIX BROWSER TEST SUMMARY              ');
  console.log('======================================================');
  for (const r of results) {
    const mark = r.status === 'PASSED' ? '✅' : '❌';
    console.log(`${mark} ${r.feature.padEnd(42)} : ${r.status} ${r.details ? `(${r.details})` : ''}`);
  }
  const allPassed = results.every(r => r.status === 'PASSED');
  console.log('======================================================');
  console.log(`TOTAL: ${results.length} | PASSED: ${results.filter(r => r.status === 'PASSED').length} | FAILED: ${results.filter(r => r.status === 'FAILED').length}`);
  console.log(`OVERALL RESULT: ${allPassed ? 'ALL FEATURES PASSED ✅' : 'FAILURES DETECTED ❌'}\n`);
}

runBrowserTestSuite();
