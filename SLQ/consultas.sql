select (select count(distinct subject_id) from waveformfields) fields, 	-- 10134
(select count(distinct subject_id) from waveformqrst) subjects, 	-- 10134
(select count(1) from waveformqrst) qrstcomplex, 			-- 6399247
(select count(distinct  subject_id) from waveformqrst where s_i<r_i) sr,-- 0
(select count(distinct  subject_id) from waveformqrst where t_i<s_i) ts,-- 96
(select count(distinct  subject_id) from waveformqrst where q_i>t_i) qt,-- 0
(select count(1) rstqwaves from rstq),					-- 14897084
(select count(1) from subjectwords) subjectwords, 			-- 718											
(select count(1) from matrix) matrixcount,				-- 967212
(select count(distinct split_part(record, '/',3)) from rstq),		-- 753
(select count(1) from subjectrecord)					-- 742


select max(qt),max(ts),max(sr),max(ts+sr) rstqwaves from rstq
select q_amp,q_i,r_amp,r_i,s_amp,s_i,t_amp,t_i,subject_id,recorddate,qrtsorder,wave from waveformqrst order by subject_id,qrtsorder limit 10
"mimic2wdb/matched/s00135/s00135-2909-04-11-10-04"
select * from waveformqrst where subject_id=135 order by subject_id,qrtsorder  limit 10
select * from rstq where record = 'mimic2wdb/matched/s00177/s00177-3299-12-03-12-35' order by qt
"mimic2wdb/matched/s00214/s00214-3084-12-02-22-02"
"mimic2wdb/matched/s00279/s00279-3271-08-20-21-22"
--delete from rstq where record = 'mimic2wdb/matched/s00151/s00151-2509-04-16-14-43' matched/s00135/s00135-2909-04-11-10-04'
select distinct record from rstq where record like '%0279%' limit 10 

select * from matrix limit 10
select *,length(word) from subjectwords where 																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																												 order by length(word) limit 100
SELECT * FROM rstq where record like 'mimic2wdb/matched/s000%' limit 10
select min(recorddate),subject_id,database from waveformfields where database='mimic2' group by subject_id,database
select * from subjectrecord where subject_id in (select subject_id from matrix) order by subject_id
SELECT count(1),isalive FROM subjectwords where ((isalive=0 AND length(word)>3750) OR isalive=1) GROUP BY isalive ORDER BY LENGTH(word) --901
SELECT count(1) FROM subjectwords WHERE length(word)>1000 AND ((isalive=0 AND length(word)>3000) OR isalive=1) AND isalive=0 --559 506 359
select count(distinct subject_id) from matrix limit 500			--584 --713
select count(distinct subject_id) from matrix where subject_id in (select count(1) from subjectwords where isalive=1 and subject_id<20238) --306   --350 --0.60
select count(distinct subject_id) from matrix where subject_id in (select subject_id from subjectwords where isalive=0 and subject_id<20238) --194 --234 --0.40
select word from matrix where word not in (
select word from matrix where subject_id in (select subject_id from subjectwords where isalive=0)) group by word order by LENGTH(word)

select * from subjectwords where subject_id in (select subject_id from matrix where word in ('fhfbh','ebada','efa','ffhhb','geege','ccadg','hfbhf','cecba','hhfbh'))
select * from matrix where word like '%df%'


--																																																																														delete from matrix where word in (select word from matrix group by word having sum(counting)<5))
SELECT subject_id,word,isalive
    FROM subjectwords 
    WHERE length(word)>1000 
    ORDER BY isalive DESC
    LIMIT 400
select
(select round(count(1)) from subjectwords ) patients,
(select count(1) from subjectwords where isalive=0 ) alive,
(select count(1) from subjectwords where isalive=1 ) dead
select word,count(1) from matrix group by word having count(1)>=(select count(1) from subjectwords)
select * from matrix limit 10
--delete from rstq where record in('mimic2wdb/matched/s23890/s23890-2832-10-25-12-55',
--'mimic2wdb/matched/s20486/s20486-2701-07-11-18-41')
and wave is not null
select * from rstq where record = 'mimic2wdb/matched/s20486/s20486-2832-10-25-12-55'
and wave is not null
select *  from patients where subject_id=24124 limit 1
select * from rstq where record like '%24124%' limit 1
select *,length(word) from subjectwords order by length(word) limit 10
select count(1) from waveformqrst where centroid is null 
--update waveformqrst set centroid = null where centroid ='f' limit 10
select *,s_i-r_i from waveformqrst where s_i-r_i>1000 and t_i is not null limit 10
SELECT distinct q_i-t_i,t_i-s_i,s_i-r_i FROM waveformqrst 
WHERE t_i>s_i AND q_i-t_i>-130 AND q_i is not null AND r_i is not null AND s_i is not null AND t_i is not null
LIMIT 10000

