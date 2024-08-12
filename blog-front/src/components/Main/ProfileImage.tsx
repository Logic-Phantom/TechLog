import React, { FunctionComponent } from 'react'
import styled from '@emotion/styled'
//import { GatsbyImage, IGatsbyImageData } from 'gatsby-plugin-image'
import { GatsbyImage, IsbyImageData } from 'gatsby-plugin-image' //lazyloading

// 자신이 원하는 프로필 이미지 링크로 설정해주세요.
// const PROFILE_IMAGE_LINK =
//   '<https://avatars.githubusercontent.com/u/24629040?s=460&u=0bb3411f25c0e1c5d25d753fc648739367cb7032&v=4>'
const PROFILE_IMAGE_LINK = 'https://github.com/codemasterli/TechLog/blob/main/blog-front/contents/20240809.jpg?raw=true';

type ProfileImageProps = {
  profileImage: IGatsbyImageData
}

//const ProfileImageWrapper = styled(GatsbyImage)` lazyloading
const ProfileImageWrapper = styled.img`
  width: 125px;
  height: 125px;
  margin-bottom: 30px;
  border-radius: 50%;
  object-fit: cover;
  image-rendering: -webkit-optimize-contrast; /* For sharper image rendering */
 
  @media (max-width: 768px) {
    width: 80px;
    height: 80px;
  }
  `

  // const ProfileImage: FunctionComponent<ProfileImageProps> = function ({ lazyloading
  //   profileImage,
  // }) {
  //   return <ProfileImageWrapper image={profileImage} alt="Profile Image" />
  // }
  
  const ProfileImage: FunctionComponent = function () {
    return <ProfileImageWrapper src={PROFILE_IMAGE_LINK} alt="Profile Image" />
  }

  export default ProfileImage