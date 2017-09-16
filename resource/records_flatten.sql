SELECT 
	r.age
,	ra.name AS race
,	sx.name as sex
,	oc.name AS occupation
,	r.hours_week as hours_per_week
, 	wc.name AS work_class
, 	el.name AS education_level
,	r.education_num
,	r.capital_gain
,	r.capital_loss
,	r.over_50k
,	ms.name	AS marital_status
,	rel.name AS relationship_name
,	co.name as country
FROM records AS r
	LEFT JOIN workclasses AS wc
		ON r.workclass_id = wc.id
	LEFT JOIN education_levels as el
		ON r.education_level_id = el.id
	LEFT JOIN marital_statuses AS ms
		ON r.marital_status_id = ms.id
	LEFT JOIN occupations as oc
		ON r.occupation_id = oc.id
	LEFT JOIN relationships as rel
		ON r.relationship_id = rel.id
	LEFT JOIN races AS ra
		ON r.race_id = ra.id
	LEFT JOIN sexes AS sx
		ON r.sex_id = sx.id
	LEFT JOIN countries as co
		ON r.country_id = co.id