const CACHE_NAME = 'sgi-cache-v1';
const urlsToCache = [
  '',
  '/offline',
  '/static/bootstrap/css/bootstrap.min.css', // Ensure these paths are correct
  '/static/bootstrap/js/bootstrap.min.js',  // Ensure these paths are correct
    '/static/js/script.min.js',
    '/static/js/theme.js',
  '/static/img/logo.png?h=7b3a05042dd79230d60eb276d4c089f7' // Ensure these paths are correct
];

// Install service worker and cache the static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event to serve cached assets
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached asset or fetch from network
        return response || fetch(event.request);
      })
      .catch(() => {
        // Fallback to offline.html for navigation requests
        if (event.request.mode === 'navigate') {
          return caches.match('/offline.html');
        }
      })
  );
});

// Activate service worker and remove old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
