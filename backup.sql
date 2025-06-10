--
-- PostgreSQL database cluster dump
--

-- Started on 2025-06-10 11:35:19

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:n7rV2200vxkzCbC08VxsiQ==$1rY/LSfs//nCWSxvGHC6Mpop6vKwZTr1dxBSnezBMfM=:pXQo2DsXNuPRcrk51JV5Ra+FddO5VIBbo9geNR2eEU0=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-06-10 11:35:19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-06-10 11:35:20

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-06-10 11:35:20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 234 (class 1259 OID 16713)
-- Name: acciones_recientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acciones_recientes (
    id integer NOT NULL,
    descripcion text NOT NULL,
    tipo character varying(20),
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.acciones_recientes OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16712)
-- Name: acciones_recientes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.acciones_recientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.acciones_recientes_id_seq OWNER TO postgres;

--
-- TOC entry 5010 (class 0 OID 0)
-- Dependencies: 233
-- Name: acciones_recientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.acciones_recientes_id_seq OWNED BY public.acciones_recientes.id;


--
-- TOC entry 226 (class 1259 OID 16592)
-- Name: anio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anio (
    id integer NOT NULL,
    nombre character varying(20) NOT NULL
);


ALTER TABLE public.anio OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16514)
-- Name: asistencias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asistencias (
    id integer NOT NULL,
    fecha date NOT NULL,
    presente boolean NOT NULL,
    usuario_id integer,
    materia_id integer
);


ALTER TABLE public.asistencias OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16513)
-- Name: asistencias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asistencias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asistencias_id_seq OWNER TO postgres;

--
-- TOC entry 5011 (class 0 OID 0)
-- Dependencies: 221
-- Name: asistencias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asistencias_id_seq OWNED BY public.asistencias.id;


--
-- TOC entry 225 (class 1259 OID 16591)
-- Name: año_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."año_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."año_id_seq" OWNER TO postgres;

--
-- TOC entry 5012 (class 0 OID 0)
-- Dependencies: 225
-- Name: año_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."año_id_seq" OWNED BY public.anio.id;


--
-- TOC entry 236 (class 1259 OID 16723)
-- Name: comunicados; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comunicados (
    id integer NOT NULL,
    emisor_id integer NOT NULL,
    receptor_id integer NOT NULL,
    mensaje text NOT NULL,
    fecha_envio timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    leido boolean DEFAULT false,
    respuesta text,
    fecha_respuesta timestamp without time zone
);


ALTER TABLE public.comunicados OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16722)
-- Name: comunicados_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comunicados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comunicados_id_seq OWNER TO postgres;

--
-- TOC entry 5013 (class 0 OID 0)
-- Dependencies: 235
-- Name: comunicados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comunicados_id_seq OWNED BY public.comunicados.id;


--
-- TOC entry 228 (class 1259 OID 16657)
-- Name: cursos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cursos (
    id integer NOT NULL,
    nombre character varying(20) NOT NULL,
    anio_id integer NOT NULL
);


ALTER TABLE public.cursos OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16656)
-- Name: cursos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cursos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cursos_id_seq OWNER TO postgres;

--
-- TOC entry 5014 (class 0 OID 0)
-- Dependencies: 227
-- Name: cursos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cursos_id_seq OWNED BY public.cursos.id;


--
-- TOC entry 232 (class 1259 OID 16696)
-- Name: examenes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.examenes (
    id integer NOT NULL,
    curso_id integer,
    materia_id integer,
    fecha date NOT NULL,
    hora time without time zone NOT NULL,
    titulo character varying(100),
    creado_por_dni character varying(15)
);


ALTER TABLE public.examenes OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16695)
-- Name: examenes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.examenes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.examenes_id_seq OWNER TO postgres;

--
-- TOC entry 5015 (class 0 OID 0)
-- Dependencies: 231
-- Name: examenes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.examenes_id_seq OWNED BY public.examenes.id;


--
-- TOC entry 230 (class 1259 OID 16669)
-- Name: horarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horarios (
    id integer NOT NULL,
    curso_id integer NOT NULL,
    materia_id integer NOT NULL,
    dia character varying(15) NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fin time without time zone NOT NULL
);


ALTER TABLE public.horarios OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16668)
-- Name: horarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.horarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horarios_id_seq OWNER TO postgres;

