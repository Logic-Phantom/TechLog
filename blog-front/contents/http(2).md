---
date: '2024-11-25'
title: '네트워크(2)'
categories: ['HTTP','NetWork']
summary: 'DNS와 URI에 대하여..'
thumbnail: './images/http/NetWork.png'
---
## 들어가며
게속해서 이전의 작성한 주제와 같이 네트워크에 대하여 좀 더 알아보도록 하자.

---
먼저 DNS 라는 용어가 있다. 프로젝트를 진행하면서 DNS라는 용어를 많이 들어봤을거다. 이 용어를 명확히 파악하지 않고, 대강 어떠한 것이겠거니 하면서 사용을 해왔는데, 이번에 한번 제대로 알아보자.

## DNS ...?
IP 같은경우 기억하기가 대체적으로 어렵고, 변경 될 가능성도 있다. 
그 이유는 xxx.xxx.xxx.xx 를 전부 알아야 하기 때문이다. 그렇기 때문에 사용자에게 좀더 친근하게 어떠한 이름으로 작성할 수 있는 DNS 를 사용한다. 

<ex. DNS 서버 >  
|도메인명|IP|
|:---:|:---:|
|google.com|200.200.200.2|

 
상단의 표와 같이 DNS 서버에서 관리할 수 있다 이렇게 관리가 되면 IP 가 변경되더라도 사용자는 도메인명을 통하여 검색 할 수있게 설정 한다. 

## URI 와 웹 브라우저 요청 흐름
> URI(Uniform Resource Identifier)
Uniform : 리소스 식별하는 통일된 방식
Resource : 자원, URI로 식별 할 수 있는 모든 것(제한 없음)
Identifier: 다른 항목과 구분하는데 필요한 정보 

  URI는 로케이터,이름 또는 둘다 추가로 불류 될 수 있다. 
  결국 Resuorce의 정체성을 표현하는 가장 큰 영역이라고 생각하면 된다. 
  URI의 경우 제일 큰 영역이고, 그안에 URL, URN이 존재한다.
  
  ![](./images/http/URi.png)  

## URL(Uniform Resource Locator)

 URL 은 간단히 이야기하면 소스경로 라고 생각 하면된다. 

간단하게 우리가 아는 웹 브라우저 URL 이 있다고 가정하자.
```
https:ww.google.com/search?q=hello&hl=ko
```
이러한 URL 이 있다고 했을때, URL에 정해져 있는 문법은 하단과 같다.
```
scheme://[userinfo@]host[:port][/path][?query][#fragment]
```

> scheme: scheme는 주로 프로토콜 사용(프로토콜은 어떤 방식으로 자원에 접글할 것인가 하는 약속 규칙)http, thhps ,ftp 등등  
>userinfo: URL 사용자정보를 포함해서 사용(거의 사용안함)  
>host: 호스트명 (도메인명)  
>port:접속 포트 (일반적으로 생략)  
>path :소스 경로, 계층적 구조(ex ./home/file1.jpg)  
>query :key=value 형태 ? 시작, &로 추가기능 ?keyA=valueA&keyB=valueB, 보통은 query >parameter, query string 등으로 불림, 웹서버에 제공하는 파라미터, 문자형태이기 떄문   
>fragment: 잘사용하지 않음 html내부 북마크등에 사용 (서버 전송 정보는 아님)  

## URN(Uniform Resource Name)
 
  URN은 이름을 설정하는것인데 URN은 특정이름 지정이라 일반적인 사용자는 찾을 수 없다. 
  
> URI가 더 범위가 큰 영역이고 URL과 같은 의미로 생각하면 된다. 

## 웹브라우저 요청 흐름
https:ww.google.com/search?q=hello&hl=ko 요청을 보내면 
DNS 서버에서 IP를 조회한다.(:ww.google.com 이걸 조회하겠지)
1. 웹브라우저 http 메시지 생성
   ![](./images/http/http_req.png)   
2. 소켓 라이브러리 통해 데이터 전달 TCP/IP로 패킷 정보 만듬
3. 서버에 요청패킷 도착
4. TCP/IP 패킷 버리고 메시지 해석
5. HTTP 응답 메시지 (상태 코드, 어떤 파일인지, 인코딩 형식, 파일 길이 같은 것들을 포함)
   ![](./images/http/http_res.png)
6. 클라이언트에서 응답패킷 (html 이 되겠지) 확인 

---