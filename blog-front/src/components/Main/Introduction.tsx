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
          <SubTitle>Hello World, I'm</SubTitle>
          <Title>Forest_LIM 🌲</Title>
          <Description>
            A Junior Frontend Developer passionate about <strong>clean UI</strong> and <strong>creative UX</strong>.<br />
            I enjoy learning new technologies and building something meaningful with code.
          </Description>
        </Right>
      </Wrapper>
    </Background>
  )
}

export default Introduction

// 🎨 Styled Components

const Background = styled.div`
  width: 100%;
  background: linear-gradient(60deg, #29323c 0%, #485563 100%);
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

  strong {
    color: #ffffff;
  }

  @media (max-width: 768px) {
    font-size: 14px;
  }
`
