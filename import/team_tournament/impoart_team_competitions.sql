SELECT
	uuid,
	first_name,
	last_name
FROM player
-------------------------------------------------------------------------------------------

SELECT
	team.uuid team_uuid,
	team.name team_name,
	array_agg(player.uuid) players
FROM team
	LEFT JOIN player_team ON player_team.team_id = team.id
	LEFT JOIN player ON player.id = player_team.player_id
GROUP BY team.uuid, team.name

-------------------------------------------------------------------------------------------
SELECT
	competition.uuid competition_uuid,
	competition.date competition_date,
	competition.description competition_description,
	competition.name competition_name,
	team1.name team1_name,
	team1.uuid team1_uuid,
	team2.name team2_name,
	team2.uuid team2_uuid,
	match.uuid match_uuid,
	match_team1.uuid match_team1_uuid,
	players1.p match_team1_players,
	match_team2.uuid match_team2_uuid,
	players2.p match_team1_players,
	set_model.uuid set_uuid,
	set_model.first_team_scope,
	set_model.second_team_scope
FROM competition
	LEFT JOIN team team1
		ON team1.id = competition.first_team_id
	LEFT JOIN team team2
		ON team2.id = competition.second_team_id
	LEFT JOIN match
		ON match.competition_id = competition.id
	LEFT JOIN match_team match_team1
		ON match_team1.id = match.first_team_id
	LEFT JOIN match_team match_team2
		ON match_team2.id = match.second_team_id
	LEFT JOIN LATERAL (
		SELECT array_agg(player.uuid) p
		FROM player
		WHERE player.id IN (match_team1.first_player_id, match_team1.second_player_id)
	) players1 ON TRUE
	LEFT JOIN LATERAL (
		SELECT array_agg(player.uuid) p
		FROM player
		WHERE player.id IN (match_team2.first_player_id, match_team2.second_player_id)
	) players2 ON TRUE
	LEFT JOIN set_model
		ON set_model.match_id = match.id
ORDER BY match.id, set_model.id