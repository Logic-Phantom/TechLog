import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
import { IGatsbyImageData } from 'gatsby-plugin-image'
import ProfileImage from 'components/Main/ProfileImage'

type IntroductionProps = {
  profileImage: IGatsbyImageData
}

const Introduction: FunctionComponent<IntroductionProps> = ({ profileImage }) => {
  return (
    <Background>
      <Wrapper>
        <Left>
          <StyledProfileImage profileImage={profileImage} />
        </Left>
        <Right>
          <SubTitle>안녕하세요,</SubTitle>
          <Title>Forest_LIM🌿</Title>
          <Description>
            끊임없이 배우고, 성장하며<br />
            사용자에게 더 나은 경험을 선물하는 개발자입니다.
          </Description>
          <PWASection>
            <PWATitle>📱블로그 앱처럼 사용하기</PWATitle>
            <PWADescription>
              이 블로그는 PWA를 지원합니다. 모바일에서 홈 화면에 추가하여<br />
              네이티브 앱처럼 사용할 수 있습니다.
            </PWADescription>
            <PWAInstructions>
              <InstructionItem>1. 모바일 브라우저에서 블로그 접속</InstructionItem>
              <InstructionItem>2. 브라우저 메뉴에서 "홈 화면에 추가" 선택</InstructionItem>
              <InstructionItem>3. 앱 아이콘을 통해 언제든지 블로그 접속 가능</InstructionItem>
            </PWAInstructions>
          </PWASection>
        </Right>
      </Wrapper>
    </Background>
  )
}

export default Introduction

// 🎨 Styled Components

const Background = styled.div`
  width: 100%;
  background: linear-gradient(60deg,rgb(66, 105, 78) 0%,rgb(73, 110, 93) 100%);
  color: #ffffff;
  padding: 60px 20px;
`

const Wrapper = styled.div`
  display: flex;
  align-items: center;
  max-width: 960px;
  margin: 0 auto;

  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
  }
`

const Left = styled.div`
  flex-shrink: 0;
  margin-right: 40px;

  @media (max-width: 768px) {
    margin-right: 0;
    margin-bottom: 20px;
  }
`

const StyledProfileImage = styled(ProfileImage)`
  border-radius: 50%;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  width: 160px;
  height: 160px;
  overflow: hidden;
`

const Right = styled.div`
  flex: 1;
`

const SubTitle = styled.div`
  font-size: 18px;
  color: #ccc;
  margin-bottom: 8px;

  @media (max-width: 768px) {
    font-size: 16px;
  }
`

const Title = styled.div`
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 16px;

  @media (max-width: 768px) {
    font-size: 24px;
  }
`

const Description = styled.div`
  font-size: 16px;
  line-height: 1.6;
  color: #eee;
  margin-bottom: 24px;

  strong {
    color: #ffffff;
  }

  @media (max-width: 768px) {
    font-size: 14px;
  }
`

const PWASection = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
`

const PWATitle = styled.div`
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
  color: #ffffff;
`

const PWADescription = styled.div`
  font-size: 14px;
  line-height: 1.6;
  color: #eee;
  margin-bottom: 16px;
`

const PWAInstructions = styled.div`
  font-size: 14px;
  color: #eee;
`

const InstructionItem = styled.div`
  margin-bottom: 8px;
  padding-left: 16px;
  position: relative;

  &:before {
    content: "•";
    position: absolute;
    left: 0;
    color: #ffffff;
  }
`
