import { PostListItemType } from 'types/PostItem.types'
import { normalizePath } from 'utils/analytics'

// gatsby-node.js 의 SiteStats 노드 (static/data/popular-posts.json 이 없으면 available:false)
export type SiteStatsType = {
  available: boolean
  source: string | null
  metric: string | null
  generatedAt: string | null
  rangeStart: string | null
  rangeEnd: string | null
  totalViews: number | null
  posts: { path: string; views: number }[]
}

// 통계 JSON 의 시각은 UTC. 게시글 날짜(KST)와 맞추려고 +9시간 한 'YYYY-MM-DD HH:mm:ss' 로 바꾼다
// (GraphQL formatString 은 UTC 기준이라 쓰지 않음, 빌드 서버 시간대와도 무관)
export const toKst = function (value: string): string {
  const time = Date.parse(value)
  if (Number.isNaN(time)) return value.replace('T', ' ')
  return new Date(time + 9 * 60 * 60 * 1000).toISOString().replace('T', ' ')
}

// 통계 경로를 실제 게시글 slug 와 매핑. 사이트에 없는 경로는 버린다
export const buildViewsBySlug = function (
  stats: SiteStatsType | null | undefined,
  posts: PostListItemType[],
): Record<string, number> {
  const result: Record<string, number> = {}
  if (!stats || !stats.available) return result
  const slugByPath: Record<string, string> = {}
  posts.forEach(({ node: { fields: { slug } } }) => {
    slugByPath[normalizePath(slug)] = slug
  })
  stats.posts.forEach(({ path, views }) => {
    const slug = slugByPath[normalizePath(path)]
    if (slug !== undefined) result[slug] = (result[slug] || 0) + views
  })
  return result
}

// 실제 조회수 내림차순 → 동점이면 최신 글 → 제목순. 조회수 기록이 없는 글은 포함하지 않는다
export const rankByViews = function (
  posts: PostListItemType[],
  viewsBySlug: Record<string, number>,
  limit?: number,
): { post: PostListItemType; views: number }[] {
  const ranked = posts
    .filter(({ node: { fields: { slug } } }) => viewsBySlug[slug] > 0)
    .map(post => ({ post, views: viewsBySlug[post.node.fields.slug] }))
    .sort(
      (a, b) =>
        b.views - a.views ||
        b.post.node.frontmatter.date.localeCompare(a.post.node.frontmatter.date) ||
        a.post.node.frontmatter.title.localeCompare(b.post.node.frontmatter.title),
    )
  return limit ? ranked.slice(0, limit) : ranked
}
