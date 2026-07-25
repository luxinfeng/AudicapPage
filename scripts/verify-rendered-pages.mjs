import { readFileSync, readdirSync } from 'node:fs';
import { relative, resolve } from 'node:path';

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
const siteOrigin = 'https://audicap.work';
const docsDirectory = resolve('docs');
const nonIndexablePaths = new Set([
  '/404.html',
  '/audicap-popup-preview.html',
  '/checkout.html',
  '/og-share-generator.html',
  '/share.html',
  '/success.html'
]);

function listHtmlFiles(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = resolve(directory, entry.name);
    return entry.isDirectory() ? listHtmlFiles(path) : path.endsWith('.html') ? [path] : [];
  });
}

function pagePathFromFile(file) {
  const outputPath = relative(docsDirectory, file).replaceAll('\\', '/');
  if (outputPath.endsWith('index.html')) {
    return `/${outputPath.slice(0, -'index.html'.length)}`;
  }
  return `/${outputPath}`;
}

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

const htmlFiles = listHtmlFiles(docsDirectory);
const outputPagePaths = new Set(htmlFiles.map(pagePathFromFile));
const canonicalUrls = new Set();
const alternateUrls = new Set();

for (const file of htmlFiles) {
  const pagePath = pagePathFromFile(file);
  const html = readFileSync(file, 'utf8');
  const canonicalMatch = html.match(/<link rel="canonical" href="([^"]+)"/i);

  if (!nonIndexablePaths.has(pagePath)) {
    const expectedCanonical = `${siteOrigin}${pagePath}`;
    if (canonicalMatch?.[1] !== expectedCanonical) {
      failures.push(
        `${relative('.', file)}: expected canonical "${expectedCanonical}", found "${canonicalMatch?.[1] ?? 'none'}"`
      );
    } else if (canonicalUrls.has(expectedCanonical)) {
      failures.push(`${relative('.', file)}: duplicate canonical "${expectedCanonical}"`);
    } else {
      canonicalUrls.add(expectedCanonical);
    }

    const openGraphUrl = html.match(/<meta property="og:url" content="([^"]+)"/i)?.[1];
    if (openGraphUrl !== expectedCanonical) {
      failures.push(
        `${relative('.', file)}: expected og:url "${expectedCanonical}", found "${openGraphUrl ?? 'none'}"`
      );
    }

    for (const alternate of html.matchAll(/<link rel="alternate" hreflang="[^"]+" href="([^"]+)"/gi)) {
      alternateUrls.add(alternate[1]);
    }
  }

  for (const match of html.matchAll(/href="([^"]+)"/g)) {
    const href = match[1];
    if (!href.startsWith('/') || href.startsWith('//')) continue;

    const linkPath = href.split(/[?#]/, 1)[0];
    if (!linkPath) continue;

    const pageTarget =
      linkPath === '/' || linkPath.endsWith('/') || linkPath.endsWith('.html') ? linkPath : null;
    if (pageTarget && !outputPagePaths.has(pageTarget)) {
      failures.push(`${relative('.', file)}: internal page link does not exist "${href}"`);
      continue;
    }

    if (outputPagePaths.has(`${linkPath}.html`)) {
      failures.push(
        `${relative('.', file)}: internal page link "${href}" must use "${linkPath}.html"`
      );
    }
  }

  if (html.includes('http://audicap.work')) {
    failures.push(`${relative('.', file)}: contains non-HTTPS audicap.work URL`);
  }
}

const sitemap = readFileSync(resolve('docs/sitemap.xml'), 'utf8');
const sitemapUrls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);
const sitemapUrlSet = new Set(sitemapUrls);

if (sitemapUrls.length !== sitemapUrlSet.size) {
  failures.push('docs/sitemap.xml: contains duplicate URLs');
}

for (const canonical of canonicalUrls) {
  if (!sitemapUrlSet.has(canonical)) {
    failures.push(`docs/sitemap.xml: missing canonical URL "${canonical}"`);
  }
}

for (const sitemapUrl of sitemapUrlSet) {
  if (!canonicalUrls.has(sitemapUrl)) {
    failures.push(`docs/sitemap.xml: URL has no matching canonical page "${sitemapUrl}"`);
  }
}

for (const alternateUrl of alternateUrls) {
  if (!sitemapUrlSet.has(alternateUrl)) {
    failures.push(`hreflang URL is not listed in sitemap: "${alternateUrl}"`);
  }
}

const robots = readFileSync(resolve('docs/robots.txt'), 'utf8');
if (!robots.includes(`Sitemap: ${siteOrigin}/sitemap.xml`)) {
  failures.push('docs/robots.txt: missing canonical Sitemap declaration');
}

if (failures.length > 0) {
  console.error('Rendered page verification failed:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  console.log(
    `Verified body classes, internal URLs, and ${canonicalUrls.size} sitemap canonicals across ${htmlFiles.length} rendered pages.`
  );
}
