/**
 * Implement Gatsby's SSR (Server Side Rendering) APIs in this file.
 *
 * See: https://www.gatsbyjs.com/docs/reference/config-files/gatsby-ssr/
 */
// JSX 를 쓰면 Babel 이 import 를 넣어 ESM 이 되므로 exports.* 대신 import/export 문법을 쓴다
import React from 'react'

// 분석 스크립트는 운영 빌드(gatsby build)에서 환경 변수가 올바를 때만 넣는다.
// 값이 없거나 형식이 틀리면 스크립트를 넣지 않고, 사이트는 그대로 동작한다.
const GA_ID = (process.env.GATSBY_GA_MEASUREMENT_ID || '').trim()
const GC_ENDPOINT = (process.env.GATSBY_GOATCOUNTER_ENDPOINT || '').trim()
const isProduction = process.env.NODE_ENV === 'production'
const validGa = /^G-[A-Z0-9]+$/.test(GA_ID)
const validGc = /^https:\/\/[^/\s"'<>]+\/count\/?$/.test(GC_ENDPOINT)

if (isProduction && GA_ID && !validGa) {
  console.warn(`[analytics] GATSBY_GA_MEASUREMENT_ID 형식이 아니어서 GA4를 끕니다 (G-XXXXXXXXXX 형태여야 함)`)
}
if (isProduction && GC_ENDPOINT && !validGc) {
  console.warn(`[analytics] GATSBY_GOATCOUNTER_ENDPOINT 형식이 아니어서 GoatCounter를 끕니다 (https://코드.goatcounter.com/count)`)
}

/**
 * @type {import('gatsby').GatsbySSR['onRenderBody']}
 */
export const onRenderBody = ({ setHtmlAttributes, setHeadComponents }) => {
  setHtmlAttributes({ lang: `ko` })

  if (!isProduction) return
  const head = []

  if (validGa) {
    // 자동 page_view 는 끄고(send_page_view:false) gatsby-browser 의 onRouteUpdate 에서만 보낸다 → 최초 진입·SPA 이동 모두 1회
    head.push(
      <script key="gtag-src" async src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`} />,
      <script
        key="gtag-init"
        dangerouslySetInnerHTML={{
          __html: `window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${GA_ID}',{send_page_view:false});`,
        }}
      />,
    )
  }

  if (validGc) {
    // no_onload: 자동 집계를 끄고 onRouteUpdate 에서 정규화한 경로로 직접 count() 호출
    head.push(
      <script
        key="goatcounter"
        id="goatcounter-js"
        async
        src="https://gc.zgo.at/count.js"
        data-goatcounter={GC_ENDPOINT}
        data-goatcounter-settings='{"no_onload": true}'
      />,
    )
  }

  if (head.length) setHeadComponents(head)
}
