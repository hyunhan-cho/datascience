
* Chapter 01. STATA 시작하기

1. Stata 소개

• 1980년대 중반 미국의 StataCorp이 개발한 통계 소프트웨어 패키지
• Statistics와 Data의 합성어
• 경제학, 사회학, 정치학, 의학 등 다양한 사회과학과 자연과학에서 이용
• Stata의 장점
  ○ Stata는 통계분석은 물론 데이터 관리와 그래픽에서 탁월한 능력을 발휘
  ○ Stata는 광범위한 내용의 통계분석이 가능하여 매우 다양한 분야의 사용자들의 요구에
부합
  ○ Stata는 인터넷과의 상호작용을 통해 다양한 부가적인 기능을 이용할 수 있음
  ○ Stata는 가격과 유지비용이 타 통계프로그램에 비해 저렴
• 관련 웹사이트
  ○ http://www.stata.co.kr : 한국STATA학회
  ○ http://www.stata.com : StataCorp
  ○ http://cafe.naver.com/stata : STATA이용자 카페

2. Stata 켜기: 창(window)

• Command 창

  ○ 실행하고자 하는 명령어(command)를 입력하는 창
  ○ 예) sysuse auto : auto.dta 파일 불러오기
  ○ 예) browse : 데이터 스프레드쉬트 보기
  ○ 예) edit : 데이터 스프레드쉬트 편집
  ○ 예) summarize price
  ○ Tip : tab 키 사용하면 변수이름이 자동으로 완성
  ○ Stata 명령문이 실행되어 결과가 제시되는 창
  ○ 블록으로 선택한 후 : Copy text / Copy Table을 이용하여 다른 문서작성 프로그램에 붙
여넣기 할 수 있음

• Result 창
  ○ Stata 명령문이 실행되어 결과가 제시되는 창
  ○ 블록으로 선택한 후 : Copy text / Copy Table을 이용하여 다른 문서작성 프로그램에 붙
여넣기 할 수 있음

• Review 창
  ○ Command 창에 입력한 명령문이 모이는 장소
  ○ 문법에 맞지 않아 에러가 발생한 명령문은 빨간 색으로 표시
  ○ Review창에 커서를 놓고 오른쪽 마우스 클릭을 하면 Save all을 이용하여 Review 창에 모
여 있는 명령문을 하나의 텍스트 파일로 저장할 수 있음

• Variables 창
  ○ 데이터 파일에 포함되어 있는 변수이름, 변수의 레이블, 변수의 포멧 형태를 보여줌
  ○ 변수이름은 32글자(영문)까지 가능
  ○ 변수레이블은 80글자(영문)까지 가능 : 한글로는 40자
  
3. 데이터파일 불러오기

• 기존 데이터 파일 불러오기

  a. File > Open 을 이용 원하는 디렉터리에서 필요한 파일을 불러오기
  b. sysuse auto.dta : 시스템 상의 데이터 사용하기
  c. Use http://www.stata-press.com/data/r9/auto.dta : web 데이터 불러오기
  d. Webuse auto : web 데이터 불러오기

  save "/Users/swj/Library/CloudStorage/Dropbox/TEACHING/2024년 2학기/온라인데이터커뮤니케이션/auto.dta"

  sysuse auto
  
  
  
  use "/Users/swj/Library/CloudStorage/Dropbox/다운로드 드롭박스/auto.dta"
  
sum price
  
  sum
  
   save "/Users/swj/Library/CloudStorage/Dropbox/다운로드 드롭박스/auto.dta", replace

  
  sum // 요약통계
  
  
  
• 데이터를 직접 입력하는 방법
  ○ DATA Editor 창을 이용하는 방법 : 프로그래밍을 하는 경우 입력이 불가능
  ○ Input 명령어 이용하는 방법
     예제) input aa bb cc // 1 2 3 // 4 5 6 // 7 8 9 // end
• Clear : 로딩된 모든 데이터 삭제



4. STATA 관련 디렉터리

sysdir

sysuse auto

5. 명령어와 대화창(dialog box :db)
• 예제) sysuse auto // db summarize
• 예제) summarize price mpg
   ○ Option syntax : 명령어 , 이후
