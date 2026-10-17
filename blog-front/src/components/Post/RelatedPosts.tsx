import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
import PostItem from 'components/Main/PostItem'
import { PostListItemType } from 'types/PostItem.types'
import { trackEvent } from 'utils/analytics'

type RelatedPostsProps = {
  posts: PostListItemType[]
  currentSlug: string
}

const Section = styled.section`
  width: 768px;
  margin: 60px auto 0;

  @media (max-width: 768px) {
    width: 100%;
    margin-top: 40px;
    padding: 0 20px;
  }
`

const Heading = styled.h2`
  margin-bottom: 20px;
  font-size: 22px;
  font-weight: 800;

  @media (max-width: 768px) {
    font-size: 19px;
  }
`

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding-bottom: 60px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`

// 관련 글은 gatsby-node.js 에서 빌드 시점에 계산되어 pageContext.relatedSlugs 로 전달된다
const RelatedPosts: FunctionComponent<RelatedPostsProps> = function ({
  posts,
  currentSlug,
}) {
  const items = posts.filter(({ node }) => node.fields.slug !== currentSlug)
  if (items.length === 0) return null

  return (
    <Section aria-labelledby="related-posts-heading">
      <Heading id="related-posts-heading">함께 읽으면 좋은 글</Heading>
      <Grid>
        {items.map(({ node: { id, fields: { slug }, frontmatter } }) => (
          <PostItem
            {...frontmatter}
            link={slug}
            key={id}
            onClick={() =>
              trackEvent('related_post_click', {
                content_type: 'post',
                item_id: slug,
                from_item_id: currentSlug,
              })
            }
          />
        ))}
      </Grid>
    </Section>
  )
}

export default RelatedPosts
