-- Active: 1757665983045@@127.0.0.1@3306@preprocessing
use preprocessing;

select * from raw_data;
select * from match_info;


#1. raw_data(
--game_id bigint 
-- action_id bigint 
-- period_id bigint 
-- time_seconds double 
-- team_id bigint 
-- player_id double 
-- result_name text 
-- start_x double 
-- start_y double 
-- end_x double 
-- end_y double 
-- dx double 
-- dy double 
-- type_name text 
-- player_name_ko text 
-- team_name_ko text 
-- position_name text 
-- main_position text)

#2. match_info(
-- game_id bigint 
-- season_id bigint 
-- competition_id bigint 
-- game_day bigint 
-- game_date text 
-- home_team_id bigint 
-- away_team_id bigint 
-- home_score bigint 
-- away_score bigint 
-- venue text 
-- competition_name text 
-- country_name text 
-- season_name bigint 
-- home_team_name text 
-- home_team_name_ko text 
-- away_team_name text 
-- away_team_name_ko text


#
-- 특정 선수의 특정 이벤트에 따른 승률

--구하고 싶은 값: 승률

--남길 컬럼 : 선수이름, 이벤트, 승률
--필요한 테이블 : raw_data, match_info

SELECT rd.player_name_ko,
       rd.type_name,
       SUM(CASE 
               WHEN (mi.home_team_id = rd.team_id AND mi.home_score > mi.away_score) 
                    OR (mi.away_team_id = rd.team_id AND mi.away_score > mi.home_score) 
               THEN 1 
               ELSE 0 
           END) AS wins,
       COUNT(*) AS total_events,
       ROUND(SUM(CASE 
                     WHEN (mi.home_team_id = rd.team_id AND mi.home_score > mi.away_score) 
                          OR (mi.away_team_id = rd.team_id AND mi.away_score > mi.home_score) 
                     THEN 1 
                     ELSE 0 
                 END) / COUNT(*) * 100, 2) AS win_rate
FROM raw_data rd
JOIN match_info mi ON rd.game_id = mi.game_id
GROUP BY rd.player_name_ko, rd.type_name;

#다중 회귀 모델 (Multiple Regression Model)
# X -> y를 예측

# X = [type_name, wins, total_events]
# y = win_rate
