import React, { useState, useEffect } from 'react'
import styled from '@emotion/styled'

const ScrollToTopButton = styled.button`
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(60deg, rgb(66, 105, 78) 0%, rgb(73, 110, 93) 100%);
  border: 2px solid white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px);

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    background: white;
    border-color: rgb(66, 105, 78);
  }

  &:active {
    transform: translateY(0);
  }

  &.visible {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }

  @media (max-width: 768px) {
    bottom: 20px;
    right: 20px;
    width: 45px;
    height: 45px;
  }
`

const ArrowIcon = styled.div`
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 12px solid white;
  margin-bottom: 2px;
  transition: border-bottom-color 0.3s ease;

  ${ScrollToTopButton}:hover & {
    border-bottom-color: rgb(66, 105, 78);
  }
`

interface ScrollToTopProps {
  showBelow?: number
}

const ScrollToTop: React.FC<ScrollToTopProps> = ({ showBelow = 400 }) => {
  const [show, setShow] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > showBelow) {
        setShow(true)
      } else {
        setShow(false)
      }
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [showBelow])

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }

  return (
    <ScrollToTopButton 
      onClick={scrollToTop}
      className={show ? 'visible' : ''}
      aria-label="맨 위로 이동"
    >
      <ArrowIcon />
    </ScrollToTopButton>
  )
}

export default ScrollToTop