--
-- TOC entry 5016 (class 0 OID 0)
-- Dependencies: 229
-- Name: horarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.horarios_id_seq OWNED BY public.horarios.id;


--
-- TOC entry 224 (class 1259 OID 16536)
-- Name: materias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materias (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    profesor_id integer,
    curso_id integer
);


ALTER TABLE public.materias OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16535)
-- Name: materias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.materias_id_seq OWNER TO postgres;

--
-- TOC entry 5017 (class 0 OID 0)
-- Dependencies: 223
-- Name: materias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.materias_id_seq OWNED BY public.materias.id;


--
-- TOC entry 220 (class 1259 OID 16502)
-- Name: notas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notas (
    id integer NOT NULL,
    nota numeric(4,2) NOT NULL,
    usuario_id integer,
    materia_id integer
);


ALTER TABLE public.notas OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16501)
-- Name: notas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notas_id_seq OWNER TO postgres;

--
-- TOC entry 5018 (class 0 OID 0)
-- Dependencies: 219
-- Name: notas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notas_id_seq OWNED BY public.notas.id;


--
-- TOC entry 218 (class 1259 OID 16467)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    apellido character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    dni character varying(15) NOT NULL,
    rol character varying(20) NOT NULL,
    "contraseña" text,
    curso_id integer,
    CONSTRAINT usuarios_rol_check CHECK (((rol)::text = ANY ((ARRAY['alumno'::character varying, 'profesor'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16466)
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- TOC entry 5019 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- TOC entry 4795 (class 2604 OID 16716)
-- Name: acciones_recientes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acciones_recientes ALTER COLUMN id SET DEFAULT nextval('public.acciones_recientes_id_seq'::regclass);


--
-- TOC entry 4791 (class 2604 OID 16595)
-- Name: anio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anio ALTER COLUMN id SET DEFAULT nextval('public."año_id_seq"'::regclass);


--
-- TOC entry 4789 (class 2604 OID 16517)
-- Name: asistencias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencias ALTER COLUMN id SET DEFAULT nextval('public.asistencias_id_seq'::regclass);


--
-- TOC entry 4797 (class 2604 OID 16726)
-- Name: comunicados id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comunicados ALTER COLUMN id SET DEFAULT nextval('public.comunicados_id_seq'::regclass);


--
-- TOC entry 4792 (class 2604 OID 16660)
-- Name: cursos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cursos ALTER COLUMN id SET DEFAULT nextval('public.cursos_id_seq'::regclass);


--
-- TOC entry 4794 (class 2604 OID 16699)
-- Name: examenes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examenes ALTER COLUMN id SET DEFAULT nextval('public.examenes_id_seq'::regclass);


--
-- TOC entry 4793 (class 2604 OID 16672)
-- Name: horarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios ALTER COLUMN id SET DEFAULT nextval('public.horarios_id_seq'::regclass);


--
-- TOC entry 4790 (class 2604 OID 16539)
-- Name: materias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias ALTER COLUMN id SET DEFAULT nextval('public.materias_id_seq'::regclass);


--
-- TOC entry 4788 (class 2604 OID 16505)
-- Name: notas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notas ALTER COLUMN id SET DEFAULT nextval('public.notas_id_seq'::regclass);


--
-- TOC entry 4787 (class 2604 OID 16470)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- TOC entry 5002 (class 0 OID 16713)
-- Dependencies: 234
-- Data for Name: acciones_recientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.acciones_recientes (id, descripcion, tipo, fecha) FROM stdin;
\.


--
-- TOC entry 4994 (class 0 OID 16592)
-- Dependencies: 226
-- Data for Name: anio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anio (id, nombre) FROM stdin;
1	1º Año
2	2º Año
3	3º Año
4	4º Año
5	5º Año
6	6º Año
\.


--
-- TOC entry 4990 (class 0 OID 16514)
-- Dependencies: 222
-- Data for Name: asistencias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.asistencias (id, fecha, presente, usuario_id, materia_id) FROM stdin;
1	2025-04-27	t	1	1
2	2025-04-27	t	1	1
3	2025-04-28	t	1	1
4	2025-04-28	t	1	1
\.


--
-- TOC entry 5004 (class 0 OID 16723)
-- Dependencies: 236
-- Data for Name: comunicados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comunicados (id, emisor_id, receptor_id, mensaje, fecha_envio, leido, respuesta, fecha_respuesta) FROM stdin;
1	8	1	anuncio el 10/06/25	2025-06-10 10:15:19.788957	f	\N	\N
2	8	7	anuncio el 10/06/25	2025-06-10 10:15:19.865271	f	\N	\N
\.


--
-- TOC entry 4996 (class 0 OID 16657)
-- Dependencies: 228
-- Data for Name: cursos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cursos (id, nombre, anio_id) FROM stdin;
1	1°A	1
2	1°B	1
3	2°A	2
4	2°B	2
5	3°A	3
6	3°B	3
7	4°A	4
8	4°B	4
9	5°A	5
10	5°B	5
11	6°A	6
12	6°B	6
\.


--
-- TOC entry 5000 (class 0 OID 16696)
-- Dependencies: 232
-- Data for Name: examenes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.examenes (id, curso_id, materia_id, fecha, hora, titulo, creado_por_dni) FROM stdin;
2	2	1	2025-05-22	11:45:00		00112233
3	1	100	2025-05-27	08:30:00		88776655
\.


--
-- TOC entry 4998 (class 0 OID 16669)
-- Dependencies: 230
-- Data for Name: horarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.horarios (id, curso_id, materia_id, dia, hora_inicio, hora_fin) FROM stdin;
1	1	1	Lunes	08:00:00	09:30:00
2	2	1	Martes	10:00:00	11:30:00
3	1	100	Lunes	07:00:00	07:45:00
4	1	101	Lunes	07:45:00	08:30:00
5	1	102	Lunes	08:30:00	09:15:00
6	1	103	Lunes	09:15:00	10:00:00
7	1	104	Lunes	10:15:00	11:00:00
8	1	105	Lunes	11:00:00	11:45:00
9	1	106	Lunes	11:45:00	12:30:00
10	1	107	Lunes	12:30:00	13:15:00
11	1	108	Martes	07:00:00	07:45:00
12	1	109	Martes	07:45:00	08:30:00
13	1	100	Martes	08:30:00	09:15:00
14	1	101	Martes	09:15:00	10:00:00
15	1	102	Martes	10:15:00	11:00:00
16	1	103	Martes	11:00:00	11:45:00
17	1	104	Martes	11:45:00	12:30:00
18	1	105	Martes	12:30:00	13:15:00
19	1	106	Miércoles	07:00:00	07:45:00
20	1	107	Miércoles	07:45:00	08:30:00
21	1	108	Miércoles	08:30:00	09:15:00
22	1	109	Miércoles	09:15:00	10:00:00
23	1	100	Miércoles	10:15:00	11:00:00
24	1	101	Miércoles	11:00:00	11:45:00
25	1	102	Miércoles	11:45:00	12:30:00
26	1	103	Miércoles	12:30:00	13:15:00
27	1	104	Jueves	07:00:00	07:45:00
28	1	105	Jueves	07:45:00	08:30:00
29	1	106	Jueves	08:30:00	09:15:00
30	1	107	Jueves	09:15:00	10:00:00
31	1	108	Jueves	10:15:00	11:00:00
32	1	109	Jueves	11:00:00	11:45:00
33	1	100	Jueves	11:45:00	12:30:00
34	1	101	Jueves	12:30:00	13:15:00
35	1	102	Viernes	07:00:00	07:45:00
36	1	103	Viernes	07:45:00	08:30:00
37	1	104	Viernes	08:30:00	09:15:00
38	1	105	Viernes	09:15:00	10:00:00
39	1	106	Viernes	10:15:00	11:00:00
40	1	107	Viernes	11:00:00	11:45:00
41	1	108	Viernes	11:45:00	12:30:00
42	1	109	Viernes	12:30:00	13:15:00
43	2	200	Lunes	07:00:00	07:45:00
44	2	201	Lunes	07:45:00	08:30:00
45	2	202	Lunes	08:30:00	09:15:00
46	2	203	Lunes	09:15:00	10:00:00
47	2	204	Lunes	10:15:00	11:00:00
48	2	205	Lunes	11:00:00	11:45:00
49	2	206	Lunes	11:45:00	12:30:00
50	2	207	Lunes	12:30:00	13:15:00
51	2	208	Martes	07:00:00	07:45:00
52	2	209	Martes	07:45:00	08:30:00
53	2	200	Martes	08:30:00	09:15:00
54	2	201	Martes	09:15:00	10:00:00
55	2	202	Martes	10:15:00	11:00:00
56	2	203	Martes	11:00:00	11:45:00
57	2	204	Martes	11:45:00	12:30:00
58	2	205	Martes	12:30:00	13:15:00
59	2	206	Miércoles	07:00:00	07:45:00
60	2	207	Miércoles	07:45:00	08:30:00
61	2	208	Miércoles	08:30:00	09:15:00
62	2	209	Miércoles	09:15:00	10:00:00
63	2	200	Miércoles	10:15:00	11:00:00
64	2	201	Miércoles	11:00:00	11:45:00
65	2	202	Miércoles	11:45:00	12:30:00
66	2	203	Miércoles	12:30:00	13:15:00
67	2	204	Jueves	07:00:00	07:45:00
68	2	205	Jueves	07:45:00	08:30:00
69	2	206	Jueves	08:30:00	09:15:00
70	2	207	Jueves	09:15:00	10:00:00
71	2	208	Jueves	10:15:00	11:00:00
72	2	209	Jueves	11:00:00	11:45:00
73	2	200	Jueves	11:45:00	12:30:00
74	2	201	Jueves	12:30:00	13:15:00
75	2	202	Viernes	07:00:00	07:45:00
76	2	203	Viernes	07:45:00	08:30:00
77	2	204	Viernes	08:30:00	09:15:00
78	2	205	Viernes	09:15:00	10:00:00
79	2	206	Viernes	10:15:00	11:00:00
80	2	207	Viernes	11:00:00	11:45:00
81	2	208	Viernes	11:45:00	12:30:00
82	2	209	Viernes	12:30:00	13:15:00
\.


--
-- TOC entry 4992 (class 0 OID 16536)
-- Dependencies: 224
-- Data for Name: materias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materias (id, nombre, profesor_id, curso_id) FROM stdin;
2	Literatura	2	\N
1	Matemáticas	5	\N
3	Ciencias	10	\N
100	Matemática	2	1
101	Lengua	2	1
102	Física	2	1
103	Historia	2	1
104	Biología	2	1
105	Geografía	2	1
106	Educación Física	2	1
107	Inglés	2	1
108	Química	2	1
109	Literatura	2	1
200	Matemática	2	2
201	Lengua	2	2
202	Física	2	2
203	Historia	2	2
204	Biología	2	2
205	Geografía	2	2
206	Educación Física	2	2
207	Inglés	2	2
208	Química	2	2
209	Literatura	2	2
\.


--
-- TOC entry 4988 (class 0 OID 16502)
-- Dependencies: 220
-- Data for Name: notas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notas (id, nota, usuario_id, materia_id) FROM stdin;
4	9.50	1	\N
3	9.50	1	3
2	9.50	1	2
1	4.50	1	1
5	7.00	1	1
6	2.00	1	2
7	6.00	1	3
8	6.00	7	1
9	9.50	7	3
10	8.00	1	1
\.


--
-- TOC entry 4986 (class 0 OID 16467)
-- Dependencies: 218
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre, apellido, email, dni, rol, "contraseña", curso_id) FROM stdin;
2	María	González	maria.gonzalez@email.com	87654321	profesor	\N	\N
3	Pedro	Ramírez	pedro.ramirez@email.com	11223344	admin	\N	\N
5	robert	perez	rperez@mail.com	44332211	profesor	\N	\N
8	agustin	rosas	arosas@mail.com	88776655	admin	$2b$12$OmRf6w2IUgHCPHdcPvyLZObaq86EVhDC/tFCGcVDqjb8XJLY4m0DW	\N
10	juan	disalvo	jdisalvo@mail.com	00112233	profesor	$2b$12$6j2JRhl3hEvnUfLw2vD7v.IIZ0CP/gP16J4Fzpmt66H9Q.60LqKOK	\N
1	Lucas	Martínez	lucas.martinez@email.com	12345678	alumno	\N	1
7	valentin	vaccari	vvaccari@mail.com	09876543	alumno	$2b$12$u7Vgf9ugw./as.Kw9//4D./Ats8867G5xkwZuYFlXHRpqCwm/lj8G	1
4	valentino	Castaldi	tinocast@gmail.com	45937484	alumno	12345678	3
12	juan	castaldi	jcastaldi@gmail.com	181164680	alumno	$2b$12$OUE.0SeHBZSxlnzE48JyXug/6lM5OQc22KH6Vun5J4b5TRSIOfv/y	\N
\.


--
-- TOC entry 5020 (class 0 OID 0)
-- Dependencies: 233
-- Name: acciones_recientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.acciones_recientes_id_seq', 1, false);


--
-- TOC entry 5021 (class 0 OID 0)
-- Dependencies: 221
-- Name: asistencias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.asistencias_id_seq', 4, true);


--
-- TOC entry 5022 (class 0 OID 0)
-- Dependencies: 225
-- Name: año_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."año_id_seq"', 6, true);


--
-- TOC entry 5023 (class 0 OID 0)
-- Dependencies: 235
-- Name: comunicados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comunicados_id_seq', 2, true);


--
-- TOC entry 5024 (class 0 OID 0)
-- Dependencies: 227
-- Name: cursos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cursos_id_seq', 12, true);


--
-- TOC entry 5025 (class 0 OID 0)
-- Dependencies: 231
-- Name: examenes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.examenes_id_seq', 3, true);


--
-- TOC entry 5026 (class 0 OID 0)
-- Dependencies: 229
-- Name: horarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horarios_id_seq', 82, true);


--
-- TOC entry 5027 (class 0 OID 0)
-- Dependencies: 223
-- Name: materias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materias_id_seq', 4, true);


--
-- TOC entry 5028 (class 0 OID 0)
-- Dependencies: 219
-- Name: notas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notas_id_seq', 10, true);


--
-- TOC entry 5029 (class 0 OID 0)
-- Dependencies: 217
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 12, true);


--
-- TOC entry 4822 (class 2606 OID 16721)
-- Name: acciones_recientes acciones_recientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acciones_recientes
    ADD CONSTRAINT acciones_recientes_pkey PRIMARY KEY (id);


--
-- TOC entry 4810 (class 2606 OID 16519)
-- Name: asistencias asistencias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencias
    ADD CONSTRAINT asistencias_pkey PRIMARY KEY (id);


--
-- TOC entry 4814 (class 2606 OID 16597)
-- Name: anio año_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anio
    ADD CONSTRAINT "año_pkey" PRIMARY KEY (id);


--
-- TOC entry 4824 (class 2606 OID 16732)
-- Name: comunicados comunicados_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comunicados
    ADD CONSTRAINT comunicados_pkey PRIMARY KEY (id);


--
-- TOC entry 4816 (class 2606 OID 16662)
-- Name: cursos cursos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cursos
    ADD CONSTRAINT cursos_pkey PRIMARY KEY (id);


--
-- TOC entry 4820 (class 2606 OID 16701)
-- Name: examenes examenes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examenes
    ADD CONSTRAINT examenes_pkey PRIMARY KEY (id);


--
-- TOC entry 4818 (class 2606 OID 16674)
-- Name: horarios horarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4812 (class 2606 OID 16541)
-- Name: materias materias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT materias_pkey PRIMARY KEY (id);


--
-- TOC entry 4808 (class 2606 OID 16507)
-- Name: notas notas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT notas_pkey PRIMARY KEY (id);


--
-- TOC entry 4802 (class 2606 OID 16477)
-- Name: usuarios usuarios_dni_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_dni_key UNIQUE (dni);


--
-- TOC entry 4804 (class 2606 OID 16475)
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- TOC entry 4806 (class 2606 OID 16473)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- TOC entry 4838 (class 2606 OID 16733)
-- Name: comunicados comunicados_emisor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comunicados
    ADD CONSTRAINT comunicados_emisor_id_fkey FOREIGN KEY (emisor_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 4839 (class 2606 OID 16738)
-- Name: comunicados comunicados_receptor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comunicados
    ADD CONSTRAINT comunicados_receptor_id_fkey FOREIGN KEY (receptor_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 4833 (class 2606 OID 16663)
-- Name: cursos cursos_anio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cursos
    ADD CONSTRAINT cursos_anio_id_fkey FOREIGN KEY (anio_id) REFERENCES public.anio(id);


--
-- TOC entry 4836 (class 2606 OID 16702)
-- Name: examenes examenes_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examenes
    ADD CONSTRAINT examenes_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.cursos(id);


--
-- TOC entry 4837 (class 2606 OID 16707)
-- Name: examenes examenes_materia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examenes
    ADD CONSTRAINT examenes_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES public.materias(id);


--
-- TOC entry 4831 (class 2606 OID 16685)
-- Name: materias fk_curso; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT fk_curso FOREIGN KEY (curso_id) REFERENCES public.cursos(id);


--
-- TOC entry 4826 (class 2606 OID 16560)
-- Name: notas fk_materia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_materia FOREIGN KEY (materia_id) REFERENCES public.materias(id);


--
-- TOC entry 4827 (class 2606 OID 16549)
-- Name: notas fk_materia_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_materia_id FOREIGN KEY (materia_id) REFERENCES public.materias(id) ON DELETE CASCADE;


--
-- TOC entry 4829 (class 2606 OID 16555)
-- Name: asistencias fk_materia_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencias
    ADD CONSTRAINT fk_materia_id FOREIGN KEY (materia_id) REFERENCES public.materias(id) ON DELETE CASCADE;


--
-- TOC entry 4830 (class 2606 OID 16525)
-- Name: asistencias fk_usuario_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asistencias
    ADD CONSTRAINT fk_usuario_id FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 4828 (class 2606 OID 16530)
-- Name: notas fk_usuario_id_notas; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_usuario_id_notas FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- TOC entry 4834 (class 2606 OID 16675)
-- Name: horarios horarios_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.cursos(id);


--
-- TOC entry 4835 (class 2606 OID 16680)
-- Name: horarios horarios_materia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES public.materias(id);


--
-- TOC entry 4832 (class 2606 OID 16544)
-- Name: materias materias_profesor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT materias_profesor_id_fkey FOREIGN KEY (profesor_id) REFERENCES public.usuarios(id);


--
-- TOC entry 4825 (class 2606 OID 16690)
-- Name: usuarios usuarios_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.cursos(id);


-- Completed on 2025-06-10 11:35:21

--
-- PostgreSQL database dump complete
--

--
-- Database "test_db" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-06-10 11:35:21

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4907 (class 1262 OID 16386)
-- Name: test_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE test_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es-AR';


ALTER DATABASE test_db OWNER TO postgres;

\connect test_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16387)
-- Name: persona; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.persona (
    id_persona integer NOT NULL,
    nombre character varying,
    email character varying,
    apellido character varying(255)
);


ALTER TABLE public.persona OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16390)
-- Name: persona_id_persona_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.persona_id_persona_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.persona_id_persona_seq OWNER TO postgres;

--
-- TOC entry 4908 (class 0 OID 0)
-- Dependencies: 218
-- Name: persona_id_persona_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.persona_id_persona_seq OWNED BY public.persona.id_persona;


--
-- TOC entry 220 (class 1259 OID 16406)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16399)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer DEFAULT nextval('public.usuario_id_usuario_seq'::regclass) NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 4747 (class 2604 OID 16391)
-- Name: persona id_persona; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persona ALTER COLUMN id_persona SET DEFAULT nextval('public.persona_id_persona_seq'::regclass);


--
-- TOC entry 4898 (class 0 OID 16387)
-- Dependencies: 217
-- Data for Name: persona; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.persona (id_persona, nombre, email, apellido) FROM stdin;
4	Valentino	vcastaldi@mail.com	Castaldi
7	marcos	mcanto@mail.com	cantu
8	angel	agangi@mail.com	gangi
9	carlos	clara@mail.com	lara
15	maria	mesparza@mail.com	esparza
21	pedro	pnajera@mail.com	najera
2	juan carlos	cjjuarez@mail.com	juarez
24	camilo	ctoilet@mail.com	toilet
\.


--
-- TOC entry 4900 (class 0 OID 16399)
-- Dependencies: 219
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, username, password) FROM stdin;
2	kgomze	123
1	jperez	456
5	pfrancisco	222
6	lsuarez	888
\.


--
-- TOC entry 4909 (class 0 OID 0)
-- Dependencies: 218
-- Name: persona_id_persona_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.persona_id_persona_seq', 24, true);


--
-- TOC entry 4910 (class 0 OID 0)
-- Dependencies: 220
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 6, true);


--
-- TOC entry 4750 (class 2606 OID 16398)
-- Name: persona persona_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persona
    ADD CONSTRAINT persona_pkey PRIMARY KEY (id_persona);


--
-- TOC entry 4752 (class 2606 OID 16405)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


-- Completed on 2025-06-10 11:35:23

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-06-10 11:35:23

--
-- PostgreSQL database cluster dump complete
--

