
--SO
use 05-Sep-2018-SO;

SELECT Id,Tags FROM posts WHERE PostTypeId = 1 INTO OUTFILE '/var/lib/mysql-files/id-tags-all.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

SELECT Id,Title,Body,Tags FROM posts WHERE PostTypeId = 1 INTO OUTFILE '/var/lib/mysql-files/SO-all-with-Raretag.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';