• 예제) summarize price mpg, detail
• 기타 : sysdir - stata 관련 디렉토리



6. Help 메뉴이용법

• 예제) 

help summarize



7. 작업환경 설정과 업데이트

• 기본 설정 상태 확인 : set

• 메모리 설정
  ○ Query memory : 메모리 설정
  ○ Set memory 300m, perm

• Output 설정
  ○ Query output : output 설정
  ○ Set more off, perm

  
  
  sum price
  sum make
  

8. 업데이트
  ○ Update all 
  
  
  

Chapter 02. 로그파일과 데이터파일

1. 로그파일의 종류와 작성

• 로그파일은 Results 창에 나오는 모든 명령문과 output을 텍스터 파일형태로 저장한 파일

  ○ Result 화면이 보관할 수 있는 내용의 용량은 32KB로 실행 결과물이 많을 경우 원하는 결과들이
 Results 화면에서 사라져 없어질 수 있음
  ○ 따라서 Stata로 작업을 시작하기 전에 로그파일 이름을 지정할 경우, 나중에 저장된 로그파일을 이용
하여 자신이 실행했던 모든 결과물들을 열람 혹은 편집할 수 있음

• 로그파일 종류
  ○ *.smcl 형식
    - Result화면과 동일한 형태로 한눈에 보기에 용이하며 프린트하는 경우 Stata화면처럼 깔끔하게
나옴
    - 그러나 Stata에서만 불러올 수 있고 한글이나 MS-Word 같은 문서작성 프로그램에서 불러올 수
없는 단점이 존재

  ○ *.log 형식
    - 일반적인 텍스트 파일의 한 종류로 한글이나 MS-Word와 같은 문서작성 프로그램에서 불러올
수 있고 편집도 가능
    - Stata의 Result 화면과 달라 줄이 안 맞거나 폰트가 많이 달라짐.

• 로그파일 지정하는 방법
  a. 메뉴 : File > Log > Begin을 선택
  b. Command창에 입력 : log using "C:\data\log1.smcl"
• 로그파일 실행을 마치는 방법  
  a. 메뉴 : File > Log > Close
  b. Command 창에 입력 : log close
• 기존에 만들었던 로그파일을 이어 사용하는 방법
  ○ 기존의 로그파일을 다시 지정.
  ○ 관련 옵션
  i. View existing file(read-only)
  ii. Append to existing file :
  iii. Overwirte existing file :

   
2. STATA 데이터 파일의 형태와 종류

• 각 열(column)은 변수(variable)을 의미하며
• 각 행(row)은 관측치(observation)를 나타냄
• 자료 특성
  ○ 변수의 값이 숫자인 경우 숫자변수(numeric variable)
  ○ 변수의 값이 문자인 경우 문자(string) →
  
  
3. 데이터의 저장 형태(storage type)  
  
• 데이터 파일(sysuse auto)을 불러들인 후 Command 창에 describe 실행

  ○ 로딩한 자료에 대해 다양한 정보를 제공
  ○ 변수 개수, 관측치 수, 사용하고 있는 메모리의 크기, 각 변수에 대한 저장형태
• 변수의 저장형태 : storage type
  ○ Byte : 0과 1을 가지는 더미변수에 주로 사용, 이산형 변수*
  ○ Int : 정수 값을 갖는 숫자 변수
  ○ Long : 더 큰 정수 값을 가지는 변수
  ○ Float : default 저장형태로 실수
  ○ Double : 더 큰 실수의 저장 형태
  ○ String : 문자변수 저장형태
    - Str18 : 문자의 최대 길이가 18개 글자인 문자변수
  
• 저장형태는 숫자변수인 경우 STATA에서 자동으로 지정


