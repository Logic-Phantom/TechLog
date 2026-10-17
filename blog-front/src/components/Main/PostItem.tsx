import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
import { Link } from 'gatsby'
import { PostFrontmatterType } from 'types/PostItem.types'
import { GatsbyImage } from 'gatsby-plugin-image'
//import { PostFrontmatterType } from 'types/PostItem.types'

type PostItemProps = PostFrontmatterType & {
  link: string
  views?: number // 배포 시점 통계 API 집계값. 없으면 표시하지 않음
  onClick?: () => void
}

// type PostItemProps = {
//   title: string
//   date: string
//   categories: string[]
//   summary: string
//   thumbnail: {
//     publicURL: string
//   }
//   link: string
// }

const PostItemWrapper = styled(Link)`
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.15);
  transition: 0.3s box-shadow;
  cursor: pointer;

  &:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  }
`

const ThumbnailImage = styled(GatsbyImage)`
  width: 100%;
  height: 200px;
  border-radius: 10px 10px 0 0;
`

const PostItemContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px;
`

const Title = styled.div`
  display: -webkit-box;
  overflow: hidden;
  margin-bottom: 3px;
  text-overflow: ellipsis;
  white-space: normal;
  overflow-wrap: break-word;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  font-size: 20px;
  font-weight: 700;
`

const Date = styled.div`
  font-size: 14px;
  font-weight: 400;
  opacity: 0.7;
`

const Views = styled.span`
  margin-left: 8px;
  font-variant-numeric: tabular-nums;
`

const Category = styled.div`
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
  margin: 10px -5px;
`

const CategoryItem = styled.div`
  margin: 2.5px 5px;
  padding: 3px 5px;
  border-radius: 3px;
  background: black;
  font-size: 14px;
  font-weight: 700;
  color: white;
`

const Summary = styled.div`
  display: -webkit-box;
  overflow: hidden;
  margin-top: auto;
  text-overflow: ellipsis;
  white-space: normal;
  overflow-wrap: break-word;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  font-size: 16px;
  opacity: 0.8;
`

const PostItem: FunctionComponent<PostItemProps> = function ({
  title,
  date,
  categories,
  summary,
  thumbnail,
  link,
  views,
  onClick,
}) {
  // 썸네일 이미지 데이터 추출 (null-safe)
  const gatsbyImageData = thumbnail && thumbnail.childImageSharp ? thumbnail.childImageSharp.gatsbyImageData : undefined;

  return (
    <PostItemWrapper to={link} onClick={onClick}>
      {gatsbyImageData && <ThumbnailImage image={gatsbyImageData} alt={title} />}

      <PostItemContent>
        <Title>{title}</Title>
        <Date>
          {date}
          {typeof views === 'number' && (
            <Views
              aria-label={`조회수 ${views.toLocaleString('ko-KR')}회`}
              title="마지막 배포 시점 집계"
            >
              · 👁 {views.toLocaleString('ko-KR')}
            </Views>
          )}
        </Date>
        <Category>
          {categories.map(item => (
            <CategoryItem key={item}>{item}</CategoryItem>
          ))}
        </Category>
        <Summary>{summary}</Summary>
      </PostItemContent>
    </PostItemWrapper>
  )
}


export default PostItem

