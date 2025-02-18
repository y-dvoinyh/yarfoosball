# yarfoosball
Вэб приложение для расчетарейтинга игроков в настольный футбол


https://live.kickertool.de/api/table_soccer/tournaments/qOa7qMNsnG68KU-H62LPz.json


-- Мухина Дарья 686 -> 102 
-- Артем Вуколов 500 -> 51
-- Карина Печикян 335 -> 21 
-- Лейсян Шакирова 820 -> 184
-- Даниил Тараканов 392 -> 60
-- Артем Андреевских 486 -> 157
-- Артем Андреевских 295 -> 157
-- Артем Андреевских 179 -> 157
-- Дарья Пестова 595 -> 107
-- Дарья Пестова 775 -> 107
-- Денис Киселев 501 -> 482
-- Елизавета Киселева 502 -> 480
-- Марина Баруздина 665 -> 367
-- Софья Поскребышева 603 -> 143
-- Симонова Полина 599 -> 386
-- Савелий Ануфриев 186 -> 15
-- Роман Нефилим 200 -> 168



/*
UPDATE rating_history
SET player_id = 157 
WHERE player_id = 179
*/
/*
UPDATE teams
SET first_player_id = 157
WHERE first_player_id = 179
*/
/*
UPDATE teams
SET second_player_id = 157
WHERE second_player_id = 179
*/

--DELETE FROM ratings WHERE player_id = 179
--DELETE FROM players WHERE id = 179


-- Дарья Иванова 856 
-- Дарья Пестова 107
-- competitions 
--	176  Пипи 21.06.2024
-- Мышь 07.03.2024
-- Мышь 29.12.2023
-- Мышь 22.12.23
-- БХ 2.12.2023
-- БХ 25.11.2023
-- БХ 7.10.2023
-- Пипи 06.10
-- БХ 09.09.23
-- БХ 26.08.2023
-- БХ 19.08.2023
-- БХ 22.07.2023
-- БХ 8.07.2023
-- Pipistrello 30.06.2023
-- БХ 03.06.2023
-- БХ 20.05.2023

/*
Обе участвовали в 
	COMPETITON
	Pipistrello 30.06.2023 - 316 - rating_history = 4213
	Мышь 29.12.2023 - 248 - rating_history = 13672
	
	MATCH
	Pipistrello 30.06.2023 rating_history
	4107
	4124
	4141
	4147
	4166
	4188
	4197
	Мышь 29.12.2023
	13492
	13515
	13547
	13605
	
*/
/*
SELECT 
	competitions.id,
	competitions.name,
	rating_history.*
FROM competitions 
	LEFT JOIN rating_history
		ON rating_history.competition_id = competitions.id
			AND level = 'COMPETITION'
			AND player_id = 107
WHERE competitions.id = 248

/*
name in (
	'Пипи 21.06.2024', 
	'Мышь 07.03.2024', 
	'Мышь 22.12.23', 
	'БХ 2.12.2023', 
	'БХ 25.11.2023', 
	'БХ 7.10.2023',
	'Пипи 06.10', 
	'БХ 09.09.23', 
	'БХ 26.08.2023', 
	'БХ 19.08.2023', 
	'БХ 22.07.2023',
	'БХ 8.07.2023', 
	'БХ 03.06.2023', 
	'БХ 20.05.2023'
)*/
*/

/*

COMPETITON
	Pipistrello 30.06.2023 - 316 - rating_history = 4213
	Мышь 29.12.2023 - 248 - rating_history = 13672

--UPDATE rating_history SET player_id = 856 WHERE id IN (4213,13672)

*/

/*
SELECT 
	competitions.id,
	competitions.name,
	rating_history.id,
	t1p1.first_name || ' ' || t1p1.last_name AS "t1p1",
	t1p2.first_name || ' ' || t1p2.last_name AS "t1p2",
	t2p1.first_name || ' ' || t2p1.last_name AS "t2p1",
	t2p2.first_name || ' ' || t2p2.last_name AS "t2p2"
FROM competitions 
	LEFT JOIN rating_history
		ON rating_history.competition_id = competitions.id
			AND level = 'MATCH'
			AND player_id = 107
	LEFT JOIN matches ON matches.id = rating_history.match_id
	LEFT JOIN teams t1 ON t1.id = matches.first_team_id
	LEFT JOIN teams t2 ON t2.id = matches.second_team_id
	LEFT JOIN players t1p1 ON t1p1.id = t1.first_player_id
	LEFT JOIN players t1p2 ON t1p2.id = t1.second_player_id
	LEFT JOIN players t2p1 ON t2p1.id = t2.first_player_id
	LEFT JOIN players t2p2 ON t2p2.id = t2.second_player_id
WHERE competitions.id = 248
ORDER BY match_id
*/
/*
MATCH
	Pipistrello 30.06.2023 rating_history
	4107
	4124
	4141
	4147
	4166
	4188
	4197
*/
/*
UPDATE rating_history
SET player_id = 856
WHERE id = ANY(
SELECT 
	rating_history.id
FROM competitions 
	LEFT JOIN rating_history
		ON rating_history.competition_id = competitions.id
WHERE competitions.name IN (
	'Пипи 21.06.2024', 
	'Мышь 07.03.2024', 
	'Мышь 22.12.23', 
	'БХ 2.12.2023', 
	'БХ 25.11.2023', 
	'БХ 7.10.2023',
	'Пипи 06.10', 
	'БХ 09.09.23', 
	'БХ 26.08.2023', 
	'БХ 19.08.2023', 
	'БХ 22.07.2023',
	'БХ 8.07.2023', 
	'БХ 03.06.2023', 
	'БХ 20.05.2023'
)
	AND rating_history.player_id = 107
)

*/