4. 데이터의 디스플레이 포멧(display format)
• "data2_1.dta" 파일이용
• 숫자 포멧은 값은 같아도 다르게 보이게 표현할 수 있음
  ○ e_fmt : 자리수가 많은 경우 이용.
   - 3.06e 􀵅 06 􀵌 3.96 􀵈 10􀬺 􀵌 3,690,000
   - %9.2e : 9는 전체 숫자를 표현할 수 있는 최대자리수, .2는 소수점 이하 자리수, e는 e-format
  ○ f_fmt : fixed format으로 소수점 이하 자릿수를 고정시키고자 할 때 이용
   - %9.2f : 9는 전체 숫자를 표현할 수 있는 최대자리수, .2는 소수점 이하 자리수, f는 fixed-format
  ○ g_fmt : general format으로 입력한 숫자를 그대로 보여줌
   - 8.1g : 8는 전체 숫자를 표현할 수 있는 최대자리수, .1는 최소 소수점 이하 자리수(예를 들어
21은 21.0으로 표시), g는 general-format
• 문자 포멧은 s_fmt로 %9s는 문자를 최대 9글자까지 표현할 수 있다는 의미
• 변수의 포멧을 바꾸는 방법
  ○ format g_fmt %11.2g : g_fmt의 최대 자릿수를 11로 늘리고 최소 소수점 자릿수를 2로 늘리는 명령어
  ○ format s_fmt %-9s : s_fmt의 포맷을 왼쪽 줄 맞춤으로 바꾸고자 하는 명령어

  
5. STATA dofile


  
  
Chapter 03. 날짜 데이터 활용

책 3장 또는 아래 온라인 자료 등을 참조

https://m.blog.naver.com/gustncjstk1/222012371693


Chapter 04. 데이터파일 형식 전환

• Stata의 데이터 파일은 *.dta형식의 파일
다른 데이터파일이 dta 이외의 형식으로 되어 있다면 이를 dta 형식으로 전환해야만 Stata에서 사용할 수
있음
• 형식 전환 방법
(1) Stata의 import 기능 이용 방법 : ASCII, Excel, SAS, SPSS 형식의 파일을 STATA 데이터 파일로 변환
(2) Stat-Transfer 이용 방법 : STATA, SAS, SPSS, ODBC, Acess, Excel, Text, Gauss, MATLAB 등의 다양한
형식의 데이터 파일을 서로 다른 쪽으로 변환하는 것이 가능
○ 여기에서는 import를 이용하는 방법을 활용
○ 'export' 기능을 이용하면 *.dta파일을 txt로 내보내는 것도 가능


5. 데이터 내보내기(export)

• File > Export를 통해 적절한 파일의 종류를 선택하면 됨

• 그 밖에 SAS, SPSS 등 다른 통계프로그램의 데이터 파일을 STATA에서 불러들일 수 있음



Chapter 05.  데이터관리 기본 명령어


• 메뉴창의 Data 항목 활용

1. describe, codebook

• describle : 데이터 세트에 대한 전반적인 속성(형식상 속성)을 요약해서 보여줌
  ○ 데이터파일의 디렉터리 위치, 관측치 개수, 변수 개수 등의 기본적인 정보와 각 변수들의
저장형태, 디스플레이 포멧, 레이블 등 기술적인 정보들이 포함
  ○ 특정변수에 대해서도 describe 실행
    sysuse auto, clear
    describe price mpg
• codebook : 데이터의 내용상 속성을 보여줌
  ○ 레이블 설명 : 변수에 대한 설명
  ○ 범위, 정수로서 단위(unit)
  ○ 각 자료값의 빈도수(frequency)
  ○ 변수의 저장형태, 결측치(missing)를 보여줌
  ○ 연속형 자료의 경우 평균(mean), 표준편차(standard deviation), 백분위수(percentiles)에
대한 정보들이 제공

2. display
• 결과를 보여주는 명령어
  ○ 계산기로 유용하게 이용
• di 4*(2+3)
• di _pi
• di %12.10f _pi
• di comb(6,2)*0.5^2*0.5^4 : 동전을 6번 던져 앞면이 두번 나올 확률
• db display : 대화창 이용
• help function : 함수에 대한 설명

3. list
• 데이터세트의 모든 값을 Result창에 그대로 보여주는 명령어
   ○ 참고 : set more off. perm
• list variable-names : 지정한 변수의 모든 값을 보여줌
  ○ list price mpg  
• option  
  ○ list, sep(10) : 매 10번째 행에 구분선을 긋고자 할 때
  ○ list, mean sum N : 평균, 합계, 관측치 개수를 마지막에 보여줌
