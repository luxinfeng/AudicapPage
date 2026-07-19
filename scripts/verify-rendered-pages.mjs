import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const expectedBodyClasses = new Map([
  ['docs/index.html', ['home-page']],
  ['docs/use-cases/coursera-transcription.html', ['home-page', 'seo-page']],
  ['docs/use-cases/udemy-course-transcription.html', ['home-page', 'seo-page']],
  ['docs/use-cases/canvas-lecture-transcription.html', ['home-page', 'seo-page']],
  ['docs/use-cases/medical-training-transcription.html', ['home-page', 'seo-page']],
  ['docs/use-cases/hubspot-certification-notes.html', ['home-page', 'seo-page']],
  ['docs/use-cases/interpreter-training-transcription.html', ['home-page', 'seo-page']]
]);

const failures = [];

for (const [file, expectedClasses] of expectedBodyClasses) {
  const html = readFileSync(resolve(file), 'utf8');
  const bodyMatch = html.match(/<body(?:\s+class="([^"]*)")?[^>]*>/i);
  const actualClasses = new Set((bodyMatch?.[1] ?? '').split(/\s+/).filter(Boolean));

  for (const className of expectedClasses) {
    if (!actualClasses.has(className)) {
      failures.push(`${file}: missing body class "${className}"`);
    }
  }
}

if (failures.length > 0) {
  console.error('Rendered page verification failed:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  console.log(`Verified body classes for ${expectedBodyClasses.size} rendered pages.`);
}
