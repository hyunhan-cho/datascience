*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*
* Chapter 01. STATA 시작하기
*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*

* Stata 내장 데이터 "auto.dta" 불러오기
sysuse auto, clear


* 데이터 스프레드시트 보기 (새 창)
browse

* 데이터 스프레드 시트 편집하기(새 창에서)
edit

* price변수의 요약 통계량 보기
summarize price
sum price

*웹 url에서  데이터 불러오기
use http://www.stata-press.com/data/r9/auto.dta, clear

*webuse 명령어로 데이터 불러오기
webuse auto, clear

*데이터를 직접 입력하기
clear
input aa bb cc
1 2 3
4 5 6
7 8 9
end
list

* 메모리에 로딩된 데이터 지우기
clear

* Stata 시스템 관련 디렉터리 확인
sysdir

*명렁어랑 대화창(dialog box)
sysuse auto, clear


*작업환경 설정 상태 확인
set

*메모리 설정 확인
query memory
* set memory 300m, perm

*결과창(output) 설정 확인 및 변경
query output
set more off, perm //결과가 길엉도 계속 표시되도록 영구 설정



*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*
* Chapter 02. 로그파일과 데이터파일
*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*

* 로그 시작 (현재 디렉토리에 파일 생성, 기존 파일이 있으면 덮어씀)
log using "my_log.smcl", replace

* 명령 실행
describe
summarize //stata에서도 로그 찍는게 있다니 완전 신기.

* 로그 종료
log close


*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*
* Chapter 05. 데이터관리 기본 명령어
*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*
sysuse auto, clear

// 1. describe,codebook
describe

describe price mpg
codebook

//2. display (계산기처럼 사용)
display 4 * (2 + 3)
display pi
display %12.10f - pi
display comb(6, 2)

*stata함수 도움말
help function

// 3. 데이터 나열
list
list price mpg
list, sep(10)
list, mean sum N
list price in 1/10 //1 ~10번재 관측치만
list price in -5/L

//4. rename(뱐수 이름 변경)
rename price price1000
rename mpg _mpg1

list price1000 _mpg1 in 1/5

*6. drop, keep, move, order(변수/관측치 관리)
drop headroom, trunk //변수 삭제
drop in 1/10
sysuse auto, clear
keep make price mpg
keep if foreign == 1
describe

* 7. 데이터 레이블
label data "1978 Automobile Data"
label variable price "Price in USD"
describe

sysuse auto, clear
* 8. generate, replace (변수 생성 및 변경)

gen weight_kg = weight * 0.453592 // 파운드를 kg으로 변환
gen price_category = 1 if price < 5000
replace price_category = 2 if price >= 5000 & price < 10000
replace price_category = 3 if price >= 10000 & price < .
tab price_category

*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*
* Chapter 06. 데이터관리 고급명령어
*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*
sysuse nlsw88, clear

*1. tabulate로 더미변수 만들기
tabulate race, gen(dum_race_)
list race dum_race_* in 1/10

* 2. egen (확장된 generate)
* 예제 데이터(grunfeld) 불러오기
webuse grunfeld, clear

* (1) Maximum, Minimum 함수
bysort company: egen float max_invest = max(invest)

* (2) Mean, Median 함수
bysort company: egen float mean_invest = mean(invest)

* (3) Percent 함수
by year, sort: egen float percdent_invest = pc(invest)
list company year invest max_invest mean_invest percdent_invest if company<=2

*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*
* Chapter 07. 기초 통계분석
*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*

sysuse nlsw88, clear
* 1. summarize
summarize wage // 기본 요약통계
summarize wage, detail // 상세 요약통계
bysort race: su wage // 그룹별 요약통계
su wage if married==0 // 조건별 요약통계

* return list 활용
su wage
return list
gen wage_z = (wage - r(mean)) / r(sd) // 표준화 변수 생성
su wage_z



* 2. tabstat (원하는 통계량 선택)
tabstat wage, stats(mean sd p50 min max)
tabstat wage, by(race) stats(mean sd)

* 3. table (그룹별 통계표)
table gender kids, contents(mean lived)


* 4. tabulate (빈도표)
tabulate race // 일원 빈도표
tabulate race married // 이원 빈도표
tab1 race married south // 여러 변수 일원 빈도표
tab2 race married south // 여러 변수 조합 이원 빈도표


* 카이제곱(chi-square) 검정
tabulate race south, exp chi2

* tabi (요약된 데이터로 검정)
tabi 42 18 \ 64 29, chi2 expected

* 5. 신뢰구간 추정
* ci (평균 신뢰구간)
ci means wage, level(95)

ci proportions south, wald



* cii (요약된 데이터로 신뢰구간 추정)
cii means 153 19.268 16.954
cii proportions 153 47, wald


* 6. 모평균에 대한 t-검정 (ttest)
* (1) One-sample t-test (단일표본)
ttest wage == 7.5

* (2) Paired t-test (대응표본) - 이 데이터셋에는 적합한 변수가 없음
* ttest before == after

ttest wage , by(married)
ttest wage, by(married) unequal // 이분산 가정


