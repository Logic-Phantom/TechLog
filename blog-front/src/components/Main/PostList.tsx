//import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
import PostItem from 'components/Main/PostItem'
import { PostListItemType } from 'types/PostItem.types'
//import React, { FunctionComponent, useMemo } from 'react'
import React, { FunctionComponent } from 'react'
import useInfiniteScroll, {
  useInfiniteScrollType,
} from 'hooks/useInfiniteScroll'


const POST_ITEM_DATA = {
  title: 'React 시작하기',
  date: '2024.08.12.',
  categories: ['Web', 'Frontend', 'Testing'],
  summary:
    'React를 사용하여 블로그 만들기 시작',
  thumbnail:
    'https://github.com/logic-phantom/TechLog/blob/main/blog-front/contents/react.png?raw=true',
  link: 'https://www.google.co.kr',
}

type PostListProps = {
  selectedCategory: string
  posts: PostListItemType[]
}

export type PostType = {
  node: {
    id: string
    frontmatter: {
      title: string
      summary: string
      date: string
      categories: string[]
      thumbnail: {
        publicURL: string
      }
    }
  }
}


// const PostListWrapper = styled.div`
//   display: grid;
//   grid-template-columns: 1fr 1fr;
//   grid-gap: 20px;
//   width: 768px;
//   margin: 0 auto;
//   padding: 50px 0 100px;

//   @media (max-width: 768px) {
//     grid-template-columns: 1fr;
//     width: 100%;
//     padding: 50px 20px;
//   }
// `

const PostListWrapper = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-gap: 20px;
  width: 1268px;
  margin: 0 auto;
  padding: 50px 0 100px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    width: 100%;
    padding: 50px 20px;
  }
`

//실질적인 아이템 목록 
// const PostList: FunctionComponent = function () {
//   return (
//     <PostListWrapper>
//       <PostItem {...POST_ITEM_DATA} />
//     </PostListWrapper>
//   )
// }

const PostList: FunctionComponent<PostListProps> = function ({
  selectedCategory,
  posts,
}) {
  const { containerRef, postList }: useInfiniteScrollType = useInfiniteScroll(
    selectedCategory,
    posts,
  )

  return (
    <PostListWrapper ref={containerRef}>
      {postList.map(
        ({
          node: {
            id,
            fields: { slug },
            frontmatter,
          },
        }: PostListItemType) => (
          <PostItem {...frontmatter} link={slug} key={id} />
        ),
      )}
    </PostListWrapper>
  )
}


export default PostList