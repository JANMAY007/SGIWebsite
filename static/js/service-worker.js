const CACHE_NAME = 'sgi-cache-v1';
const urlsToCache = [
  '/offline.html',
  '/static/bootstrap/css/bootstrap.min.css', // Include your CSS files
  '/static/bootstrap/css/bootstrap.min.js', // Include your JS files
  '/static/img/logo.png?h=7b3a05042dd79230d60eb276d4c089f7' // Your logo
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
