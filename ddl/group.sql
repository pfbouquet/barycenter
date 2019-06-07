CREATE TABLE public.group (

  insert_datetime TIMESTAMP DEFAULT now(),
  id VARCHAR(100) NOT NULL CONSTRAINT group_pkey PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  creator VARCHAR(50) NOT NULL

);
