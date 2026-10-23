//import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
import GlobalStyle from 'components/Common/GlobalStyle'
import Footer from 'components/Common/Footer'
import CategoryList, { CategoryListProps } from 'components/Main/CategoryList'
import Introduction from 'components/Main/Introduction'
import PostList, { PostType } from 'components/Main/PostList'
import PopularPosts from 'components/Main/PopularPosts'
import ScrollToTop from 'components/Common/ScrollToTop'
import { graphql } from 'gatsby'
import { PostListItemType } from 'types/PostItem.types'
import { IGatsbyImageData } from 'gatsby-plugin-image'
import queryString, { ParsedQuery } from 'query-string'
import React, { FunctionComponent, useMemo } from 'react'
import Template from 'components/Common/Template'
import { buildViewsBySlug, rankByViews, SiteStatsType, toKst } from 'utils/stats'
//import { PostListItemType } from 'types/PostItem.types'

const CATEGORY_LIST = {
  All: 5,
  Web: 3,
  Mobile: 2,
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
`

type IndexPageProps = {
  location: {
    search: string
  }
  data: {
    site: {
      siteMetadata: {
        title: string
        description: string
        siteUrl: string
      }
    }
    allMarkdownRemark: {
      edges: PostListItemType[]
    }
    file: {
      childImageSharp: {
        gatsbyImageData: IGatsbyImageData
      }
      publicURL: string
    }
    siteStats: SiteStatsType | null
  }
}

// CATEGORY_LIST 상수 제거

const IndexPage: FunctionComponent<IndexPageProps> = function ({
  location: { search },
  data: {
    site: {
      siteMetadata: { title, description, siteUrl },
    },
    allMarkdownRemark: { edges },
    file: {
      childImageSharp: { gatsbyImageData },
      publicURL,
    },
    siteStats,
  },
}) {
  const parsed: ParsedQuery<string> = queryString.parse(search)
  const selectedCategory: string =
    typeof parsed.category !== 'string' || !parsed.category
      ? 'All'
      : parsed.category

  const categoryList = useMemo(
    () =>
      edges.reduce(
        (
          list: CategoryListProps['categoryList'],
          {
            node: {
              frontmatter: { categories },
            },
          }: PostType,
        ) => {
          categories.forEach(category => {
            if (list[category] === undefined) list[category] = 1;
            else list[category]++;
          });

          list['All']++;

          return list;
        },
        { All: 0 },
      ),
    [],
  )

  // 인기 글은 실제 조회수 데이터가 있을 때만 (최신 글로 대체하지 않음)
  const viewsBySlug = useMemo(() => buildViewsBySlug(siteStats, edges), [])
  const popularPosts = useMemo(() => rankByViews(edges, viewsBySlug, 5), [])

  return (
    <Template
      title={title}
      description={description}
      url={`${siteUrl.replace(/\/$/, '')}/`}
      image={publicURL}
    >
      <Introduction profileImage={gatsbyImageData} />
      <PopularPosts
        items={popularPosts}
        generatedAt={
          siteStats && siteStats.generatedAt
            ? `${toKst(siteStats.generatedAt).slice(0, 10).replace(/-/g, '.')}.`
            : null
        }
      />
      <CategoryList
        selectedCategory={selectedCategory}
        categoryList={categoryList}
      />
      <PostList
        selectedCategory={selectedCategory}
        posts={edges}
        viewsBySlug={viewsBySlug}
      />
      <ScrollToTop />
    </Template>
  )
}




export default IndexPage

export const getPostList = graphql`
  query getPostList {
    site {
      siteMetadata {
        title
        description
        siteUrl
      }
    }
    allMarkdownRemark(
      sort: [{frontmatter: {date: DESC}}, {frontmatter: {title: ASC}}]
    ) {
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
    file(name: { eq: "profile-image" }) {
      childImageSharp {
        gatsbyImageData(width: 120, height: 120)
      }
      publicURL
    }
    siteStats {
      available
      generatedAt
      posts {
        path
        views
      }
    }
  }
`;
