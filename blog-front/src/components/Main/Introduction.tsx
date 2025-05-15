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
      <Card>
        <ImageWrapper>
          <StyledProfileImage profileImage={profileImage} />
        </ImageWrapper>
        <TextContent>
          <SubTitle>안녕하세요,</SubTitle>
          <Title>Forest_LIM 입니다 🌿</Title>
          <Description>
            끊임없이 배우고, 성장하며<br />
            사용자에게 더 나은 경험을 선물하는 프론트엔드 개발자입니다.
          </Description>
        </TextContent>
      </Card>
    </Background>
  )
}

export default Introduction

// 🎨 Styled Components (변경 없음)

const Background = styled.div`
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #ece9e6 0%, #ffffff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
`

const Card = styled.div`
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  padding: 40px;
  display: flex;
  gap: 40px;
  align-items: center;
  max-width: 900px;
  width: 100%;

  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
`

const ImageWrapper = styled.div`
  flex-shrink: 0;
`

const StyledProfileImage = styled(ProfileImage)`
  width: 160px;
  height: 160px;
  border-radius: 50%;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
`

const TextContent = styled.div`
  flex: 1;
`

const SubTitle = styled.div`
  font-size: 20px;
  color: #666;
  margin-bottom: 8px;
`

const Title = styled.div`
  font-size: 36px;
  font-weight: 800;
  color: #222;
  margin-bottom: 16px;
`

const Description = styled.div`
  font-size: 18px;
  line-height: 1.7;
  color: #444;
`