• list in
  ○ in 은 자료의 범위를 제한하는 qualifier
    list price in 1/10 // 1~10번째 관측치를 보려고 할 때 이용
    list price in -5/L // 끝에서 5번째부터 마지막 관측치까지 보려고 할 때 이용

	list
    	* 데이터를 나열하는 명령어

		
		
4. rename
• 주어진 변수이름을 변경하는 명령어
• STATA의 변수 이름 구성의 규칙
(1) 영문자, 숫자, 특수문자의 조합으로만 만들 수 있다.
(2) 최대 32글자(숫자와 특수문자 포함)만 사용
(3) 한글은 사용할 수 없음
(4) 숫자로 시작할 수 없음
(5) 일부 특수문자 -(하이픈)이나 *(asterisk)는 사용할 수 없다
(6) space를 사용할 수 없다

• 이용 사례1
 sysuse auto, clear
 rename price price1000
 rename mpg _mpg1

• 이용 사례2 : db rename
 Rename multiple variables identified by a prefix : 어떤 특정한 문자(들)로 시작하는 변수
이름을 일괄적으로 어떤 다른 문자(들)로 바꿀 수 있다.    
 
 
 
*******************************************************************
***************************************************************************
 
5. sort, gsort, bysort
• 자료를 정렬하는 명령어
• sort price : price 변수를 기준으로 오름차순 정렬
  ○ 오름차순만 가능
• gsort -price : price 변수를 기준으로 내림차순 정렬
○ + : 오름차순 정렬
○ - : 내림차순 정렬

• sort company year : company가 1순위 정렬 변수 year가 2순위 정렬 변수

• bysort : by와 sort가 결합한 것

  ○ by는 prefix의 한 종류로 기준을 의미
  ○ by company : summarize invest // 각 company에 대해 invest를 요약하라
    - 에러 발생. sort가 선행되어야 함

  ○ 대안
  ○ sort company
  ○ by company : summarize invest
  ○ 또는
  ○ by company, sort : summarize
  ○ bysort company : summarize invest

  6. drop, keep, move, order
• drop : 특정변수나 관찰치를 삭제하는 명령어
  sysuse auto, clear
  drop price mpg
  ○ drop _all : 모든 변수 삭제
  drop in 1/10
• keep : 지정한 변수나 관찰치만 남기는 명령어  
  ○ sysuse auto, clear
  keep make price
  ○ keep if foreign==1
• move : 변수간 위치를 바꿀 때 사용
  ○ sysuse auto, clear
  ○ move price rep78 : price를 rep78위치로 옮기라는 명령어    
  ○ 2개 변수만 지정가능
• order : 2개 이상의 변수위치를 한번에 바꿀 때 이용  
  ○ sysuse auto, clear
  ○ order mpg rep78 price : 지정한 순서로 배열한 후 가장 앞에 위치시키는 명령어
    
7. 데이터 레이블

• 어떤 물건에 붙여 놓은 설명 꼬리표
  ○ 데이터세트나, 변수에 설명을 붙일 수 있음
• 데이터세트 레이블
  ○ Data>Data Utilities>Label Utilities>Label dataset 선택한 후 Attach label to data에
"stata연습용파일_5월2일"을 입력
  ○ label data "Stata연습용파일_5월_2일" : 직접입력
  ○ describe으로 확인
• 변수 레이블
  ○  Data>Data Utilities>Label Utilities>Label variable 선택한 후 Attach a label to a variable
에 "자동차 가격"을 입력
  ○ label variable price "자동차 가격": 직접입력
  ○ describe으로 확인    
    
8. generate, replace
• data5_4.dta 이용
• generate : 새로운 변수를 생성
   gen gap=flife-mlife
  gen ln_pop = log(pop)
  gen var2=_n
gen var3=_n-1
 replace pop=pop*1000
• replace : 기존 변수의 값을 새로운 값으로 대체하는 명령어
  ○ 1 - 실업률 0%이상 9.0%미만인 지역
  ○ 2 - 실업률 9.0%이상 11%미만인 지역
  ○ 3 - 실업률 11.0%이상인 지역
 gen var5=1 if unemp<9.0
  replace var5=2 if unemp>=9.0 & unem<11
  replace var5=3 if unemp>=11 & unemp<.    
    
    
    
Chapter 06. 데이터관리 고급명령어

