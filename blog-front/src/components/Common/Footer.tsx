import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'

const FooterWrapper = styled.footer`
  position: relative;
  width: 100%;
  padding: 40px 0;
  background: linear-gradient(180deg, rgba(66, 105, 78, 0.05) 0%, rgba(73, 110, 93, 0.1) 100%);
  border-top: 1px solid rgba(66, 105, 78, 0.1);
`

const FooterContent = styled.div`
  max-width: 960px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
`

const Message = styled.p`
  font-size: 16px;
  line-height: 1.6;
  color: #426950;
  margin-bottom: 10px;
  transition: color 0.3s ease;

  &:hover {
    color: #2c4735;
  }

  @media (max-width: 768px) {
    font-size: 14px;
  }
`

const Copyright = styled.p`
  font-size: 14px;
  color: #666;
  margin-top: 5px;

  @media (max-width: 768px) {
    font-size: 12px;
  }
`

const Emoji = styled.span`
  display: inline-block;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.2) rotate(10deg);
  }
`

const Footer: FunctionComponent = function () {
  return (
    <FooterWrapper>
      <FooterContent>
        <Message>
          Thank You for Visiting My Blog, Have a Good Day <Emoji>🌿</Emoji>
        </Message>
        <Copyright>© 2024 Developer LIM.</Copyright>
      </FooterContent>
    </FooterWrapper>
  )
}

export default Footer