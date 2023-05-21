SELECT id, username, password, email
	FROM public.artemis_user;


TRUNCATE TABLE public.artemis_output;
TRUNCATE TABLE public.artemis_input;
TRUNCATE TABLE public.artemis_user;

SELECT * FROM public.artemis_input;
SELECT * FROM public.artemis_output;

UPDATE public.artemis_output SET input_id = 2 WHERE id > 15
UPDATE public.artemis_input SET user_id = 1

DELETE FROM public.artemis_input WHERE id = 4

SELECT * FROM public.artemis_user;
SELECT * FROM public.auth_user;