1. tabulate, xi
• 더미변수(dummy variables) : 질적 자료 중 명목형 자료를 (범주형) 변수로 표현하는 방식
  ○ 예) 인종 : 1(백인), 2(흑인), 3(기타)

• tabulate 와 xi를 이용하여 더미변수를 만들 수 있음 : nlsw88.dat 파일 이용
• tabulate : 범주형 변수의 빈도표를 만드는 명령어
• 예제
  sysuse nlsw88
  tab race : value label로 표시
  tab race, nolabel : 숫자로 표시
• 더미변수 만들기 I
  ○ 백인인 경우(1) 아닌 경우(0)
  ○ 흑인인 경우(1) 아닌 경우(0)
  ○ 기타인 경우(1) 아닌 경우(0)
  ○ tab race, gen(dum_race_)
  ○ brow로 확인
  ○ tab1 dum_race_1 dum_race_2 dum_race_3
• 더미 변수 만들기 II
   sysuse nlsw88, clear
   xi i.race, noomit prefix(dum_)
   - i.race는 race변수를 가지고 더미변수를 만들라는 의미. i는 indicator의 약자
   - noomit : 이 옵션을 추가하지 않으면 2개의 더미변수만 만들어짐
   - dum_race_1 dum_race_2 dum_race_3 가 새로 생성

2. egen
• data6_1.dta 이용
  ○ 10개 회사의 1935-1954년까지 투자실적(invest) 등을 기록한 패널 자료
• extended generate의 약자로 새로운 변수를 만드는 gen의 확장형 명령어로 새로운 변수를
만드는 명령어
  ○ gen은 어떤 변수의 수학적 변형이나 변수간 결합을 통해 새로운 변수를 생성하는 반면
  ○ egen 명령어는 좀 더 고차원적인 방법이 필요할 때 이용
  --> 구글/네이버 검색

○ 주요 egen 함수
(1) Maximum, Minimum 함수
   Maximum : 특정변수의 최대값 구하기
   Minimum : 특정변수의 최소값 구하기
   Expression 항목에 대상 변수를 입력 : 여기서는 invest
   by/if/in탭을 클릭하여 Repeat commands by groups를 선택하여 그룹별로 명
령을 실행하도록 하고 그룹을 나누는 기존으로 company변수를 선택

   - 지금까지 작업을 명령문으로 표현하면
by company, sort : egen float max_invest = max(invest)

   - 연도별 최대 투자액을 구하면
by year, sort : egen float max_invest1 = max(invest)

(2) Mean, Median 함수
  - 각 기업별로 20년 동안 투자액 평균값을 구하면
by company, sort : egen float mean_invest = mean(invest)
  - 각 연도별로 기업들의 투자액 중앙값을 구하면
by company, sort : egen float median_invest = median(invest)

(3) Percent 함수
  - 주어진 그룹에서 각 관측치가 차지하는 비중을 값으로 하는 시리즈를 만들어
주는 함수
  - 각 연도별로 전체 10개 회사의 총 투자액 중에서 각 회사의 투자액이 차지하는
비중을 볼 수 있음
  - db egen 에서 generate variable 란에 percent_invest라고 입력하고
  - Egen function에서 Percent(Proportion)을 선택하며, Expression에 invest 입력
  - by/if/in에 Repeat commands by group에서 year 선택
  - 지금까지 작업을 명령어로 보면
by year, sort : egen float percent_invest = pc(invest)


5. 데이터 구조와 관련한 명령어

• Data6_5.dat, data6_6이용 이용
• Wide type 과 Long type
  ○ Wide type data set
  ○ 1은 효과가 있음, 0은 효과가 없음
list



6. 두 파일을 결합시키는 명령어 : Append, merge






Chapter 07. 기초 통계분석


1. summarize
• 연속형 변수의 평균, 분산과 같은 요약 통계량(summary statistics)을 계산할 때 이용

• 예제 파일(data7_1.dta)을 이용하여 다음 내용을 실습
  ○ su lived : 표본평균과 표본표준편차로 계산
    - lived : 거주기간
    - STATA에서는 모든 자료를 모집단이 아닌 표본의 개념으로 봄
    su lived, detail// 백분위수(Percentiles), 중앙값, 왜도와 첨도까지 표현
    by gender, sort : su lived// 성별로 정렬한 후 성별로 요약 통계량 보기
    su lived if gender==0 : 성별이 남성(0)인 경우 요약통계량 보기
