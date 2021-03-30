--
-- PostgreSQL database dump
--

-- Dumped from database version 10.11
-- Dumped by pg_dump version 10.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: DataSearch_existingdata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."DataSearch_existingdata" (
    id integer NOT NULL,
    work character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(32) NOT NULL,
    search character varying(255) NOT NULL,
    source_title character varying(255),
    disclaimer_req boolean NOT NULL,
    citation character varying(2048) NOT NULL,
    date_accessed timestamp with time zone NOT NULL,
    comments character varying(2048),
    created_by_id integer NOT NULL,
    source_id integer NOT NULL,
    keywords character varying(1024),
    url character varying(255)
);


ALTER TABLE public."DataSearch_existingdata" OWNER TO postgres;

--
-- Name: DataSearch_existingdata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."DataSearch_existingdata_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."DataSearch_existingdata_id_seq" OWNER TO postgres;

--
-- Name: DataSearch_existingdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."DataSearch_existingdata_id_seq" OWNED BY public."DataSearch_existingdata".id;


--
-- Name: DataSearch_existingdata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSearch_existingdata" ALTER COLUMN id SET DEFAULT nextval('public."DataSearch_existingdata_id_seq"'::regclass);


--
-- Data for Name: DataSearch_existingdata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."DataSearch_existingdata" (id, work, email, phone, search, source_title, disclaimer_req, citation, date_accessed, comments, created_by_id, source_id, keywords, url) FROM stdin;
12	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Plastic Contamination	UK Waste Strategy: Bioeconomy Opportunities Aplenty	f	Bob Horton, Jeremy Tomkinson, and Adrian Higson.Industrial Biotechnology.Apr 2019.ahead of printhttp://doi.org/10.1089/ind.2019.29161.bho	2019-11-04 10:40:33.876546-05		1	5		https://www.liebertpub.com/doi/abs/10.1089/ind.2019.29161.bho?journalCode=ind
1	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Plastic	Co-pyrolysis characteristics and kinetic analysis of organic food waste and plastic	t	https://www.sciencedirect.com/science/article/pii/S0960852417317893	2019-10-25 08:40:43-04	https://www.sciencedirect.com/science/article/pii/S0960852417317893	1	1	\N	https://www.sciencedirect.com/science/article/pii/S0960852417317893/
4	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Recovery	Comparison through a LCA evaluation analysis of food waste disposal options from the perspective of global warming and resource recovery	f	Mi-Hyung Kim, Jung-Wk Kim. Elsevier.  https://www.sciencedirect.com/science/article/pii/S0048969710004456. https://doi.org/10.1016/j.scitotenv.2010.04.049.	2019-10-30 06:23:24-04	Keywords: Food waste management,  Life cycle assessment, Resource recovery, Environmental impacts.	1	1	\N	https://www.sciencedirect.com/science/article/pii/S0048969710004456?via%3Dihub
5	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Recovery Environmental Engineering	Sustainable Management of Coffee and Cocoa Agro-Waste	f	Pushpa S. Murthy (Central Food Technological Research Institute, India), Nivas Manohar Desai (Central Food Technological Research Institute, India) and Siridevi G. B. (Central Food Technological Research Institute, India).	2019-10-30 06:32:37-04	https://www.igi-global.com/chapter/sustainable-management-of-coffee-and-cocoa-agro-waste/222995	1	1	\N	https://www.igi-global.com/chapter/sustainable-management-of-coffee-and-cocoa-agro-waste/222995
6	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	food waste disposal options	Life cycle assessment (LCA) of food waste treatment in Hong Kong: On-site fermentation methodology	f	Journal of Environmental Management. Volume 240, 15 June 2019, Pages 343-351. https://www.sciencedirect.com/science/article/pii/S0301479719304323.	2019-10-30 06:47:29-04	This paper utilizes Life Cycle Assessment (LCA) to determine the environmental impacts associated with this S-FRB technology and identify environmental hotspots to reduce these impacts. In this paper, we have conducted an on-site pilot-scale study for 2 months at a canteen located at the City University of Hong Kong, which resulted in a 90% reduction in the mass of food waste treated in the S-FRB system.	1	1	\N	https://www.sciencedirect.com/science/article/pii/S0301479719304323
8	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Recycle	Recycle food wastes into high quality fish feeds for safe and quality fish production	f	Ming-Hung Wonga, Wing-Yin Mo, Wai-Ming Choi, Zhang Cheng, Yu-Bon Man.  "Recycle food wastes into high quality fish feeds for safe and quality fish production." Elsevier. Environmental Pollution, Volume 219, December 2016, Pages 631-638. https://doi.org/10.1016/j.envpol.2016.06.035.	2019-10-30 14:41:06-04	\N	1	1	\N	https://doi.org/10.1016/j.envpol.2016.06.035
10	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste De-Packaging	The sounding side of materials and products. A sensory interaction revaluated in the user-experience	f	Lerma, Beatrice (2019)  Cuaderno 94. "The sounding side of materials and products. A sensory interaction revaluated in the user-experience." Pages 99 thru 107. Cuaderno 94 |  Centro de Estudios en Diseño y Comunicación (2020/2021). pp 99 - 107  ISSN 1668-0227. Accessed 11/1/2019. https://fido.palermo.edu/servicios_dyc/publicacionesdc/archivos/777_libro.pdf#page=99.	2019-11-01 06:11:49-04	\N	1	1	\N	https://fido.palermo.edu/servicios_dyc/publicacionesdc/archivos/777_libro.pdf#page=99
11	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	plastic waste in food	Feasibility Study on the Application of Fabricated Multipurpose Food Packaging Plastic (MFPP) Liner as Alternative Landfill Liner Material in Sustainable Landfill Infrastructure Model	f	Feasibility Study on the Application of Fabricated Multipurpose Food Packaging Plastic (MFPP) Liner as Alternative Landfill Liner Material in Sustainable Landfill Infrastructure Model. https://www.scientific.net/KEM.821.343.	2019-11-01 08:59:06-04	Multipurpose Food Packaging Plastic (MFPP) is one of the largest residential and commercial solid waste all over the world. BWP is categorized under Non-Biodegradable Plastic Waste (N-BPW). Due to its inability to degrade, this abundance of N-BPW caused space decrement in landfill. Many methods have been proposed for recycling of N-BPW such as incorporating N-BPW into road construction and added material in concrete production. In the present study, the feasibility of using MFPP as landfill liner material is studied through a series of laboratory testing in terms of mechanical and chemical characteristics. The liner sample was prepared in terms of a fabricated layer (combination of 60 layers (Sample A) and 80 layers (Sample B) of a single plastic). The fabricated layers were prepared by applying hot-pressing technique to increase the strength of the surface attachment between each of the layers. The prepared fabricated MFPP liners were tested for Ultimate Tensile Strength Test (UTS), Scanning Electron Microscopy (SEM) and X-Ray Distraction (XRD). The tested samples were then compared with the Conventional Geomembranes (GMs). Obtained results indicated that proposed fabricated MFPP Liner had 70% similar characteristics to GMs. In addition, the fabricated MFPP Liners have an ability to sustain maximum loading higher than Conventional GMs. These desirable characteristics indicated that the fabricated MFPP Liners has potential to be used as landfill liner material.	1	1	\N	https://www.scientific.net/KEM.821.343
13	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	USEEIO model	Method for endogenizing capital in the United States Environmentally‐Extended Input‐Output model	f	https://doi.org/10.1111/jiec.12931	2019-11-06 10:54:23.335089-05	Each year businesses, governments, and homeowners in the United States invest around one fifth of gross domestic product into the creation of capital assets such as buildings, machinery, and software to enable production and consumption.	1	5		https://onlinelibrary.wiley.com/doi/abs/10.1111/jiec.12931
3	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste De-Packaging	Systems and Methods for Enviornmentally Undisruptive Disposal of Food Waste	f	https://patentimages.storage.googleapis.com/5b/19/87/07322cddd0a739/US20100071602A1.pdf	2019-10-25 08:41:05-04	Abstract. A processing facility can dispose of food waste in environmentally un-disruptive manners. The processing facility can convert the food waste into bio-energy and bio-fuel products, such as bio-diesel, ethanol, and electricity. The processing facility can sort the food waste based on the fats or carbohydrates content of the food waste, and the processing facility can include a fluidized bed combustion module for combusting portions of the food waste.	1	1	\N	https://patentimages.storage.googleapis.com/5b/19/87/07322cddd0a739/US20100071602A1.pdf
14	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Laboratory Analysis	Food Analysis Laboratory Manual	f	Nielsen, Suzanne 2017. Food Analysis Laboratory Manual. Springer International Publishing.	2019-12-18 06:27:34.643116-05	This third edition laboratory manual was written to accompany Food Analysis, Fifth Edition, by the same author. New to this third edition of the laboratory manual are four introductory chapters that complement both the textbook chapters and the laboratory exercises.  The 24 laboratory exercises in the manual cover 21 of the 35 chapters in the textbook. DOI: 10.1007/978-3-319-44127-6. ISBN: 9783319441276 (online) 9783319441252 (print).	1	2	Industrial Chemistry/Chemical Engineering, Food Science, Spectroscopy/Spectrometry, Chemistry, Chemical engineering, Food science, Spectroscopy	https://www.springer.com/gp/book/9783319441252#aboutAuthors
15	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Analysis Laboratories in USA	Food Labs and Services	f	N/A	2019-12-18 06:45:10.72643-05	This is a food waste testing lab and we need to add 'OTHER' as an option for SOURCE... placed temporarily under proceedings.	1	8	Testing services, training, consulting, auditing, certification, on-site testing, product design, research, development	https://www.eurofinsus.com/food/
16	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Data Set .xlxs	FUSIONS Food waste data set for EU-28 New Estimates and Environmental Impact	f	N/A	2019-12-19 06:41:07.711969-05	Food waste is an issue of importance to global food security and good environmental governance, directly linked with all aspects of sustainability (e.g. availability of resources, increasing costs and health). The amount of food produced but not consumed leads to negative impacts throughout the food supply chain and households. There is a pressing need to prevent food waste to make the transition to a resource efficient Europe. Previous studies show the necessity for more consistent and comparable data in order to decrease the uncertainties and making it possible to better understand the magnitude of the problem, and the scale of the potential opportunities.	1	1	Food supply chain and Food waste	https://ec.europa.eu/food/sites/food/files/safety/docs/fw_lib_fw_expo2015_fusions_data-set_151015.pdf
17	ORD/CESER/LRTD	young.daniel@epa.gov	513-569-7451	Coffee grounds recycling	17 Genius Ways To Recycle Used Coffee Grounds	f	Editorial Team, Natural Living Ideas.com, https://www.naturallivingideas.com/recycle-used-coffee-grounds/. Accessed January 7, 2020.	2020-01-07 07:50:38.212794-05		1	11	coffee, grounds, reuse	https://www.naturallivingideas.com/recycle-used-coffee-grounds/
18	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	A Winning Formula: Making Connections to Turn Food Waste into Energy	A Winning Formula: Making Connections to Turn Food Waste into Energy	f	N/A	2020-01-08 04:47:55.057339-05	N/A	1	1		https://www.epa.gov/sciencematters/winning-formula-making-connections-turn-food-waste-energy
19	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Food Waste Sampling	An interdisciplinary living laboratory approach to investigate college food waste co-composting with additional on-site organic waste feedstocks	f	Anne B. Alerding, Jennifer E. DeHart, David K. Kniffin, Nattachat Srikongyos, Michael J. DeBlasio, Jacob M. Kelliher, James A. Marsh, Heather L. Magill, Charles D. Newhouse, Samuel K. Allen, Paul J. Ackerman, and Emily L. Lilly\r\nInternational Journal of Environment and Waste Management 2019 24:1, 61-80.	2020-01-08 06:42:34.418278-05	In an effort to curb the monetary and environmental costs of food waste disposal, colleges and universities are developing composting programs. Incorporating additional on-site wastes could improve composting efficiency and provide cost savings.	1	5	aerated static pile, ASP, bacteria, compost, food waste, living laboratory, waste management, organic waste, co-composting	https://www.inderscienceonline.com/doi/abs/10.1504/IJEWM.2019.100658
20	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	microsplastics in food	Microplastics, a food safety issue?	f	Rainieri S., Barranco A. (2019)  Trends in Food Science and Technology,  84 , pp. 55-57.	2020-01-28 13:43:36.483507-05	Review Description\r\nThe risk posed by microplastics for human and environment, has become a hot topic. The concern is focused not only on the effect of microplastics as such but also on additives and chemical contaminants absorbed by microplastics that may be released and affect negatively animals and environmental health. Despite several works have been written on this topic, a number of knowledge gaps still should be filled to enable a correct risk assessment of this important issue. For example, the relevance of microplastics for food safety has not yet been fully established and scientific results aimed at establishing a possible health risk for contaminants associated with microplastics are rather controversial. The risk assessment of microplastics in foodstuff is still at a very early stage and very few studies on the monitoring of microplastics in foodstuff and their effects on human health are available. Additionally, it is difficult to compare results from different studies as methodologies and study designs are not uniform. For this reason, it is not always possible to reach some definitive conclusion. This work sets out to complement the reviews and statements already existing, by updating the information and identifying if any of the knowledge gaps have been covered and if further ones have been detected with the final aim of properly assessing and managing this emerging risk.	1	5	Microplastics\r\nPOPs\r\nToxicity\r\nNanoplastics\r\nRisk assessment	https://www.sciencedirect.com/science/article/abs/pii/S0924224417303898
21	ORD/CESER/LRTD/EDAB	young.daniel@epa.gov	(513) 569-7451	Effects of food presence on microplastic ingestion and egestion in Mytilus galloprovincialis	Effects of food presence on microplastic ingestion and egestion in Mytilus galloprovincialis	t	xxx	2020-01-29 09:32:20.168344-05	Research on plastic pollution in marine environments has increased exponentially in the recent decades (Strungaru et al., 2019, Alimba and Faggio, 2019). In particular, small particles of manufactured or weathered plastic (microplastics (MPs), <5 mm), characterized by global abundance, have been studied extensively. MPs are widely distributed and have been monitored in polar regions (Lusher et al., 2015, Waller et al., 2017), tropical regions (Lima et al., 2014, Do Sul et al., 2014), the East (Ng and Obbard, 2006, Isobe et al., 2015), the West (Claessens et al., 2011, Collignon et al., 2012, Alomar et al., 2016, Bellas et al., 2016), coastal areas (de Lucia et al., 2014, Stolte et al., 2015), open seas (Reisser et al., 2014, Romeo et al., 2015), sea surfaces (Song et al., 2014, Song et al., 2015), and the deep sea (Van Cauwenberghe et al., 2013, Taylor et al., 2016).	1	5	Plastic particle, Mussel, Egestion rate, Mytilus gallo, provincialis marine pollution	https://www.sciencedirect.com/science/article/pii/S0045653519320946
\.


--
-- Name: DataSearch_existingdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."DataSearch_existingdata_id_seq"', 21, true);


--
-- Name: DataSearch_existingdata DataSearch_existingdata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSearch_existingdata"
    ADD CONSTRAINT "DataSearch_existingdata_pkey" PRIMARY KEY (id);


--
-- Name: DataSearch_existingdata_created_by_id_11974ff1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "DataSearch_existingdata_created_by_id_11974ff1" ON public."DataSearch_existingdata" USING btree (created_by_id);


--
-- Name: DataSearch_existingdata_source_id_f5c82b8d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "DataSearch_existingdata_source_id_f5c82b8d" ON public."DataSearch_existingdata" USING btree (source_id);


--
-- Name: DataSearch_existingdata DataSearch_existingda_source_id_f5c82b8d_fk_DataSearch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSearch_existingdata"
    ADD CONSTRAINT "DataSearch_existingda_source_id_f5c82b8d_fk_DataSearch" FOREIGN KEY (source_id) REFERENCES public."DataSearch_existingdatasource"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: DataSearch_existingdata DataSearch_existingdata_created_by_id_11974ff1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSearch_existingdata"
    ADD CONSTRAINT "DataSearch_existingdata_created_by_id_11974ff1_fk_auth_user_id" FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

