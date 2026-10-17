import React, { FunctionComponent } from 'react'
import { graphql } from 'gatsby'
//import { PostPageItemType } from 'types/PostItem.types' // 바로 아래에서 정의할 것입니다
import Template, { toAbsoluteUrl } from 'components/Common/Template'
import PostHead from 'components/Post/PostHead'
import PostContent from 'components/Post/PostContent'
import PostShare from 'components/Post/PostShare'
import RelatedPosts from 'components/Post/RelatedPosts'
import CommentWidget from 'components/Post/CommentWidget'
import ScrollToTop from 'components/Common/ScrollToTop'
import { PostFrontmatterType, PostListItemType } from 'types/PostItem.types'
import { buildViewsBySlug, SiteStatsType } from 'utils/stats'



type PostTemplateProps = {
    data: {
      site: {
        siteMetadata: {
          title: string
          author: string
          siteUrl: string
        }
      }
      allMarkdownRemark: {
        edges: PostPageItemType[]
      }
      related: {
        edges: PostListItemType[]
      }
      siteStats: SiteStatsType | null
    }
    pageContext: {
      slug: string
      relatedSlugs?: string[]
    }
  }

  export type PostPageItemType = {
    node: {
      html: string
      excerpt?: string
      fields: {
        slug: string
      }
      frontmatter: PostFrontmatterType & {
        isoDate: string
        updatedAt?: string | null
      }
    }
}

  // summary 는 카드용 짧은 카피(10~25자)라 검색 결과 설명으로는 짧다.
  // 짧으면 본문 앞부분(제목 제외)을 이어 붙여 155자 안쪽의 meta description 을 만든다
  const buildDescription = (summary: string, title: string, excerpt?: string): string => {
    if (summary.length >= 50 || !excerpt) return summary
    let rest = excerpt.replace(/\s+/g, ' ').trim()
    if (rest.startsWith(title)) rest = rest.slice(title.length).trim()
    if (!rest) return summary
    // 이모지(서로게이트 쌍)를 반으로 자르면 Utterances 의 encodeURIComponent 가 실패하므로 코드 포인트 단위로 자른다
    // (excerpt 자체가 이모지 중간에서 잘려 올 수 있어 짝 없는 서로게이트도 제거)
    const chars = Array.from(`${summary} — ${rest}`).filter(
      ch => !(ch.length === 1 && ch.charCodeAt(0) >= 0xd800 && ch.charCodeAt(0) <= 0xdfff),
    )
    return chars.length > 155 ? `${chars.slice(0, 154).join('').trimEnd()}…` : chars.join('')
  }

  const PostTemplate: FunctionComponent<PostTemplateProps> = function ({
    data: {
      site: {
        siteMetadata: { title: siteName, author, siteUrl },
      },
      allMarkdownRemark: { edges },
      related,
      siteStats,
    },
    pageContext: { relatedSlugs = [] },
  }) {
    const {
      node: {
        html,
        excerpt,
        fields: { slug },
        frontmatter: {
          title,
          summary,
          date,
          isoDate,
          updatedAt,
          categories,
          thumbnail,
        },
      },
    } = edges[0];

    // 썸네일 이미지 데이터 추출 (null-safe)
    const gatsbyImageData = thumbnail && thumbnail.childImageSharp ? thumbnail.childImageSharp.gatsbyImageData : undefined;
    const publicURL = thumbnail && thumbnail.publicURL ? thumbnail.publicURL : undefined;

    // canonical URL (gatsby-plugin-canonical-urls 와 같은 siteUrl + slug)
    const canonicalUrl = toAbsoluteUrl(siteUrl, slug) || siteUrl
    const imageUrl = toAbsoluteUrl(siteUrl, publicURL)
    const description = buildDescription(summary, title, excerpt)
    const views = buildViewsBySlug(siteStats, [
      { node: { id: slug, fields: { slug }, frontmatter: edges[0].node.frontmatter } },
    ])[slug]

    // 빌드 시점에 계산한 순서대로 관련 글 정렬
    const relatedPosts = relatedSlugs
      .map(relatedSlug => related.edges.find(({ node }) => node.fields.slug === relatedSlug))
      .filter((edge): edge is PostListItemType => edge !== undefined)

    // 확인 가능한 정보만 넣는다 (수정일은 updatedAt 프론트매터가 있을 때만)
    const jsonLd: Record<string, unknown> = {
      '@context': 'https://schema.org',
      '@type': 'BlogPosting',
      headline: title,
      description,
      datePublished: isoDate,
      ...(updatedAt ? { dateModified: updatedAt } : {}),
      mainEntityOfPage: { '@type': 'WebPage', '@id': canonicalUrl },
      url: canonicalUrl,
      ...(imageUrl ? { image: [imageUrl] } : {}),
      author: { '@type': 'Person', name: author, url: 'https://github.com/Logic-Phantom' },
      publisher: { '@type': 'Organization', name: siteName, url: siteUrl },
      inLanguage: 'ko-KR',
      articleSection: categories,
    }

    return (
      <Template
        title={title}
        description={description}
        url={slug}
        image={publicURL}
        type="article"
        publishedTime={isoDate}
        modifiedTime={updatedAt || undefined}
        jsonLd={jsonLd}
      >
        <PostHead
          title={title}
          date={date}
          categories={categories}
          thumbnail={gatsbyImageData}
          path={slug}
          views={views}
        />
        <PostContent html={html} />
        <PostShare title={title} url={canonicalUrl} slug={slug} />
        <RelatedPosts posts={relatedPosts} currentSlug={slug} />
        <CommentWidget />
        <ScrollToTop />
      </Template>
    )
  }

export default PostTemplate

export const queryMarkdownDataBySlug = graphql`
  query queryMarkdownDataBySlug($slug: String, $relatedSlugs: [String]) {
    site {
      siteMetadata {
        title
        author
        siteUrl
      }
    }
    allMarkdownRemark(filter: { fields: { slug: { eq: $slug } } }) {
      edges {
        node {
          html
          excerpt(pruneLength: 200, format: PLAIN)
          fields {
            slug
          }
          frontmatter {
            title
            summary
            date(formatString: "YYYY.MM.DD.")
            isoDate: date(formatString: "YYYY-MM-DD")
            updatedAt(formatString: "YYYY-MM-DD")
            categories
            thumbnail {
              childImageSharp {
                gatsbyImageData
              }
              publicURL
            }
          }
        }
      }
    }
    related: allMarkdownRemark(filter: { fields: { slug: { in: $relatedSlugs } } }) {
      edges {
        node {
          id
          fields {
            slug
          }
          frontmatter {
            title
            summary
            date(formatString: "YYYY.MM.DD.")
            categories
            thumbnail {
              childImageSharp {
                gatsbyImageData(width: 768, height: 400)
              }
            }
          }
        }
      }
    }
    siteStats {
      available
      posts {
        path
        views
      }
    }
  }
`

// export type PostPageItemType = {
//     node: {
//       html: string
//       frontmatter: PostFrontmatterType
//     }
//   }
