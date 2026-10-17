// GA4 · GoatCounter 공통 헬퍼
// - 스크립트는 gatsby-ssr.js 가 운영 빌드에서 환경 변수가 있을 때만 넣는다.
// - 이 파일은 그 스크립트가 있을 때만 동작하고, 없으면 아무 일도 하지 않는다.

type GoatCounterVars = { path: string; title?: string; event?: boolean }

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void
    goatcounter?: { count?: (vars: GoatCounterVars) => void }
  }
}

export const GOATCOUNTER_SCRIPT_ID = 'goatcounter-js'

// 조회수 집계·조회에 쓰는 경로 규칙 (scripts/fetch_stats.py 의 normalize_path 와 동일해야 함)
// - 쿼리·해시 제거, 퍼센트 인코딩 해제, 앞뒤 슬래시 보장 (Gatsby 게시글 slug 가 `/slug/` 형태)
export const normalizePath = function (raw: string): string {
  let path = (raw || '/').split(/[?#]/)[0]
  try {
    path = decodeURIComponent(path)
  } catch (e) {
    // 잘못된 인코딩이면 원문 유지
  }
  if (!path.startsWith('/')) path = `/${path}`
  const last = path.split('/').pop() || ''
  if (!path.endsWith('/') && !last.includes('.')) path = `${path}/`
  return path.replace(/\/{2,}/g, '/')
}

// GATSBY_GOATCOUNTER_ENDPOINT(`https://코드.goatcounter.com/count`)에서 사이트 주소를 얻는다
export const getGoatCounterBase = function (): string | null {
  const endpoint = process.env.GATSBY_GOATCOUNTER_ENDPOINT
  if (!endpoint || !/^https:\/\/[^/\s]+\/count\/?$/.test(endpoint)) return null
  return endpoint.replace(/\/count\/?$/, '')
}

// 공개 방문자 카운터(`/counter/<path>.json`)에서 해당 경로의 누적 수를 가져온다.
// 응답의 count 는 천 단위 구분자가 들어간 문자열이므로 숫자만 남겨 해석한다. 없으면 null.
export const fetchViewCount = async function (
  path: string,
  signal?: AbortSignal,
): Promise<number | null> {
  const base = getGoatCounterBase()
  if (!base || typeof fetch !== 'function') return null
  try {
    const res = await fetch(
      `${base}/counter/${encodeURIComponent(normalizePath(path))}.json`,
      { signal, credentials: 'omit' },
    )
    if (!res.ok) return null
    const data = await res.json()
    const digits = String(data && data.count).replace(/[^0-9]/g, '')
    return digits ? Number(digits) : null
  } catch (e) {
    return null
  }
}

// GA4 맞춤 이벤트 (share_click · copy_link · related_post_click). 개인정보는 보내지 않는다.
export const trackEvent = function (
  name: string,
  params: Record<string, string | number> = {},
): void {
  if (typeof window === 'undefined' || typeof window.gtag !== 'function') return
  window.gtag('event', name, params)
}

let lastTrackedPath: string | null = null
let lastSentTitle: string | null = null
let pendingGoatCounter: GoatCounterVars | null = null
let pendingTimer: ReturnType<typeof setTimeout> | null = null
let pendingSend: (() => void) | null = null
const TITLE_WAIT_MS = 1000

const countGoatCounter = function (vars: GoatCounterVars): void {
  const gc = window.goatcounter
  if (gc && typeof gc.count === 'function') {
    gc.count(vars)
    return
  }
  // count.js 가 아직 로딩 중이면 마지막 페이지만 기억했다가 로드 직후 1회 전송
  const script = document.getElementById(GOATCOUNTER_SCRIPT_ID)
  if (!script) return
  if (pendingGoatCounter === null) {
    script.addEventListener(
      'load',
      () => {
        const next = pendingGoatCounter
        pendingGoatCounter = null
        const loaded = window.goatcounter
        if (next && loaded && typeof loaded.count === 'function') loaded.count(next)
      },
      { once: true },
    )
  }
  pendingGoatCounter = vars
}

// gatsby-browser 의 onRouteUpdate 에서 호출 (최초 진입 + SPA 이동 모두).
// GA4 는 config 에서 send_page_view:false 로 자동 페이지뷰를 끄고 여기서만 보내므로 중복되지 않는다.
// 같은 경로가 연달아 들어오면(해시 이동·재렌더) 무시한다.
export const trackPageView = function (
  location: { pathname: string; search?: string },
  isInitial = false,
): void {
  if (typeof window === 'undefined') return
  const path = normalizePath(location.pathname)
  if (path === lastTrackedPath) return
  lastTrackedPath = path

  const hasGtag = typeof window.gtag === 'function'
  const hasGoatCounter = !!document.getElementById(GOATCOUNTER_SCRIPT_ID)
  if (!hasGtag && !hasGoatCounter) return

  // 이전 이동의 전송이 아직 대기 중이면(빠른 연속 이동) 지금 보내고 새 이동을 처리
  if (pendingTimer !== null && pendingSend) {
    clearTimeout(pendingTimer)
    pendingSend()
  }

  const send = () => {
    pendingTimer = null
    pendingSend = null
    const title = document.title
    lastSentTitle = title
    if (hasGtag && window.gtag) {
      window.gtag('event', 'page_view', {
        page_title: title,
        page_location: `${window.location.origin}${location.pathname}${
          location.search || ''
        }`,
        page_path: path,
      })
    }
    if (hasGoatCounter) countGoatCounter({ path, title })
  }

  // SPA 이동(특히 뒤로/앞으로 가기)은 onRouteUpdate 가 새 페이지 렌더·react-helmet 의 제목 갱신보다
  // 먼저 올 수 있으므로, 제목이 직전 전송 때와 달라질 때까지 최대 1초 기다린 뒤 보낸다
  const startedAt = Date.now()
  const trySend = () => {
    if (
      isInitial ||
      document.title !== lastSentTitle ||
      Date.now() - startedAt >= TITLE_WAIT_MS
    ) {
      send()
      return
    }
    pendingTimer = setTimeout(trySend, 50)
  }
  pendingSend = send
  pendingTimer = setTimeout(trySend, 0)
}
