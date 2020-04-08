// This is the service worker with the Cache-first network

const CACHE = "pwabuilder-precache";
const precacheFiles = [
    "/",
    "/profile/",
    "/fishid/",
    "/static/style.css",
    "/static/identify.js",
    "/static/jquery.fittext.js",
    "/static/fish/Black-Crappie-Duane-Raver.jpg",		
    "/static/fish/Striped-Bass-Duane-Raver.jpg",
    "/static/fish/Black-Crappie-Live.jpg",	
    "/static/fish/Striped_bass.jpg",
    "/static/fish/Black_crappie.jpg",		
    "/static/fish/White-Bass-Duane-Raver.jpg",
    "/static/fish/Bluegill-Duane-Raver.jpg",		
    "/static/fish/White-crappie-Duane Raver.jpg",
    "/static/fish/Bluegill.jpg",				
    "/static/fish/White_bass.jpg",
    "/static/fish/ChannelCatfish-Duane-Raver.jpg",		
    "/static/fish/White_crappie.jpg",
    "/static/fish/Flathead-Catfish-Duane-Raver.jpg",	
    "/static/fish/Yellow_perch.jpg",
    "/static/fish/Largemouth-Bass-Duane-Raver.jpg",		
    "/static/fish/channel_catfish.jpg",
    "/static/fish/Smallmouth-Bass-Duane-Raver.jpg",		
    "/static/fish/yellow-perch-Duane-Raver.jpg",
    "/static/fish/Smallmouth_bass.jpg",
    "/lake/2/",
    "/lake/1/"
];

self.addEventListener("install", function (event) {
    console.log("[PWA Builder] Install Event processing");

    console.log("[PWA Builder] Skip waiting on install");
    self.skipWaiting();

    event.waitUntil(
        caches.open(CACHE).then(function (cache) {
            console.log("[PWA Builder] Caching pages during install");
            return cache.addAll(precacheFiles);
        })
    );
});

// Allow sw to control of current page
self.addEventListener("activate", function (event) {
    console.log("[PWA Builder] Claiming clients for current page");
    event.waitUntil(self.clients.claim());
});

// If any fetch fails, it will look for the request in the cache and serve it from there first
self.addEventListener("fetch", function (event) {
    if (event.request.method !== "GET") return;

    event.respondWith(
        fromCache(event.request).then(
            function (response) {
                // The response was found in the cache so we responde with it and update the entry

                // This is where we call the server to get the newest version of the
                // file to use the next time we show view
                event.waitUntil(
                    fetch(event.request).then(function (response) {
                        return updateCache(event.request, response);
                    })
                );

                return response;
            },
            function () {
                // The response was not found in the cache so we look for it on the server
                return fetch(event.request)
                    .then(function (response) {
                        // If request was success, add or update it in the cache
                        event.waitUntil(updateCache(event.request, response.clone()));

                        return response;
                    })
                    .catch(function (error) {
                        console.log("[PWA Builder] Network request failed and no cache." + error);
                    });
            }
        )
    );
});

function fromCache(request) {
    // Check to see if you have it in the cache
    // Return response
    // If not in the cache, then return
    return caches.open(CACHE).then(function (cache) {
        return cache.match(request).then(function (matching) {
            if (!matching || matching.status === 404) {
                return Promise.reject("no-match");
            }

            return matching;
        });
    });
}

function updateCache(request, response) {
    return caches.open(CACHE).then(function (cache) {
        return cache.put(request, response);
    });
}
