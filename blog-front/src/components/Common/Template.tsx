import React, { FunctionComponent, ReactNode } from 'react'
import styled from '@emotion/styled'
import GlobalStyle from 'components/Common/GlobalStyle'
import Footer from 'components/Common/Footer'
import { Helmet } from 'react-helmet'
import { graphql, useStaticQuery } from 'gatsby'

type TemplateProps = {
  title: string
  description: string
  url: string
  image?: string
  type?: 'website' | 'article'
  publishedTime?: string
  modifiedTime?: string
  jsonLd?: Record<string, unknown>
  children: ReactNode
}

type SiteMetadataQuery = {
  site: {
    siteMetadata: {
      title: string
      siteUrl: string
    }
  }
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`

// 상대 경로(/static/...)를 og:image 등에서 쓸 수 있는 절대 URL로 바꾼다
export const toAbsoluteUrl = function (siteUrl: string, value?: string): string | undefined {
  if (!value) return undefined
  if (/^https?:\/\//.test(value)) return value
  return `${siteUrl.replace(/\/$/, '')}${encodeURI(value.startsWith('/') ? value : `/${value}`)}`
}

const Template: FunctionComponent<TemplateProps> = function ({
  title,
  description,
  url,
  image,
  type = 'website',
  publishedTime,
  modifiedTime,
  jsonLd,
  children,
}) {
  const {
    site: {
      siteMetadata: { title: siteName, siteUrl },
    },
  } = useStaticQuery<SiteMetadataQuery>(graphql`
    query TemplateSiteMetadata {
      site {
        siteMetadata {
          title
          siteUrl
        }
      }
    }
  `)
  const imageUrl = toAbsoluteUrl(siteUrl, image)
  const pageUrl = toAbsoluteUrl(siteUrl, url) || siteUrl

  return (
    <Container>
      <Helmet>
        <title>{title}</title>

        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta httpEquiv="Content-Type" content="text/html;charset=UTF-8" />

        <meta property="og:type" content={type} />
        <meta property="og:title" content={title} />
        <meta property="og:description" content={description} />
        {imageUrl && <meta property="og:image" content={imageUrl} />}
        <meta property="og:url" content={pageUrl} />
        <meta property="og:site_name" content={siteName} />
        <meta property="og:locale" content="ko_KR" />
        {publishedTime && <meta property="article:published_time" content={publishedTime} />}
        {modifiedTime && <meta property="article:modified_time" content={modifiedTime} />}

        <meta name="twitter:card" content={imageUrl ? 'summary_large_image' : 'summary'} />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        {imageUrl && <meta name="twitter:image" content={imageUrl} />}

        {jsonLd && (
          <script type="application/ld+json">
            {JSON.stringify(jsonLd).replace(/</g, '\\u003c')}
          </script>
        )}
      </Helmet>

      <GlobalStyle />
      {children}
      <Footer />
    </Container>
  )
}

export default Template
