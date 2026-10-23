import React, { FunctionComponent, useMemo } from 'react'
import styled from '@emotion/styled'
import { graphql, Link } from 'gatsby'
import Template from 'components/Common/Template'
import PopularPosts from 'components/Main/PopularPosts'
import ScrollToTop from 'components/Common/ScrollToTop'
import { PostListItemType } from 'types/PostItem.types'
import { buildViewsBySlug, rankByViews, SiteStatsType, toKst } from 'utils/stats'

type StatsPageProps = {
  data: {
    allMarkdownRemark: {
      edges: PostListItemType[]
    }
    siteStats: SiteStatsType | null
  }
}

const Header = styled.div`
  width: 100%;
  background: linear-gradient(60deg, rgb(66, 105, 78) 0%, rgb(73, 110, 93) 100%);
  color: #ffffff;
  padding: 50px 20px;
`

const HeaderInner = styled.div`
  max-width: 960px;
  margin: 0 auto;
`

const HomeLink = styled(Link)`
  font-size: 15px;
  opacity: 0.85;

  &:hover {
    text-decoration: underline;
  }
`

const PageTitle = styled.h1`
  margin-top: 16px;
  font-size: 32px;
  font-weight: 800;

  @media (max-width: 768px) {
    font-size: 24px;
  }
`

const Content = styled.main`
  flex: 1;
  width: 960px;
  margin: 0 auto;
  padding-bottom: 80px;

  @media (max-width: 960px) {
    width: 100%;
  }
`

const Block = styled.section`
  margin-top: 40px;

  @media (max-width: 960px) {
    padding: 0 20px;
  }
`

const SubHeading = styled.h2`
  margin-bottom: 16px;
  font-size: 22px;
  font-weight: 800;
`

const Summary = styled.dl`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;

  div {
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.12);
  }

  dt {
    font-size: 14px;
    opacity: 0.7;
  }

  dd {
    margin-top: 6px;
    font-size: 24px;
    font-weight: 800;
    font-variant-numeric: tabular-nums;
  }
`

const Notice = styled.p`
  padding: 20px;
  border-radius: 10px;
  background: rgba(66, 105, 78, 0.08);
  line-height: 1.7;
`

const Note = styled.p`
  margin-top: 12px;
  font-size: 14px;
  line-height: 1.6;
  opacity: 0.75;
`

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;

  th,
  td {
    padding: 10px 8px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    text-align: left;
  }

  th:last-of-type,
  td:last-of-type {
    text-align: right;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }

  a:hover {
    text-decoration: underline;
  }

  @media (max-width: 768px) {
    font-size: 14px;
  }
`

const formatDateTime = (value: string | null) =>
  value ? `${toKst(value).slice(0, 16)} KST` : '-'

const formatDate = (value: string | null) => (value ? toKst(value).slice(0, 10) : null)

const StatsPage: FunctionComponent<StatsPageProps> = function ({
  data: {
    allMarkdownRemark: { edges },
    siteStats,
  },
}) {
  const viewsBySlug = useMemo(() => buildViewsBySlug(siteStats, edges), [])
  const ranked = useMemo(() => rankByViews(edges, viewsBySlug), [])
  const available = !!siteStats && siteStats.available

  return (
    <Template
      title="블로그 통계 | Forest_LIM"
      description="GoatCounter 공개 통계로 집계한 게시글 조회수와 인기 글 순위"
      url="/stats/"
    >
      <Header>
        <HeaderInner>
          <HomeLink to="/">← 메인으로</HomeLink>
          <PageTitle>📊 블로그 통계</PageTitle>
        </HeaderInner>
      </Header>

      <Content>
        {!available || !siteStats ? (
          <Block>
            <Notice>
              아직 조회수 통계가 설정되지 않았거나 데이터를 가져오지 못했습니다.
              <br />
              통계는 배포 빌드 때 GoatCounter API 에서 받아오며, 가짜 수치는 표시하지 않습니다.
            </Notice>
          </Block>
        ) : (
          <>
            <Block aria-labelledby="stats-summary">
              <SubHeading id="stats-summary">요약</SubHeading>
              <Summary>
                {siteStats.totalViews !== null && (
                  <div>
                    <dt>사이트 전체 조회수</dt>
                    <dd>{siteStats.totalViews.toLocaleString('ko-KR')}</dd>
                  </div>
                )}
                <div>
                  <dt>조회 기록이 있는 게시글</dt>
                  <dd>{ranked.length.toLocaleString('ko-KR')}편</dd>
                </div>
                <div>
                  <dt>마지막 갱신</dt>
                  <dd style={{ fontSize: 18 }}>{formatDateTime(siteStats.generatedAt)}</dd>
                </div>
              </Summary>
              <Note>
                집계 기준: GoatCounter 방문 수({siteStats.metric || 'visitors'}) ·{' '}
                {formatDate(siteStats.rangeStart) || '전체 기간'} ~{' '}
                {formatDate(siteStats.rangeEnd || siteStats.generatedAt) || '-'} (KST) · 배포 빌드 때마다 갱신
              </Note>
            </Block>

            <PopularPosts items={ranked.slice(0, 5)} />

            <Block aria-labelledby="stats-all">
              <SubHeading id="stats-all">게시글별 누적 조회수</SubHeading>
              {ranked.length === 0 ? (
                <Notice>아직 게시글 조회 기록이 없습니다.</Notice>
              ) : (
                <Table>
                  <thead>
                    <tr>
                      <th scope="col">순위</th>
                      <th scope="col">게시글</th>
                      <th scope="col">조회수</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ranked.map(({ post: { node }, views }, index) => (
                      <tr key={node.id}>
                        <td>{index + 1}</td>
                        <td>
                          <Link to={node.fields.slug}>{node.frontmatter.title}</Link>
                        </td>
                        <td>{views.toLocaleString('ko-KR')}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              )}
            </Block>
          </>
        )}
      </Content>
      <ScrollToTop />
    </Template>
  )
}

export default StatsPage

export const queryStats = graphql`
  query queryStats {
    allMarkdownRemark(
      sort: [{ frontmatter: { date: DESC } }, { frontmatter: { title: ASC } }]
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
                gatsbyImageData(width: 400, height: 240)
              }
            }
          }
        }
      }
    }
    siteStats {
      available
      metric
      generatedAt
      rangeStart
      rangeEnd
      totalViews
      posts {
        path
        views
      }
    }
  }
`
