SELECT 
	r.age
,	ra.name         AS race
,	sx.name         AS sex
,	oc.name         AS occupation
,	r.hours_week    AS hours_per_week
, 	wc.name         AS work_class
, 	el.name         AS education_level
,	r.education_num
,	r.capital_gain  AS income
,	r.capital_loss  AS loss
,	r.over_50k
,	ms.name	        AS marital_status
,	rel.name        AS relationship_name
,	co.name         AS country
FROM records AS r
	LEFT JOIN workclasses AS wc
		ON r.workclass_id       = wc.id
	LEFT JOIN education_levels AS el
		ON r.education_level_id = el.id
	LEFT JOIN marital_statuses AS ms
		ON r.marital_status_id  = ms.id
	LEFT JOIN occupations AS oc
		ON r.occupation_id      = oc.id
	LEFT JOIN relationships AS rel
		ON r.relationship_id    = rel.id
	LEFT JOIN races AS ra
		ON r.race_id            = ra.id
	LEFT JOIN sexes AS sx
		ON r.sex_id             = sx.id
	LEFT JOIN countries AS co
		ON r.country_id         = co.id