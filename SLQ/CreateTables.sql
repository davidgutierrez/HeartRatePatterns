CREATE TABLE waveformqrst (
  id serial NOT NULL,
  q_amp real,
  q_i integer,
  r_amp real,
  r_i integer,
  s_amp real,
  s_i integer,
  t_amp real,
  t_i integer,
  subject_id integer,
  recorddate character varying(255),
  qrtsorder integer,
  wave real[], -- Original Wave
  centroid character varying(50),
  CONSTRAINT waveformqrst_pkey PRIMARY KEY (id),
  CONSTRAINT "uniqueQRST" UNIQUE (subject_id, recorddate, qrtsorder)
);

CREATE TABLE subjectword
(
  id serial NOT NULL,
  subject_id integer,
  word character varying(40000),
  isalive integer,
  CONSTRAINT subjectwords_pkey PRIMARY KEY (id)
);
