const fs = require('fs');
const path = require('path');
const { createFilePath } = require(`gatsby-source-filesystem`);

// scripts/fetch_stats.py 가 배포 빌드 직전에 만드는 공개 조회수 데이터 (없으면 통계 기능만 꺼짐)
const STATS_FILE = path.resolve(__dirname, 'static/data/popular-posts.json');
const RELATED_POST_COUNT = 4;

// 선택 필드는 스키마에 미리 선언해 두어, 기존 글에 없어도 쿼리가 깨지지 않게 한다
exports.createSchemaCustomization = ({ actions }) => {
  actions.createTypes(`
    type MarkdownRemarkFrontmatter {
      tags: [String]
      updatedAt: Date @dateformat
    }

    type SiteStatsPost {
      path: String!
      views: Int!
    }

    type SiteStats implements Node @dontInfer {
      available: Boolean!
      source: String
      metric: String
      generatedAt: Date @dateformat
      rangeStart: Date @dateformat
      rangeEnd: Date @dateformat
      totalViews: Int
      posts: [SiteStatsPost!]!
    }
  `);
};

const readStats = reporter => {
  if (!fs.existsSync(STATS_FILE)) return null;
  try {
    const raw = JSON.parse(fs.readFileSync(STATS_FILE, 'utf8'));
    const posts = (Array.isArray(raw.posts) ? raw.posts : [])
      .filter(p => p && typeof p.path === 'string' && Number.isInteger(p.views) && p.views >= 0)
      .map(p => ({ path: p.path, views: p.views }));
    return {
      available: posts.length > 0 || Number.isInteger(raw.totalViews),
      source: typeof raw.source === 'string' ? raw.source : null,
      metric: typeof raw.metric === 'string' ? raw.metric : null,
      generatedAt: raw.generatedAt || null,
      rangeStart: raw.rangeStart || null,
      rangeEnd: raw.rangeEnd || null,
      totalViews: Number.isInteger(raw.totalViews) ? raw.totalViews : null,
      posts,
    };
  } catch (e) {
    reporter.warn(`[stats] ${STATS_FILE} 를 읽지 못해 통계 없이 빌드합니다: ${e.message}`);
    return null;
  }
};

// 통계 파일이 없어도 siteStats 노드는 항상 만들어(available:false) 페이지 쿼리가 실패하지 않게 한다
exports.sourceNodes = ({ actions, createNodeId, createContentDigest, reporter }) => {
  const stats = readStats(reporter) || {
    available: false,
    source: null,
    metric: null,
    generatedAt: null,
    rangeStart: null,
    rangeEnd: null,
    totalViews: null,
    posts: [],
  };
  actions.createNode({
    ...stats,
    id: createNodeId('site-stats'),
    internal: { type: 'SiteStats', contentDigest: createContentDigest(stats) },
  });
};

// 관련 글 계산 (빌드 시점): 공통 카테고리 > 공통 태그 > 제목·요약 키워드, 동점이면 최신순 → 부족하면 최신 글로 보충
const STOP_WORDS = new Set(['완벽', '가이드', '정리', '이해', '활용', '방법', '그리고', 'the', 'and', 'for', 'with', 'api', 'web']);
const keywords = text =>
  new Set(
    (text || '')
      .toLowerCase()
      .replace(/[^0-9a-z가-힣\s]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length >= 2 && !STOP_WORDS.has(w)),
  );
const lower = list => new Set((list || []).filter(Boolean).map(v => String(v).toLowerCase()));
const countShared = (a, b) => [...a].filter(v => b.has(v)).length;

const computeRelated = posts => {
  const prepared = posts.map(({ fields: { slug }, frontmatter }) => ({
    slug,
    date: frontmatter.date || '',
    categories: lower(frontmatter.categories),
    tags: lower(frontmatter.tags),
    words: keywords(`${frontmatter.title || ''} ${frontmatter.summary || ''}`),
  }));
  const byRecency = (a, b) =>
    b.date.localeCompare(a.date) || a.slug.localeCompare(b.slug);
  const latest = [...prepared].sort(byRecency);

  const related = {};
  prepared.forEach(current => {
    const scored = prepared
      .filter(other => other.slug !== current.slug)
      .map(other => ({
        ...other,
        score:
          countShared(current.categories, other.categories) * 10 +
          countShared(current.tags, other.tags) * 5 +
          Math.min(countShared(current.words, other.words), 3),
      }))
      .filter(other => other.score > 0)
      .sort((a, b) => b.score - a.score || byRecency(a, b))
      .slice(0, RELATED_POST_COUNT)
      .map(other => other.slug);

    for (const other of latest) {
      if (scored.length >= RELATED_POST_COUNT) break;
      if (other.slug !== current.slug && !scored.includes(other.slug)) scored.push(other.slug);
    }
    related[current.slug] = scored;
  });
  return related;
};

// Setup Import Alias
exports.onCreateWebpackConfig = ({ getConfig, actions }) => {
  const output = getConfig().output || {};

  actions.setWebpackConfig({
    output,
    resolve: {
      alias: {
        components: path.resolve(__dirname, 'src/components'),
        utils: path.resolve(__dirname, 'src/utils'),
        hooks: path.resolve(__dirname, 'src/hooks'),
      },
    },
  });
};

// Generate a Slug Each Post Data
exports.onCreateNode = ({ node, getNode, actions }) => {
  const { createNodeField } = actions;

  if (node.internal.type === `MarkdownRemark`) {
    const slug = createFilePath({ node, getNode });

    createNodeField({ node, name: 'slug', value: slug });
  }
};

// Generate Post Page Through Markdown Data
exports.createPages = async ({ actions, graphql, reporter }) => {
  const { createPage } = actions;

  // Get All Markdown File For Paging
  const queryAllMarkdownData = await graphql(
    `
      {
        allMarkdownRemark(
          sort: [{frontmatter: {date: DESC}}, {frontmatter: {title: ASC}}]
        ) {
          edges {
            node {
              fields {
                slug
              }
              frontmatter {
                title
                summary
                date(formatString: "YYYY-MM-DD")
                categories
                tags
              }
            }
          }
        }
      }
    `,
  );

  // Handling GraphQL Query Error
  if (queryAllMarkdownData.errors) {
    reporter.panicOnBuild(`Error while running query`);
    return;
  }

  // Import Post Template Component
  const PostTemplateComponent = path.resolve(
    __dirname,
    'src/templates/post_template.tsx',
  );

  const relatedBySlug = computeRelated(
    queryAllMarkdownData.data.allMarkdownRemark.edges.map(({ node }) => node),
  );

  // Page Generating Function
  const generatePostPage = ({
    node: {
      fields: { slug },
    },
  }) => {
    const pageOptions = {
      path: slug,
      component: PostTemplateComponent,
      context: { slug, relatedSlugs: relatedBySlug[slug] || [] },
    };

    createPage(pageOptions);
  };

  // Generate Post Page And Passing Slug Props for Query
  queryAllMarkdownData.data.allMarkdownRemark.edges.forEach(generatePostPage);
};