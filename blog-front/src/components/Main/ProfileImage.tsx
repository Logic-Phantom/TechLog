import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
import { GatsbyImage, IGatsbyImageData } from 'gatsby-plugin-image'
//import { GatsbyImage, IsbyImageData } from 'gatsby-plugin-image' //lazyloading

// 자신이 원하는 프로필 이미지 링크로 설정해주세요.
// const PROFILE_IMAGE_LINK =
//   '<https://avatars.githubusercontent.com/u/24629040?s=460&u=0bb3411f25c0e1c5d25d753fc648739367cb7032&v=4>'
const PROFILE_IMAGE_LINK = 'https://github.com/logic-phantom/TechLog/blob/main/blog-front/contents/20240809.jpg?raw=true';

type ProfileImageProps = {
  profileImage: IGatsbyImageData
}
//lazyloading
//const ProfileImageWrapper = styled.img`
const ProfileImageWrapper = styled(GatsbyImage)` 
  width: 150px;
  height: 150px;
  margin-bottom: 30px;
  border-radius: 15px;
  object-fit: cover;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
  }

  @media (max-width: 768px) {
    width: 100px;
    height: 100px;
    border-radius: 12px;
  }
`
 //lazy
  const ProfileImage: FunctionComponent<ProfileImageProps> = function ({ 
    profileImage,
  }) {
    return <ProfileImageWrapper image={profileImage} alt="Profile Image" />
  }
  
  // const ProfileImage: FunctionComponent = function () {
  //   return <ProfileImageWrapper src={PROFILE_IMAGE_LINK} alt="Profile Image" />
  // }

  export default ProfileImage