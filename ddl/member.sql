CREATE TABLE coding_night.member (

  insert_datetime TIMESTAMP DEFAULT now(),
  id SERIAL NOT NULL CONSTRAINT member_pkey PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  group_id VARCHAR(50) NOT NULL,
  address_1 VARCHAR(100) NOT NULL,
  address_2 VARCHAR(100) NOT NULL

);
