import React, { FunctionComponent, useEffect, useState } from 'react'
import styled from '@emotion/styled'
import { fetchViewCount, getGoatCounterBase } from 'utils/analytics'

type ViewCounterProps = {
  path: string
  // 배포 빌드 때 통계 API 에서 받은 값 (실시간 카운터를 못 읽을 때만 사용)
  fallbackViews?: number
}

const Counter = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-left: 12px;
  font-variant-numeric: tabular-nums;

  @media (max-width: 768px) {
    margin-left: 8px;
  }
`

// 실제 집계값이 있을 때만 표시. 기능이 꺼졌거나 데이터가 없으면 아무것도 그리지 않는다
const ViewCounter: FunctionComponent<ViewCounterProps> = function ({
  path,
  fallbackViews,
}) {
  const [views, setViews] = useState<number | null>(null)
  const [live, setLive] = useState(false)

  useEffect(() => {
    setViews(null)
    setLive(false)
    if (!getGoatCounterBase()) return undefined
    const controller =
      typeof AbortController !== 'undefined' ? new AbortController() : undefined
    fetchViewCount(path, controller && controller.signal).then(count => {
      if (count === null) return
      setViews(count)
      setLive(true)
    })
    return () => controller && controller.abort()
  }, [path])

  const shown = views !== null ? views : fallbackViews
  if (shown === undefined || shown === null) return null
  const formatted = shown.toLocaleString('ko-KR')

  return (
    <Counter
      aria-label={`조회수 ${formatted}회`}
      title={live ? 'GoatCounter 방문 수 (최대 몇 시간 지연)' : '마지막 배포 시점 집계'}
    >
      <span aria-hidden="true">👁</span>
      <span aria-hidden="true">조회수 {formatted}</span>
    </Counter>
  )
}

export default ViewCounter
