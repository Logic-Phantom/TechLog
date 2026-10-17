/**
 * Implement Gatsby's Browser APIs in this file.
 *
 * See: https://www.gatsbyjs.com/docs/reference/config-files/gatsby-browser/
 */

// You can delete this file if you're not using it
import 'prismjs/themes/prism-tomorrow.css';
import { trackPageView } from './src/utils/analytics';

// 최초 진입과 SPA 이동(링크·뒤로/앞으로 가기) 모두에서 호출된다. 분석 스크립트가 없으면 아무 일도 하지 않음
export const onRouteUpdate = ({ location, prevLocation }) => {
  trackPageView(location, !prevLocation);
};
