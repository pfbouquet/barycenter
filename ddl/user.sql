CREATE TABLE public.user (

  insert_datetime TIMESTAMP DEFAULT now(),
  id SERIAL NOT NULL CONSTRAINT users_pkey PRIMARY KEY,
  username VARCHAR(30) NOT NULL,
  password_hash VARCHAR(100) NOT NULL,
  email TEXT NOT NULL,
  address_1 VARCHAR(100) NOT NULL,
  address_2 VARCHAR(100) NOT NULL

);