select q_amp,q_i,r_amp,r_i,s_amp,s_i,t_amp,t_i,wave from waveformqrst where subject_id=7685 and q_i=912354
limit 1

SELECT q_i,r_i,s_i,t_i,qrst.subject_id,qrst.recorddate,fs,signame,signallength FROM waveformqrst qrst 
LEFT JOIN waveformfields fields
ON qrst.subject_id = fields.subject_id
AND qrst.recorddate = fields.recorddate
WHERE 
(q_i-t_i between floor(-744.43478261)-26 and ceil(-744.43478261)+26) and
(t_i-s_i between floor(687.7173913)-26 and ceil(687.7173913)+26)
and (s_i-r_i between floor(52.47826087)-26 and ceil(52.47826087)+26) 
limit 1

     
--update waveformfields set signallength = null where subject_id in (5710,5336,5933,5607,5451)
--select * from waveformQRST where subject_id in (571,3554,317,4865,4865,1075) limit 10
--delete from waveformqrst where subject_id = 7981 3768 in (5710,5336,5933,5607,5451)

select subject_id,min(t_i-s_i) from waveformqrst where t_i<s_i group by subject_id order by min(t_i-s_i)

select count(1) from r 						--14863543
SELECT count(DISTINCT r.record) FROM r 				--1181
select count(distinct hb.record) from heartbeatstemporal hb 	--1080
select count(1) cantidadDeProcesados from heartbeatstemporal 	--14862361
select count(1) rstqwaves from rstq				--14780786
select count(1) rstqwaves from rstq where qt>0 			-- 1232715< 9700= 12555757>

select count(1) as countcentroids from rstq where centroid is not null --319107

SELECT DISTINCT qt,ts,sr,centroid FROM rstq WHERE qt IS NOT NULL and qt>0 AND ts IS NOT NULL AND sr IS NOT NULL

SELECT *, pg_size_pretty(total_bytes) AS total
    , pg_size_pretty(index_bytes) AS INDEX
    , pg_size_pretty(toast_bytes) AS toast
    , pg_size_pretty(table_bytes) AS TABLE
  FROM (
  SELECT *, total_bytes-index_bytes-COALESCE(toast_bytes,0) AS table_bytes FROM (
      SELECT c.oid,nspname AS table_schema, relname AS TABLE_NAME
              , c.reltuples AS row_estimate
              , pg_total_relation_size(c.oid) AS total_bytes
              , pg_indexes_size(c.oid) AS index_bytes
              , pg_total_relation_size(reltoastrelid) AS toast_bytes
          FROM pg_class c
          LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
          WHERE relkind = 'r'
  ) a
) a order by total_bytes;

SELECT m.word,sum(m.counting),avg(s.isalive)
FROM matrix m LEFT JOIN subjectwords s ON m.subject_id=s.subject_id
WHERE m.word in (select word from wordspearson where p1>0.01)
group by m.word order by avg(s.isalive)
select count(1) from wordspearson where p1>0.1
order by p1 desc
--16768

select * from rstq where centroid is not null limit 10
select sum(counting) sumcounting from matrix m 
select subject_id,sum(counting) from matrix m group by subject_id order by sum(counting)
select word,sum(counting) from matrix m group by word order by sum(counting)

select * from matrix m LEFT JOIN subjectwords s ON m.subject_id=s.subject_id
where m.word = 'fbabd' and subject_id=19372

delete from matrix where word in (select word FROM wordspearson where p1<=0.02) limit 10
SELECT word,p1 as p1iisabigvaluesoletsseeitallplease,p2 as p2iisabigvaluesoletsseeitallplease FROM wordspearson
where  p1>0.02 order by p1 --21724

SELECT count(1),LENGTH(word) FROM subjectwords GROUP BY LENGTH(word) ORDER BY LENGTH(word)
SELECT subject_id,word,isalive 
    FROM subjectwords 
    WHERE ((isalive=0 AND length(word)>15000) OR (isalive=1 AND length(word)>3600))

delete from word where wave='{}'