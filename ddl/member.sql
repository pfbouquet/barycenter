CREATE TABLE coding_night.member (

  insert_datetime TIMESTAMP DEFAULT now(),
  id SERIAL NOT NULL CONSTRAINT member_pkey PRIMARY KEY,
  user_id INTEGER NOT NULL,
  group_id VARCHAR(50) NOT NULL

);