• summarize 명령어를 이용한 후 return list를 치면 주요 통계량이 scalar형태로 저장된 내용
을 볼 수 있음

  ○ 이 후 이 값을 이용한 후속 작업이 가능
  ○ su lived
  ○ return list
  ○ gen lived_s=(lived-r(mean)/r(sd) : lived 표준 값 알기
  ○ su lived_s
  ○ 주의 : return list로 저장되는 값은 항상 마지막 변수의 요약통계량
   su lived educ
   return list

2. tabstat
• 사용자가 원하는 통계량 종류를 선택하여 요약통계량을 보여줌
  ○ db tabstat 실행
  ○ Group statisitcs by variable : 각 그룹별 통계량을 원할 경우 선택

3. table

• 범주형 변수(질적 변수)와 관련한 요약통계량을 보여줌
• 예제파일(data7_1.dta)를 이용

• db table 이용
  ○ Row에 gender를 column에 kids 입력
  ○ Superrow와 Supercolumn으로 3원과 4원도 가능
  ○ statistics에 원하는 통계량을 선택
• 직접입력
  tab gender kids 
  
  : 옵션이 없으면 빈도수
  
 table gender kids, contents(mean lived median lived)
  
4. tabulate
• 범주형 변수의 빈도표를 만드는 가장 기본적인 명령어
  ○ tab gender
  ○ tab gender kids
   tab gender kids, nolabel
  ○ 최대 이원 표만 가능 : 2개의 변수만 나열 가능
• tab1은 일원빈도표 전문 명령어
  ○ 여러 개의 변수이름을
   tab1 gender kids meetings
 tab2는 이원빈도표 전문 명령어  
  ○ 여러 개의 변수이름을 적을 수 있음
  ○ 여러 개의 빈도표가 나옴
   tab2 gender kids meetings
  
• tab을 이용한 chi-square 검정
  ○ 두 범주 변수간 독립성 검정
   H0 : 변수A와변수B 는서로독립이다
   H1 : 변수A와변수B 는서로독립이아니다
   H0 : 성별과환경오염회의참석여부는서로독립이다
   H1 : 성별과환경오염회의참석여부는서로독립이아니다
   
    tab gender meetings, exp chi2
     exp는 기대도수
     chi2는 chi-square 검정

• tabi는 개별 데이터가 주어지지 않아도 chi-square 검정이 가능
   ○ tabi 42 18 \ 64 29, chi2 expected
   
5. 신뢰구간 추정   
1) ci
  ○ db ci
  ○ 평균에 대한 신뢰구간은 Normal
   - ci meetings, binomial wald
  ○ 비율에 대한 신뢰구간은 Binomial 선택
2) cii
○ 신뢰구간을 구하는 요약통계량을 알고 있을 때 이용
○ cii 153 19.268 16.954 : 관측치 개수, 표본평균, 표본표준편차 순
○ cii 153 47, wald : 관측치 개수, 성공회수 (비율)  


6. 모평균에 대한 t검정
• Statitsics > summeries, table and tests > Classical test of hypotheses 선택

7_3 데이터

(1) One-sample mean comparison test
   예제 파일 data7_3.dta 선택
   ttest inc_male == 3000

(2) Mean comparison test, paired data
  ○ 예제 파일 data7_4.dta 선택
   ttest husband == wife

(3) Two-sample mean comparison test : wide type인 경우
  ○ 예제 파일 data7_3.dta 선택
   ttest inc_female == inc_male, unpaired (동분산가정)
   ttest inc_female == inc_male, unpaired unequal (이분산가정)

(4) Two-group mean comparison test : long type인 경우
  ○ 예제 파일 data7_3.dta 선택
  ○ stack inc_female inc_male, into(income)
  ○ ttest income, by(_stack) (동분산가정)
  ○ ttest income, by(_stack) unequal (이분산가정)

(5) One-sample mean comparison calculator  
  ○ 요약통계량을 이용

  (6) Two-sample mean comparison calculator
  ○ 요약통계량을 이용
 
