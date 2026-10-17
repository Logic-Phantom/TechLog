import React, { FunctionComponent, useEffect, useRef, useState } from 'react'
import styled from '@emotion/styled'
import { trackEvent } from 'utils/analytics'

type PostShareProps = {
  title: string
  url: string // canonical URL
  slug: string
}

const ShareWrapper = styled.section`
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  width: 768px;
  margin: 80px auto 0;
  padding-top: 30px;
  border-top: 1px solid rgba(66, 105, 78, 0.2);

  @media (max-width: 768px) {
    width: 100%;
    margin-top: 50px;
    padding: 20px 20px 0;
  }
`

const ShareButton = styled.button`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid rgb(66, 105, 78);
  border-radius: 20px;
  background: #ffffff;
  color: rgb(66, 105, 78);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;

  &:hover {
    background: rgb(66, 105, 78);
    color: #ffffff;
  }

  &:focus-visible {
    outline: 3px solid rgba(66, 105, 78, 0.4);
    outline-offset: 2px;
  }

  @media (max-width: 768px) {
    font-size: 14px;
  }
`

const Feedback = styled.span`
  font-size: 14px;
  color: #426950;
`

// 클립보드 API 가 없거나 거부되면 textarea + execCommand 로 한 번 더 시도
const copyText = async function (text: string): Promise<boolean> {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
      return true
    }
  } catch (e) {
    // 아래 대체 방식으로 진행
  }
  try {
    const textarea = document.createElement('textarea')
    textarea.value = text
    textarea.setAttribute('readonly', '')
    textarea.style.position = 'fixed'
    textarea.style.opacity = '0'
    document.body.appendChild(textarea)
    textarea.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(textarea)
    return ok
  } catch (e) {
    return false
  }
}

const PostShare: FunctionComponent<PostShareProps> = function ({ title, url, slug }) {
  const [canShare, setCanShare] = useState(false)
  const [message, setMessage] = useState('')
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)

  // SSR 결과와 맞추기 위해 Web Share 지원 여부는 마운트 후에 판단
  useEffect(() => {
    setCanShare(typeof navigator !== 'undefined' && typeof navigator.share === 'function')
    return () => {
      if (timer.current) clearTimeout(timer.current)
    }
  }, [])

  const notify = (text: string) => {
    setMessage(text)
    if (timer.current) clearTimeout(timer.current)
    timer.current = setTimeout(() => setMessage(''), 2500)
  }

  const handleCopy = async () => {
    const ok = await copyText(url)
    notify(ok ? '링크를 복사했습니다.' : '복사하지 못했습니다. 주소창의 링크를 이용해 주세요.')
    if (ok) trackEvent('copy_link', { content_type: 'post', item_id: slug })
  }

  const handleShare = async () => {
    if (typeof navigator.share !== 'function') {
      handleCopy()
      return
    }
    try {
      await navigator.share({ title, url })
      trackEvent('share_click', { method: 'web_share', content_type: 'post', item_id: slug })
    } catch (e) {
      // 사용자가 공유 창을 닫은 경우(AbortError)는 조용히 무시, 그 외 실패는 복사로 대체
      if (!(e instanceof Error && e.name === 'AbortError')) handleCopy()
    }
  }

  return (
    <ShareWrapper aria-label="게시글 공유">
      {canShare && (
        <ShareButton type="button" onClick={handleShare} aria-label="이 글 공유하기">
          <span aria-hidden="true">📤</span> 공유하기
        </ShareButton>
      )}
      <ShareButton type="button" onClick={handleCopy} aria-label="이 글 링크 복사">
        <span aria-hidden="true">🔗</span> 링크 복사
      </ShareButton>
      <Feedback role="status" aria-live="polite">
        {message}
      </Feedback>
    </ShareWrapper>
  )
}

export default PostShare
