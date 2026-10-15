--
-- PostgreSQL database dump
--

\restrict bBEvhT0JiRbOsdc0cG1Prpa1go1SBvrjqLgaHOiQn2YFFScpLxfQm0tTU8Aa5op

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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
-- Name: assessorias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessorias (
    assessoria_id integer NOT NULL,
    nome character varying(250) NOT NULL,
    regiao_atuacao character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: assessorias_assessoria_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.assessorias ALTER COLUMN assessoria_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.assessorias_assessoria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clientes (
    cliente_id integer NOT NULL,
    regiao character varying(100) NOT NULL,
    estado character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: clientes_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.clientes ALTER COLUMN cliente_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.clientes_cliente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: contratos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contratos (
    contrato_id integer NOT NULL,
    cliente_id integer,
    assessoria_id integer,
    data_contratacao date NOT NULL,
    data_vencimento date NOT NULL,
    valor_divida numeric(12,2) NOT NULL,
    status_contrato character varying(30) DEFAULT 'Em Aberto'::character varying NOT NULL,
    data_carga date DEFAULT CURRENT_DATE NOT NULL,
    numero_parcelas integer DEFAULT 1 NOT NULL,
    CONSTRAINT chk_periodo_valido CHECK (((data_contratacao >= '2023-01-01'::date) AND (data_contratacao <= '2026-10-01'::date))),
    CONSTRAINT contratos_numero_parcelas_check CHECK (((numero_parcelas >= 1) AND (numero_parcelas <= 24))),
    CONSTRAINT contratos_status_contrato_check CHECK (((status_contrato)::text = ANY ((ARRAY['Em Aberto'::character varying, 'Quitado'::character varying, 'Renegociado'::character varying, 'Cancelado'::character varying])::text[]))),
    CONSTRAINT contratos_valor_divida_check CHECK ((valor_divida >= (0)::numeric))
);


--
-- Name: contratos_contrato_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.contratos ALTER COLUMN contrato_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.contratos_contrato_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: interacoes_cobrancas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interacoes_cobrancas (
    interacao_id integer NOT NULL,
    contrato_id integer,
    data_interacao timestamp with time zone NOT NULL,
    canal_interacao character varying(30) NOT NULL,
    status_interacao character varying(50) NOT NULL,
    resultado character varying(50),
    CONSTRAINT interacoes_cobrancas_canal_interacao_check CHECK (((canal_interacao)::text = ANY ((ARRAY['WhatsApp'::character varying, 'SMS'::character varying, 'Telefonia'::character varying, 'E-mail'::character varying, 'Carta'::character varying])::text[]))),
    CONSTRAINT interacoes_cobrancas_resultado_check CHECK (((resultado)::text = ANY ((ARRAY['Promessa de pagamento'::character varying, 'Acordo Fechado'::character varying, 'Boleto 2ªVia Enviado'::character varying, 'Pix Gerado'::character varying, 'Contestação'::character varying, 'Cliente Alega Pago'::character varying, 'Sem Resposta'::character varying, 'Telefone Inexistente'::character varying, 'Recusa de Contato'::character varying, 'Mensagem Entregue'::character varying, 'Recusa de Acordo'::character varying, 'Sem Previsão'::character varying])::text[]))),
    CONSTRAINT interacoes_cobrancas_status_interacao_check CHECK (((status_interacao)::text = ANY ((ARRAY['Sucesso'::character varying, 'Em Negociação'::character varying, 'Insucesso Operacional'::character varying, 'Recusa'::character varying])::text[])))
);


--
-- Name: interacoes_cobrancas_interacao_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.interacoes_cobrancas ALTER COLUMN interacao_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.interacoes_cobrancas_interacao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pagamentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pagamentos (
    pagamento_id integer NOT NULL,
    contrato_id integer,
    data_pagamento timestamp without time zone,
    valor_pagamento numeric(12,2) NOT NULL,
    forma_pagamento character varying(30) NOT NULL,
    CONSTRAINT pagamentos_forma_pagamento_check CHECK (((forma_pagamento)::text = ANY ((ARRAY['Pix'::character varying, 'Boleto'::character varying, 'Transferência Bancária'::character varying, 'Cartão de Crédito'::character varying])::text[]))),
    CONSTRAINT pagamentos_valor_pagamento_check CHECK ((valor_pagamento > (0)::numeric))
);


--
-- Name: pagamentos_pagamento_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.pagamentos ALTER COLUMN pagamento_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.pagamentos_pagamento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: vw_contratos_faixa_atraso; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.vw_contratos_faixa_atraso AS
 WITH contratos_calculado AS (
         SELECT c.contrato_id,
            c.cliente_id,
            c.assessoria_id,
            a.nome AS nome_assessoria,
            c.data_contratacao,
            c.data_vencimento,
            c.valor_divida,
            c.status_contrato,
            c.data_carga,
                CASE
                    WHEN (((c.status_contrato)::text = 'Em Aberto'::text) AND (c.data_carga > c.data_vencimento)) THEN (c.data_carga - c.data_vencimento)
                    ELSE 0
                END AS dias_atraso
           FROM (public.contratos c
             JOIN public.assessorias a ON ((c.assessoria_id = a.assessoria_id)))
        )
 SELECT contrato_id,
    cliente_id,
    assessoria_id,
    nome_assessoria,
    data_contratacao,
    data_vencimento,
    valor_divida,
    status_contrato,
    data_carga,
    dias_atraso,
        CASE
            WHEN (dias_atraso = 0) THEN 'Em dia'::text
            WHEN ((dias_atraso >= 1) AND (dias_atraso <= 30)) THEN 'Até 30 dias'::text
            WHEN ((dias_atraso >= 31) AND (dias_atraso <= 60)) THEN 'Até 60 dias'::text
            WHEN ((dias_atraso >= 61) AND (dias_atraso <= 90)) THEN 'Até 90 dias'::text
            WHEN ((dias_atraso >= 91) AND (dias_atraso <= 180)) THEN 'Até 180 dias'::text
            WHEN ((dias_atraso >= 181) AND (dias_atraso <= 360)) THEN 'Até 360 dias'::text
            ELSE 'Mais de 360 dias'::text
        END AS faixa_atraso
   FROM contratos_calculado;


--
-- Name: assessorias assessorias_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessorias
    ADD CONSTRAINT assessorias_pkey PRIMARY KEY (assessoria_id);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (cliente_id);


--
-- Name: contratos contratos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contratos
    ADD CONSTRAINT contratos_pkey PRIMARY KEY (contrato_id);


--
-- Name: interacoes_cobrancas interacoes_cobrancas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interacoes_cobrancas
    ADD CONSTRAINT interacoes_cobrancas_pkey PRIMARY KEY (interacao_id);


--
-- Name: pagamentos pagamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagamentos
    ADD CONSTRAINT pagamentos_pkey PRIMARY KEY (pagamento_id);


--
-- Name: idx_contratos_assessoria; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_contratos_assessoria ON public.contratos USING btree (assessoria_id);


--
-- Name: idx_contratos_cliente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_contratos_cliente ON public.contratos USING btree (cliente_id);


--
-- Name: idx_interacoes_contrato; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_interacoes_contrato ON public.interacoes_cobrancas USING btree (contrato_id);


--
-- Name: idx_oagamentos_contrato; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_oagamentos_contrato ON public.pagamentos USING btree (contrato_id);


--
-- Name: contratos contratos_assessoria_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contratos
    ADD CONSTRAINT contratos_assessoria_id_fkey FOREIGN KEY (assessoria_id) REFERENCES public.assessorias(assessoria_id) ON DELETE SET NULL;


--
-- Name: contratos contratos_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contratos
    ADD CONSTRAINT contratos_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(cliente_id) ON DELETE RESTRICT;


--
-- Name: interacoes_cobrancas interacoes_cobrancas_contrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interacoes_cobrancas
    ADD CONSTRAINT interacoes_cobrancas_contrato_id_fkey FOREIGN KEY (contrato_id) REFERENCES public.contratos(contrato_id) ON DELETE CASCADE;


--
-- Name: pagamentos pagamentos_contrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagamentos
    ADD CONSTRAINT pagamentos_contrato_id_fkey FOREIGN KEY (contrato_id) REFERENCES public.contratos(contrato_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict bBEvhT0JiRbOsdc0cG1Prpa1go1SBvrjqLgaHOiQn2YFFScpLxfQm0tTU8Aa5op

