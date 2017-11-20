CREATE TABLE IF NOT EXISTS q
(
  id serial NOT NULL,
  record character varying(50),
  sample integer,
  amp double precision,
  CONSTRAINT q_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
  
CREATE TABLE IF NOT EXISTS s
(
  id serial NOT NULL,
  record character varying(50),
  sample integer,
  amp double precision,
  CONSTRAINT s_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX sx_record
  ON s
  USING btree
  (record COLLATE pg_catalog."default", sample);

-- R Table
CREATE TABLE IF NOT EXISTS r
(
  id serial NOT NULL,
  record character varying(50),
  sample integer,
  amp double precision,
  CONSTRAINT r_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX rx_record
  ON r
  USING btree
  (record COLLATE pg_catalog."default", sample);


-- T Table
CREATE TABLE IF NOT EXISTS t
(
  id serial NOT NULL,
  record character varying(50),
  sample integer,
  amp double precision,
  CONSTRAINT t_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

CREATE INDEX tx_record
  ON t
  USING btree
  (record COLLATE pg_catalog."default", sample);

--COPY Q(record,sample,amp) FROM '/home/scidb/HeartRatePatterns/Alejandro/Q_2.txt' 
--COPY S(record,sample,amp) FROM '/home/scidb/HeartRatePatterns/Alejandro/S_2.txt' 
--COPY R(record,sample,amp) FROM '/home/scidb/HeartRatePatterns/Alejandro/R_2.txt' 
--COPY T(record,sample,amp) FROM '/home/scidb/HeartRatePatterns/Alejandro/T_2.txt' 
--COPY A FROM '/home/scidb/HeartRatePatterns/Alejandro/A_2.txt' 
--1	mimic2wdb/matched/s03992/s03992-2531-09-18-14-26	518436		2518436	2528436		[14:26:54.489 18/09/2531]	5:37:07.488
  id	record							rec_from	rec_to	rec_total	start_time			total_time