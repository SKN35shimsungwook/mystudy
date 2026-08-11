// 데이터 분석 전체 연습 노트 — 온라인일 땐 항상 최신 파일을 받아오고,
// 오프라인일 때만 마지막으로 받아둔 캐시로 대신 보여주는 서비스워커.
const CACHE_NAME = "ml-study-playground-v2";
const APP_SHELL = [
  "./ml_study_playground.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// 네트워크 우선(Network First): 온라인이면 항상 최신 버전을 받아오고 캐시도 갱신,
// 네트워크 요청이 실패할 때(오프라인)만 캐시된 마지막 버전을 보여준다.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request)
      .then((res) => {
        const copy = res.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        return res;
      })
      .catch(() => caches.match(event.request))
  );
});
