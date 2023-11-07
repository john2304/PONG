DROP TABLE if EXIST albums;

CREATE TABLE user_info (
	id VARCHAR(11) NOT NULL,
	title VARCHAR(150),
	wins VARCHAR(100),
	loss VARCHAR(100),
	PRIMARY KEY (id),
	UNIQUE (id),
))