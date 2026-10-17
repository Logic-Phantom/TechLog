import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
import { Link } from 'gatsby'
import { GatsbyImage } from 'gatsby-plugin-image'
import { PostListItemType } from 'types/PostItem.types'

type PopularPostsProps = {
  items: { post: PostListItemType; views: number }[]
  generatedAt?: string | null
}

const Section = styled.section`
  width: 100%;
  max-width: 1268px;
  margin: 60px auto 0;

  @media (max-width: 768px) {
    width: 100%;
    margin-top: 40px;
    padding: 0 20px;
  }
`

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
`

const Heading = styled.h2`
  font-size: 24px;
  font-weight: 800;

  @media (max-width: 768px) {
    font-size: 20px;
  }
`

const StatsLink = styled(Link)`
  font-size: 14px;
  color: #426950;

  &:hover {
    text-decoration: underline;
  }
`

const List = styled.ol`
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  list-style: none;

  @media (max-width: 1268px) {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
`

const Card = styled(Link)`
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition: 0.3s box-shadow;

  &:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  }
`

const Thumb = styled(GatsbyImage)`
  width: 100%;
  height: 120px;
`

const Body = styled.div`
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 12px;
`

const Rank = styled.span`
  font-size: 13px;
  font-weight: 800;
  color: #426950;
`

const Title = styled.div`
  display: -webkit-box;
  overflow: hidden;
  margin: 4px 0 8px;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  font-size: 16px;
  font-weight: 700;
`

const Meta = styled.div`
  margin-top: auto;
  font-size: 13px;
  opacity: 0.75;
`

// 실제 조회수 데이터가 있을 때만 렌더링 (없으면 섹션 자체를 숨김)
const PopularPosts: FunctionComponent<PopularPostsProps> = function ({
  items,
  generatedAt,
}) {
  if (items.length === 0) return null

  return (
    <Section aria-labelledby="popular-posts-heading">
      <Header>
        <Heading id="popular-posts-heading">🔥 인기 글 TOP {items.length}</Heading>
        <StatsLink to="/stats/">
          {generatedAt ? `${generatedAt} 집계 · ` : ''}전체 통계 →
        </StatsLink>
      </Header>
      <List>
        {items.map(({ post: { node }, views }, index) => {
          const image = node.frontmatter.thumbnail?.childImageSharp?.gatsbyImageData
          const formatted = views.toLocaleString('ko-KR')
          return (
            <li key={node.id}>
              <Card to={node.fields.slug}>
                {image && <Thumb image={image} alt={node.frontmatter.title} />}
                <Body>
                  <Rank>#{index + 1}</Rank>
                  <Title>{node.frontmatter.title}</Title>
                  <Meta>
                    {node.frontmatter.categories.join(' / ')} ·{' '}
                    <span aria-label={`조회수 ${formatted}회`}>👁 {formatted}</span>
                  </Meta>
                </Body>
              </Card>
            </li>
          )
        })}
      </List>
    </Section>
  )
}

export default PopularPosts
