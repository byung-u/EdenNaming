Eden Naming
============
- 작명 서비스 제공
- 개인 용도, 일부 정보는 비공개함

작명
--
- 경우의 수를 줄이는 것이 관건
  - 선천명과의 합국 조화 관계 (생년월일시를 기준으로 사주팔자법)
  - 수리영동 조직관계
  - 음양 배열 관계
  - 오행의 배치 관계
  - 자의 정신 관계
  - 음령 오행의 역상 관계
  - 수리 역상의 관계
  - 어휘 어감의 조정 관계

참조
--

#### 논문
소리성명학의 理論과 特性에 관한 연구 (안종희) 공주대학교 석사학위 논문, 2016
성명학(姓名學)에 대한 인식 (金栢滿 김백만, 새국어생활, Vol.1 No.1, [1991])

#### SITE
- 갑자: https://namu.wiki/w/갑자
- 인명한자: http://help.scourt.go.kr/nm/img/hanja/hanja_2015.pdf
- 긍정어, 부정어 분류: http://newpower.tistory.com/127 
- [긍정, 부정 데이터](https://github.com/The-ECG/BigData1_1.3.3_Text-Mining/blob/master/dictionary.zip)
  - 모든 이름을 긍정/부정 비교하다보니 너무 느려서 관련 로직은 제거
- 일반 단어 제외 목록
  - [국립국어원](http://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71)
  - [영어단어 13000 다운로드](https://doc-0c-9s-docs.googleusercontent.com/docs/securesc/tec3bh8hdd1rjv0g5vd8td6522dcvi0k/skbq5ftun284uu34e9crd9gri3cupioc/1496210400000/11093551788895655914/14549008824345722584/0B4O_EqeoWv_EYWtQWXdOVW5ORGs?e=download&nonce=eed9hrem67510&user=14549008824345722584&hash=aj8che5ps7lc6o8rc4pfutotvfeucu8k)
- [Unicode 한글](http://jjeong.tistory.com/696)

VIM command
-----------
- ,(comma) to \n(newline)
`:%s/,\ /\r/g`

Release
-------
- 0.7.0 (current)
  - Code refactoring
  - Test

- 0.6.0 (June, 16 Friday 2017)
  - 기존 계획했던 기능 구현 완료
  - 기본 test

- 0.5.0 (June, 8 Thursday 2017)
  - 서버에서 처리할 기본 구현 완료
  - Django 메뉴 추가

- 0.4.0 (June, 2 Friday 2017)
  - Django를 이용하여 flatpage 구현 완료
  - 작명 결과 이름 로직 전체 수정

- 0.3.0 (May, 31 Wednesday 2017)
  - Django를 이용하여 로그인, 및 기본 기능 구현 완료

- 0.2.0 (May, 22 Monday 2017)
  - 작명에 사용할 한자 정보 수집하여 DB세팅 완료

- 0.1.0 (May, 15 Monday 2017)
  - 작명 할 한자 정보 수집
  - Django 자체 스터디
