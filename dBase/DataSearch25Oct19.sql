PGDMP     "                	    w        	   FoodWaste    10.5    10.5 �    O           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            P           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            Q           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            R           1262    448054 	   FoodWaste    DATABASE     �   CREATE DATABASE "FoodWaste" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE "FoodWaste";
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            S           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            T           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    464503    FoodWaste_attachment    TABLE     �   CREATE TABLE public."FoodWaste_attachment" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    file character varying(100),
    uploaded_by_id integer NOT NULL
);
 *   DROP TABLE public."FoodWaste_attachment";
       public         postgres    false    3            �            1259    464501    FoodWaste_attachment_id_seq    SEQUENCE     �   CREATE SEQUENCE public."FoodWaste_attachment_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public."FoodWaste_attachment_id_seq";
       public       postgres    false    238    3            U           0    0    FoodWaste_attachment_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public."FoodWaste_attachment_id_seq" OWNED BY public."FoodWaste_attachment".id;
            public       postgres    false    237            �            1259    464511    FoodWaste_dataattachmentmap    TABLE     �   CREATE TABLE public."FoodWaste_dataattachmentmap" (
    id integer NOT NULL,
    attachment_id integer NOT NULL,
    data_id integer NOT NULL
);
 1   DROP TABLE public."FoodWaste_dataattachmentmap";
       public         postgres    false    3            �            1259    464509 "   FoodWaste_dataattachmentmap_id_seq    SEQUENCE     �   CREATE SEQUENCE public."FoodWaste_dataattachmentmap_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public."FoodWaste_dataattachmentmap_id_seq";
       public       postgres    false    240    3            V           0    0 "   FoodWaste_dataattachmentmap_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public."FoodWaste_dataattachmentmap_id_seq" OWNED BY public."FoodWaste_dataattachmentmap".id;
            public       postgres    false    239            �            1259    464583    FoodWaste_existingdata    TABLE     �  CREATE TABLE public."FoodWaste_existingdata" (
    id integer NOT NULL,
    work character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(32) NOT NULL,
    search character varying(255) NOT NULL,
    article_title character varying(255) NOT NULL,
    disclaimer_req boolean NOT NULL,
    citation character varying(512) NOT NULL,
    date_accessed timestamp with time zone NOT NULL,
    comments character varying(1024),
    created_by_id integer NOT NULL
);
 ,   DROP TABLE public."FoodWaste_existingdata";
       public         postgres    false    3            �            1259    464581    FoodWaste_existingdata_id_seq    SEQUENCE     �   CREATE SEQUENCE public."FoodWaste_existingdata_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public."FoodWaste_existingdata_id_seq";
       public       postgres    false    242    3            W           0    0    FoodWaste_existingdata_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public."FoodWaste_existingdata_id_seq" OWNED BY public."FoodWaste_existingdata".id;
            public       postgres    false    241            �            1259    464594 $   FoodWaste_existingdatasharingteammap    TABLE     �   CREATE TABLE public."FoodWaste_existingdatasharingteammap" (
    id integer NOT NULL,
    added_date timestamp with time zone NOT NULL,
    can_edit boolean NOT NULL,
    data_id integer NOT NULL,
    team_id integer NOT NULL
);
 :   DROP TABLE public."FoodWaste_existingdatasharingteammap";
       public         postgres    false    3            �            1259    464592 +   FoodWaste_existingdatasharingteammap_id_seq    SEQUENCE     �   CREATE SEQUENCE public."FoodWaste_existingdatasharingteammap_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 D   DROP SEQUENCE public."FoodWaste_existingdatasharingteammap_id_seq";
       public       postgres    false    244    3            X           0    0 +   FoodWaste_existingdatasharingteammap_id_seq    SEQUENCE OWNED BY        ALTER SEQUENCE public."FoodWaste_existingdatasharingteammap_id_seq" OWNED BY public."FoodWaste_existingdatasharingteammap".id;
            public       postgres    false    243            �            1259    448182    accounts_country    TABLE     �   CREATE TABLE public.accounts_country (
    id integer NOT NULL,
    country character varying(255),
    abbreviation character varying(4) NOT NULL,
    flag character varying(255)
);
 $   DROP TABLE public.accounts_country;
       public         postgres    false    3            �            1259    448180    accounts_country_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_country_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.accounts_country_id_seq;
       public       postgres    false    3    213            Y           0    0    accounts_country_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.accounts_country_id_seq OWNED BY public.accounts_country.id;
            public       postgres    false    212            �            1259    448193    accounts_role    TABLE     `   CREATE TABLE public.accounts_role (
    id integer NOT NULL,
    role character varying(255)
);
 !   DROP TABLE public.accounts_role;
       public         postgres    false    3            �            1259    448191    accounts_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.accounts_role_id_seq;
       public       postgres    false    3    215            Z           0    0    accounts_role_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.accounts_role_id_seq OWNED BY public.accounts_role.id;
            public       postgres    false    214            �            1259    448201    accounts_sector    TABLE     d   CREATE TABLE public.accounts_sector (
    id integer NOT NULL,
    sector character varying(255)
);
 #   DROP TABLE public.accounts_sector;
       public         postgres    false    3            �            1259    448199    accounts_sector_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_sector_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.accounts_sector_id_seq;
       public       postgres    false    3    217            [           0    0    accounts_sector_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.accounts_sector_id_seq OWNED BY public.accounts_sector.id;
            public       postgres    false    216            �            1259    448209    accounts_state    TABLE     �   CREATE TABLE public.accounts_state (
    id integer NOT NULL,
    state character varying(255) NOT NULL,
    abbreviation character varying(4) NOT NULL,
    country_id integer
);
 "   DROP TABLE public.accounts_state;
       public         postgres    false    3            �            1259    448207    accounts_state_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.accounts_state_id_seq;
       public       postgres    false    3    219            \           0    0    accounts_state_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.accounts_state_id_seq OWNED BY public.accounts_state.id;
            public       postgres    false    218            �            1259    448217    accounts_userprofile    TABLE     	  CREATE TABLE public.accounts_userprofile (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    last_modified timestamp with time zone NOT NULL,
    affiliation character varying(255),
    job_title character varying(255),
    address_line1 character varying(255),
    address_line2 character varying(255),
    city character varying(255),
    zipcode character varying(255),
    country_id integer,
    role_id integer,
    sector_id integer,
    state_id integer,
    user_id integer NOT NULL
);
 (   DROP TABLE public.accounts_userprofile;
       public         postgres    false    3            �            1259    448215    accounts_userprofile_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_userprofile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.accounts_userprofile_id_seq;
       public       postgres    false    221    3            ]           0    0    accounts_userprofile_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.accounts_userprofile_id_seq OWNED BY public.accounts_userprofile.id;
            public       postgres    false    220            �            1259    448086 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         postgres    false    3            �            1259    448084    auth_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public       postgres    false    3    203            ^           0    0    auth_group_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
            public       postgres    false    202            �            1259    448096    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         postgres    false    3            �            1259    448094    auth_group_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public       postgres    false    205    3            _           0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
            public       postgres    false    204            �            1259    448078    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         postgres    false    3            �            1259    448076    auth_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public       postgres    false    201    3            `           0    0    auth_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
            public       postgres    false    200            �            1259    448104 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         postgres    false    3            �            1259    448114    auth_user_groups    TABLE        CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         postgres    false    3            �            1259    448112    auth_user_groups_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.auth_user_groups_id_seq;
       public       postgres    false    3    209            a           0    0    auth_user_groups_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;
            public       postgres    false    208            �            1259    448102    auth_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.auth_user_id_seq;
       public       postgres    false    207    3            b           0    0    auth_user_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;
            public       postgres    false    206            �            1259    448122    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         postgres    false    3            �            1259    448120 !   auth_user_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.auth_user_user_permissions_id_seq;
       public       postgres    false    3    211            c           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;
            public       postgres    false    210            �            1259    448270    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         postgres    false    3            �            1259    448268    django_admin_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public       postgres    false    3    223            d           0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
            public       postgres    false    222            �            1259    448068    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         postgres    false    3            �            1259    448066    django_content_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public       postgres    false    3    199            e           0    0    django_content_type_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
            public       postgres    false    198            �            1259    448057    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         postgres    false    3            �            1259    448055    django_migrations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.django_migrations_id_seq;
       public       postgres    false    3    197            f           0    0    django_migrations_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
            public       postgres    false    196            �            1259    448301    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         postgres    false    3            �            1259    448313    support_informationrequest    TABLE     �  CREATE TABLE public.support_informationrequest (
    id integer NOT NULL,
    created_date timestamp with time zone NOT NULL,
    sent_to_email character varying(255),
    requestor_first_name character varying(255) NOT NULL,
    requestor_last_name character varying(255) NOT NULL,
    requestor_email_address character varying(255) NOT NULL,
    request_subject character varying(255) NOT NULL,
    request_details text NOT NULL,
    response text,
    response_date date
);
 .   DROP TABLE public.support_informationrequest;
       public         postgres    false    3            �            1259    448311 !   support_informationrequest_id_seq    SEQUENCE     �   CREATE SEQUENCE public.support_informationrequest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.support_informationrequest_id_seq;
       public       postgres    false    3    226            g           0    0 !   support_informationrequest_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.support_informationrequest_id_seq OWNED BY public.support_informationrequest.id;
            public       postgres    false    225            �            1259    448324    support_priority    TABLE     s  CREATE TABLE public.support_priority (
    id integer NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone,
    created_by character varying(255),
    last_modified_by character varying(255),
    name character varying(255),
    the_description text,
    weblink character varying(255),
    ordering numeric(10,1),
    user_id integer
);
 $   DROP TABLE public.support_priority;
       public         postgres    false    3            �            1259    448322    support_priority_id_seq    SEQUENCE     �   CREATE SEQUENCE public.support_priority_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.support_priority_id_seq;
       public       postgres    false    3    228            h           0    0    support_priority_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.support_priority_id_seq OWNED BY public.support_priority.id;
            public       postgres    false    227            �            1259    448335    support_support    TABLE     �  CREATE TABLE public.support_support (
    id integer NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone,
    created_by character varying(255),
    last_modified_by character varying(255),
    make_public character varying(5),
    share_with_user_group character varying(5),
    attachment character varying(100),
    name character varying(255),
    subject character varying(255),
    length_of_reference character varying(255),
    author character varying(255),
    is_closed character varying(5),
    the_description text,
    resolution text,
    weblink character varying(255),
    ordering numeric(10,1),
    date_resolved date,
    priority_id integer,
    support_type_id integer,
    user_id integer
);
 #   DROP TABLE public.support_support;
       public         postgres    false    3            �            1259    448333    support_support_id_seq    SEQUENCE     �   CREATE SEQUENCE public.support_support_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.support_support_id_seq;
       public       postgres    false    230    3            i           0    0    support_support_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.support_support_id_seq OWNED BY public.support_support.id;
            public       postgres    false    229            �            1259    448346    support_supporttype    TABLE     v  CREATE TABLE public.support_supporttype (
    id integer NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone,
    created_by character varying(255),
    last_modified_by character varying(255),
    name character varying(255),
    the_description text,
    weblink character varying(255),
    ordering numeric(10,1),
    user_id integer
);
 '   DROP TABLE public.support_supporttype;
       public         postgres    false    3            �            1259    448344    support_supporttype_id_seq    SEQUENCE     �   CREATE SEQUENCE public.support_supporttype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.support_supporttype_id_seq;
       public       postgres    false    3    232            j           0    0    support_supporttype_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.support_supporttype_id_seq OWNED BY public.support_supporttype.id;
            public       postgres    false    231            �            1259    448387 
   teams_team    TABLE       CREATE TABLE public.teams_team (
    id integer NOT NULL,
    created_date timestamp with time zone,
    last_modified_date timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    created_by_id integer NOT NULL,
    last_modified_by_id integer
);
    DROP TABLE public.teams_team;
       public         postgres    false    3            �            1259    448385    teams_team_id_seq    SEQUENCE     �   CREATE SEQUENCE public.teams_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.teams_team_id_seq;
       public       postgres    false    234    3            k           0    0    teams_team_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.teams_team_id_seq OWNED BY public.teams_team.id;
            public       postgres    false    233            �            1259    448395    teams_teammembership    TABLE     �   CREATE TABLE public.teams_teammembership (
    id integer NOT NULL,
    added_date timestamp with time zone NOT NULL,
    is_owner boolean NOT NULL,
    can_edit boolean NOT NULL,
    member_id integer NOT NULL,
    team_id integer NOT NULL
);
 (   DROP TABLE public.teams_teammembership;
       public         postgres    false    3            �            1259    448393    teams_teammembership_id_seq    SEQUENCE     �   CREATE SEQUENCE public.teams_teammembership_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.teams_teammembership_id_seq;
       public       postgres    false    3    236            l           0    0    teams_teammembership_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.teams_teammembership_id_seq OWNED BY public.teams_teammembership.id;
            public       postgres    false    235                       2604    464506    FoodWaste_attachment id    DEFAULT     �   ALTER TABLE ONLY public."FoodWaste_attachment" ALTER COLUMN id SET DEFAULT nextval('public."FoodWaste_attachment_id_seq"'::regclass);
 H   ALTER TABLE public."FoodWaste_attachment" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    238    237    238                       2604    464514    FoodWaste_dataattachmentmap id    DEFAULT     �   ALTER TABLE ONLY public."FoodWaste_dataattachmentmap" ALTER COLUMN id SET DEFAULT nextval('public."FoodWaste_dataattachmentmap_id_seq"'::regclass);
 O   ALTER TABLE public."FoodWaste_dataattachmentmap" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    239    240    240                       2604    464586    FoodWaste_existingdata id    DEFAULT     �   ALTER TABLE ONLY public."FoodWaste_existingdata" ALTER COLUMN id SET DEFAULT nextval('public."FoodWaste_existingdata_id_seq"'::regclass);
 J   ALTER TABLE public."FoodWaste_existingdata" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    242    241    242                       2604    464597 '   FoodWaste_existingdatasharingteammap id    DEFAULT     �   ALTER TABLE ONLY public."FoodWaste_existingdatasharingteammap" ALTER COLUMN id SET DEFAULT nextval('public."FoodWaste_existingdatasharingteammap_id_seq"'::regclass);
 X   ALTER TABLE public."FoodWaste_existingdatasharingteammap" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    243    244    244                       2604    448185    accounts_country id    DEFAULT     z   ALTER TABLE ONLY public.accounts_country ALTER COLUMN id SET DEFAULT nextval('public.accounts_country_id_seq'::regclass);
 B   ALTER TABLE public.accounts_country ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    212    213    213                       2604    448196    accounts_role id    DEFAULT     t   ALTER TABLE ONLY public.accounts_role ALTER COLUMN id SET DEFAULT nextval('public.accounts_role_id_seq'::regclass);
 ?   ALTER TABLE public.accounts_role ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    214    215    215                       2604    448204    accounts_sector id    DEFAULT     x   ALTER TABLE ONLY public.accounts_sector ALTER COLUMN id SET DEFAULT nextval('public.accounts_sector_id_seq'::regclass);
 A   ALTER TABLE public.accounts_sector ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    217    216    217                       2604    448212    accounts_state id    DEFAULT     v   ALTER TABLE ONLY public.accounts_state ALTER COLUMN id SET DEFAULT nextval('public.accounts_state_id_seq'::regclass);
 @   ALTER TABLE public.accounts_state ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    218    219    219                       2604    448220    accounts_userprofile id    DEFAULT     �   ALTER TABLE ONLY public.accounts_userprofile ALTER COLUMN id SET DEFAULT nextval('public.accounts_userprofile_id_seq'::regclass);
 F   ALTER TABLE public.accounts_userprofile ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    220    221    221            
           2604    448089    auth_group id    DEFAULT     n   ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    202    203    203                       2604    448099    auth_group_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    205    204    205            	           2604    448081    auth_permission id    DEFAULT     x   ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    201    200    201                       2604    448107    auth_user id    DEFAULT     l   ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);
 ;   ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    206    207    207                       2604    448117    auth_user_groups id    DEFAULT     z   ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);
 B   ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    209    208    209                       2604    448125    auth_user_user_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);
 L   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    210    211    211                       2604    448273    django_admin_log id    DEFAULT     z   ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    223    222    223                       2604    448071    django_content_type id    DEFAULT     �   ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    199    198    199                       2604    448060    django_migrations id    DEFAULT     |   ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
 C   ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    197    196    197                       2604    448316    support_informationrequest id    DEFAULT     �   ALTER TABLE ONLY public.support_informationrequest ALTER COLUMN id SET DEFAULT nextval('public.support_informationrequest_id_seq'::regclass);
 L   ALTER TABLE public.support_informationrequest ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    226    225    226                       2604    448327    support_priority id    DEFAULT     z   ALTER TABLE ONLY public.support_priority ALTER COLUMN id SET DEFAULT nextval('public.support_priority_id_seq'::regclass);
 B   ALTER TABLE public.support_priority ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    227    228    228                       2604    448338    support_support id    DEFAULT     x   ALTER TABLE ONLY public.support_support ALTER COLUMN id SET DEFAULT nextval('public.support_support_id_seq'::regclass);
 A   ALTER TABLE public.support_support ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    229    230    230                       2604    448349    support_supporttype id    DEFAULT     �   ALTER TABLE ONLY public.support_supporttype ALTER COLUMN id SET DEFAULT nextval('public.support_supporttype_id_seq'::regclass);
 E   ALTER TABLE public.support_supporttype ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    231    232    232                       2604    448390    teams_team id    DEFAULT     n   ALTER TABLE ONLY public.teams_team ALTER COLUMN id SET DEFAULT nextval('public.teams_team_id_seq'::regclass);
 <   ALTER TABLE public.teams_team ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    234    233    234                       2604    448398    teams_teammembership id    DEFAULT     �   ALTER TABLE ONLY public.teams_teammembership ALTER COLUMN id SET DEFAULT nextval('public.teams_teammembership_id_seq'::regclass);
 F   ALTER TABLE public.teams_teammembership ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    236    235    236            F          0    464503    FoodWaste_attachment 
   TABLE DATA               P   COPY public."FoodWaste_attachment" (id, name, file, uploaded_by_id) FROM stdin;
    public       postgres    false    238   �Y      H          0    464511    FoodWaste_dataattachmentmap 
   TABLE DATA               S   COPY public."FoodWaste_dataattachmentmap" (id, attachment_id, data_id) FROM stdin;
    public       postgres    false    240   Z      J          0    464583    FoodWaste_existingdata 
   TABLE DATA               �   COPY public."FoodWaste_existingdata" (id, work, email, phone, search, article_title, disclaimer_req, citation, date_accessed, comments, created_by_id) FROM stdin;
    public       postgres    false    242   3Z      L          0    464594 $   FoodWaste_existingdatasharingteammap 
   TABLE DATA               l   COPY public."FoodWaste_existingdatasharingteammap" (id, added_date, can_edit, data_id, team_id) FROM stdin;
    public       postgres    false    244   `\      -          0    448182    accounts_country 
   TABLE DATA               K   COPY public.accounts_country (id, country, abbreviation, flag) FROM stdin;
    public       postgres    false    213   �\      /          0    448193    accounts_role 
   TABLE DATA               1   COPY public.accounts_role (id, role) FROM stdin;
    public       postgres    false    215   �j      1          0    448201    accounts_sector 
   TABLE DATA               5   COPY public.accounts_sector (id, sector) FROM stdin;
    public       postgres    false    217   8k      3          0    448209    accounts_state 
   TABLE DATA               M   COPY public.accounts_state (id, state, abbreviation, country_id) FROM stdin;
    public       postgres    false    219   �k      5          0    448217    accounts_userprofile 
   TABLE DATA               �   COPY public.accounts_userprofile (id, created, last_modified, affiliation, job_title, address_line1, address_line2, city, zipcode, country_id, role_id, sector_id, state_id, user_id) FROM stdin;
    public       postgres    false    221   n      #          0    448086 
   auth_group 
   TABLE DATA               .   COPY public.auth_group (id, name) FROM stdin;
    public       postgres    false    203   �n      %          0    448096    auth_group_permissions 
   TABLE DATA               M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public       postgres    false    205   �n      !          0    448078    auth_permission 
   TABLE DATA               N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public       postgres    false    201   o      '          0    448104 	   auth_user 
   TABLE DATA               �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public       postgres    false    207   �r      )          0    448114    auth_user_groups 
   TABLE DATA               A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public       postgres    false    209   t      +          0    448122    auth_user_user_permissions 
   TABLE DATA               P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public       postgres    false    211   )t      7          0    448270    django_admin_log 
   TABLE DATA               �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public       postgres    false    223   Ft                0    448068    django_content_type 
   TABLE DATA               C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public       postgres    false    199   v                0    448057    django_migrations 
   TABLE DATA               C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public       postgres    false    197    w      8          0    448301    django_session 
   TABLE DATA               P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public       postgres    false    224   Bz      :          0    448313    support_informationrequest 
   TABLE DATA               �   COPY public.support_informationrequest (id, created_date, sent_to_email, requestor_first_name, requestor_last_name, requestor_email_address, request_subject, request_details, response, response_date) FROM stdin;
    public       postgres    false    226   �      <          0    448324    support_priority 
   TABLE DATA               �   COPY public.support_priority (id, created, modified, created_by, last_modified_by, name, the_description, weblink, ordering, user_id) FROM stdin;
    public       postgres    false    228   �      >          0    448335    support_support 
   TABLE DATA               +  COPY public.support_support (id, created, modified, created_by, last_modified_by, make_public, share_with_user_group, attachment, name, subject, length_of_reference, author, is_closed, the_description, resolution, weblink, ordering, date_resolved, priority_id, support_type_id, user_id) FROM stdin;
    public       postgres    false    230   �      @          0    448346    support_supporttype 
   TABLE DATA               �   COPY public.support_supporttype (id, created, modified, created_by, last_modified_by, name, the_description, weblink, ordering, user_id) FROM stdin;
    public       postgres    false    232    �      B          0    448387 
   teams_team 
   TABLE DATA               t   COPY public.teams_team (id, created_date, last_modified_date, name, created_by_id, last_modified_by_id) FROM stdin;
    public       postgres    false    234   �      D          0    448395    teams_teammembership 
   TABLE DATA               f   COPY public.teams_teammembership (id, added_date, is_owner, can_edit, member_id, team_id) FROM stdin;
    public       postgres    false    236   ��      m           0    0    FoodWaste_attachment_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public."FoodWaste_attachment_id_seq"', 4, true);
            public       postgres    false    237            n           0    0 "   FoodWaste_dataattachmentmap_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public."FoodWaste_dataattachmentmap_id_seq"', 3, true);
            public       postgres    false    239            o           0    0    FoodWaste_existingdata_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public."FoodWaste_existingdata_id_seq"', 3, true);
            public       postgres    false    241            p           0    0 +   FoodWaste_existingdatasharingteammap_id_seq    SEQUENCE SET     [   SELECT pg_catalog.setval('public."FoodWaste_existingdatasharingteammap_id_seq"', 3, true);
            public       postgres    false    243            q           0    0    accounts_country_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.accounts_country_id_seq', 246, true);
            public       postgres    false    212            r           0    0    accounts_role_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.accounts_role_id_seq', 5, true);
            public       postgres    false    214            s           0    0    accounts_sector_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.accounts_sector_id_seq', 5, true);
            public       postgres    false    216            t           0    0    accounts_state_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.accounts_state_id_seq', 56, true);
            public       postgres    false    218            u           0    0    accounts_userprofile_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.accounts_userprofile_id_seq', 2, true);
            public       postgres    false    220            v           0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
            public       postgres    false    202            w           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
            public       postgres    false    204            x           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 96, true);
            public       postgres    false    200            y           0    0    auth_user_groups_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);
            public       postgres    false    208            z           0    0    auth_user_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.auth_user_id_seq', 2, true);
            public       postgres    false    206            {           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);
            public       postgres    false    210            |           0    0    django_admin_log_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 14, true);
            public       postgres    false    222            }           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 24, true);
            public       postgres    false    198            ~           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 36, true);
            public       postgres    false    196                       0    0 !   support_informationrequest_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.support_informationrequest_id_seq', 1, false);
            public       postgres    false    225            �           0    0    support_priority_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.support_priority_id_seq', 1, false);
            public       postgres    false    227            �           0    0    support_support_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.support_support_id_seq', 1, false);
            public       postgres    false    229            �           0    0    support_supporttype_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.support_supporttype_id_seq', 1, false);
            public       postgres    false    231            �           0    0    teams_team_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.teams_team_id_seq', 5, true);
            public       postgres    false    233            �           0    0    teams_teammembership_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.teams_teammembership_id_seq', 6, true);
            public       postgres    false    235            x           2606    464508 .   FoodWaste_attachment FoodWaste_attachment_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public."FoodWaste_attachment"
    ADD CONSTRAINT "FoodWaste_attachment_pkey" PRIMARY KEY (id);
 \   ALTER TABLE ONLY public."FoodWaste_attachment" DROP CONSTRAINT "FoodWaste_attachment_pkey";
       public         postgres    false    238            }           2606    464516 <   FoodWaste_dataattachmentmap FoodWaste_dataattachmentmap_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public."FoodWaste_dataattachmentmap"
    ADD CONSTRAINT "FoodWaste_dataattachmentmap_pkey" PRIMARY KEY (id);
 j   ALTER TABLE ONLY public."FoodWaste_dataattachmentmap" DROP CONSTRAINT "FoodWaste_dataattachmentmap_pkey";
       public         postgres    false    240            �           2606    464591 2   FoodWaste_existingdata FoodWaste_existingdata_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public."FoodWaste_existingdata"
    ADD CONSTRAINT "FoodWaste_existingdata_pkey" PRIMARY KEY (id);
 `   ALTER TABLE ONLY public."FoodWaste_existingdata" DROP CONSTRAINT "FoodWaste_existingdata_pkey";
       public         postgres    false    242            �           2606    464599 N   FoodWaste_existingdatasharingteammap FoodWaste_existingdatasharingteammap_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."FoodWaste_existingdatasharingteammap"
    ADD CONSTRAINT "FoodWaste_existingdatasharingteammap_pkey" PRIMARY KEY (id);
 |   ALTER TABLE ONLY public."FoodWaste_existingdatasharingteammap" DROP CONSTRAINT "FoodWaste_existingdatasharingteammap_pkey";
       public         postgres    false    244            H           2606    448190 &   accounts_country accounts_country_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.accounts_country
    ADD CONSTRAINT accounts_country_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.accounts_country DROP CONSTRAINT accounts_country_pkey;
       public         postgres    false    213            J           2606    448198     accounts_role accounts_role_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.accounts_role
    ADD CONSTRAINT accounts_role_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.accounts_role DROP CONSTRAINT accounts_role_pkey;
       public         postgres    false    215            L           2606    448206 $   accounts_sector accounts_sector_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.accounts_sector
    ADD CONSTRAINT accounts_sector_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.accounts_sector DROP CONSTRAINT accounts_sector_pkey;
       public         postgres    false    217            O           2606    448214 "   accounts_state accounts_state_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.accounts_state
    ADD CONSTRAINT accounts_state_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.accounts_state DROP CONSTRAINT accounts_state_pkey;
       public         postgres    false    219            R           2606    448225 .   accounts_userprofile accounts_userprofile_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_pkey;
       public         postgres    false    221            W           2606    448227 5   accounts_userprofile accounts_userprofile_user_id_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_user_id_key UNIQUE (user_id);
 _   ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_user_id_key;
       public         postgres    false    221            -           2606    448299    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public         postgres    false    203            2           2606    448148 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public         postgres    false    205    205            5           2606    448101 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public         postgres    false    205            /           2606    448091    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public         postgres    false    203            (           2606    448134 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public         postgres    false    201    201            *           2606    448083 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public         postgres    false    201            =           2606    448119 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public         postgres    false    209            @           2606    448163 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public         postgres    false    209    209            7           2606    448109    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public         postgres    false    207            C           2606    448127 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public         postgres    false    211            F           2606    448177 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public         postgres    false    211    211            :           2606    448293     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public         postgres    false    207            Z           2606    448279 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public         postgres    false    223            #           2606    448075 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public         postgres    false    199    199            %           2606    448073 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public         postgres    false    199            !           2606    448065 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public         postgres    false    197            ^           2606    448308 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public         postgres    false    224            a           2606    448321 :   support_informationrequest support_informationrequest_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.support_informationrequest
    ADD CONSTRAINT support_informationrequest_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.support_informationrequest DROP CONSTRAINT support_informationrequest_pkey;
       public         postgres    false    226            c           2606    448332 &   support_priority support_priority_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.support_priority
    ADD CONSTRAINT support_priority_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.support_priority DROP CONSTRAINT support_priority_pkey;
       public         postgres    false    228            f           2606    448343 $   support_support support_support_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.support_support
    ADD CONSTRAINT support_support_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.support_support DROP CONSTRAINT support_support_pkey;
       public         postgres    false    230            k           2606    448354 ,   support_supporttype support_supporttype_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.support_supporttype
    ADD CONSTRAINT support_supporttype_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.support_supporttype DROP CONSTRAINT support_supporttype_pkey;
       public         postgres    false    232            r           2606    448392    teams_team teams_team_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.teams_team
    ADD CONSTRAINT teams_team_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.teams_team DROP CONSTRAINT teams_team_pkey;
       public         postgres    false    234            u           2606    448400 .   teams_teammembership teams_teammembership_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.teams_teammembership
    ADD CONSTRAINT teams_teammembership_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.teams_teammembership DROP CONSTRAINT teams_teammembership_pkey;
       public         postgres    false    236            y           1259    464534 ,   FoodWaste_attachment_uploaded_by_id_c3c14fa9    INDEX     {   CREATE INDEX "FoodWaste_attachment_uploaded_by_id_c3c14fa9" ON public."FoodWaste_attachment" USING btree (uploaded_by_id);
 B   DROP INDEX public."FoodWaste_attachment_uploaded_by_id_c3c14fa9";
       public         postgres    false    238            z           1259    464527 2   FoodWaste_dataattachmentmap_attachment_id_c9f41a70    INDEX     �   CREATE INDEX "FoodWaste_dataattachmentmap_attachment_id_c9f41a70" ON public."FoodWaste_dataattachmentmap" USING btree (attachment_id);
 H   DROP INDEX public."FoodWaste_dataattachmentmap_attachment_id_c9f41a70";
       public         postgres    false    240            {           1259    464528 ,   FoodWaste_dataattachmentmap_data_id_d28146ba    INDEX     {   CREATE INDEX "FoodWaste_dataattachmentmap_data_id_d28146ba" ON public."FoodWaste_dataattachmentmap" USING btree (data_id);
 B   DROP INDEX public."FoodWaste_dataattachmentmap_data_id_d28146ba";
       public         postgres    false    240            ~           1259    464622 -   FoodWaste_existingdata_created_by_id_11974ff1    INDEX     }   CREATE INDEX "FoodWaste_existingdata_created_by_id_11974ff1" ON public."FoodWaste_existingdata" USING btree (created_by_id);
 C   DROP INDEX public."FoodWaste_existingdata_created_by_id_11974ff1";
       public         postgres    false    242            �           1259    464620 5   FoodWaste_existingdatasharingteammap_data_id_9177d03c    INDEX     �   CREATE INDEX "FoodWaste_existingdatasharingteammap_data_id_9177d03c" ON public."FoodWaste_existingdatasharingteammap" USING btree (data_id);
 K   DROP INDEX public."FoodWaste_existingdatasharingteammap_data_id_9177d03c";
       public         postgres    false    244            �           1259    464621 5   FoodWaste_existingdatasharingteammap_team_id_1c14a1f5    INDEX     �   CREATE INDEX "FoodWaste_existingdatasharingteammap_team_id_1c14a1f5" ON public."FoodWaste_existingdatasharingteammap" USING btree (team_id);
 K   DROP INDEX public."FoodWaste_existingdatasharingteammap_team_id_1c14a1f5";
       public         postgres    false    244            M           1259    448233 "   accounts_state_country_id_39e7b64f    INDEX     c   CREATE INDEX accounts_state_country_id_39e7b64f ON public.accounts_state USING btree (country_id);
 6   DROP INDEX public.accounts_state_country_id_39e7b64f;
       public         postgres    false    219            P           1259    448259 (   accounts_userprofile_country_id_ace726da    INDEX     o   CREATE INDEX accounts_userprofile_country_id_ace726da ON public.accounts_userprofile USING btree (country_id);
 <   DROP INDEX public.accounts_userprofile_country_id_ace726da;
       public         postgres    false    221            S           1259    448260 %   accounts_userprofile_role_id_43fb6111    INDEX     i   CREATE INDEX accounts_userprofile_role_id_43fb6111 ON public.accounts_userprofile USING btree (role_id);
 9   DROP INDEX public.accounts_userprofile_role_id_43fb6111;
       public         postgres    false    221            T           1259    448261 '   accounts_userprofile_sector_id_a623e498    INDEX     m   CREATE INDEX accounts_userprofile_sector_id_a623e498 ON public.accounts_userprofile USING btree (sector_id);
 ;   DROP INDEX public.accounts_userprofile_sector_id_a623e498;
       public         postgres    false    221            U           1259    448262 &   accounts_userprofile_state_id_305ae9e2    INDEX     k   CREATE INDEX accounts_userprofile_state_id_305ae9e2 ON public.accounts_userprofile USING btree (state_id);
 :   DROP INDEX public.accounts_userprofile_state_id_305ae9e2;
       public         postgres    false    221            +           1259    448300    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public         postgres    false    203            0           1259    448149 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public         postgres    false    205            3           1259    448150 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public         postgres    false    205            &           1259    448135 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public         postgres    false    201            ;           1259    448165 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public         postgres    false    209            >           1259    448164 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public         postgres    false    209            A           1259    448179 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public         postgres    false    211            D           1259    448178 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public         postgres    false    211            8           1259    448294     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public         postgres    false    207            X           1259    448290 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public         postgres    false    223            [           1259    448291 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public         postgres    false    223            \           1259    448310 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public         postgres    false    224            _           1259    448309 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public         postgres    false    224            d           1259    448360 !   support_priority_user_id_324b092c    INDEX     a   CREATE INDEX support_priority_user_id_324b092c ON public.support_priority USING btree (user_id);
 5   DROP INDEX public.support_priority_user_id_324b092c;
       public         postgres    false    228            g           1259    448366 $   support_support_priority_id_d8bed132    INDEX     g   CREATE INDEX support_support_priority_id_d8bed132 ON public.support_support USING btree (priority_id);
 8   DROP INDEX public.support_support_priority_id_d8bed132;
       public         postgres    false    230            h           1259    448373 (   support_support_support_type_id_7bc5a55b    INDEX     o   CREATE INDEX support_support_support_type_id_7bc5a55b ON public.support_support USING btree (support_type_id);
 <   DROP INDEX public.support_support_support_type_id_7bc5a55b;
       public         postgres    false    230            i           1259    448379     support_support_user_id_92b766a7    INDEX     _   CREATE INDEX support_support_user_id_92b766a7 ON public.support_support USING btree (user_id);
 4   DROP INDEX public.support_support_user_id_92b766a7;
       public         postgres    false    230            l           1259    448372 $   support_supporttype_user_id_9ab29626    INDEX     g   CREATE INDEX support_supporttype_user_id_9ab29626 ON public.support_supporttype USING btree (user_id);
 8   DROP INDEX public.support_supporttype_user_id_9ab29626;
       public         postgres    false    232            m           1259    448413 !   teams_team_created_by_id_4d452be8    INDEX     a   CREATE INDEX teams_team_created_by_id_4d452be8 ON public.teams_team USING btree (created_by_id);
 5   DROP INDEX public.teams_team_created_by_id_4d452be8;
       public         postgres    false    234            n           1259    448414 '   teams_team_last_modified_by_id_d25361ee    INDEX     m   CREATE INDEX teams_team_last_modified_by_id_d25361ee ON public.teams_team USING btree (last_modified_by_id);
 ;   DROP INDEX public.teams_team_last_modified_by_id_d25361ee;
       public         postgres    false    234            o           1259    448411    teams_team_name_c519f9ad    INDEX     O   CREATE INDEX teams_team_name_c519f9ad ON public.teams_team USING btree (name);
 ,   DROP INDEX public.teams_team_name_c519f9ad;
       public         postgres    false    234            p           1259    448412    teams_team_name_c519f9ad_like    INDEX     h   CREATE INDEX teams_team_name_c519f9ad_like ON public.teams_team USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.teams_team_name_c519f9ad_like;
       public         postgres    false    234            s           1259    448425 '   teams_teammembership_member_id_5d9958f7    INDEX     m   CREATE INDEX teams_teammembership_member_id_5d9958f7 ON public.teams_teammembership USING btree (member_id);
 ;   DROP INDEX public.teams_teammembership_member_id_5d9958f7;
       public         postgres    false    236            v           1259    448426 %   teams_teammembership_team_id_2ee7a456    INDEX     i   CREATE INDEX teams_teammembership_team_id_2ee7a456 ON public.teams_teammembership USING btree (team_id);
 9   DROP INDEX public.teams_teammembership_team_id_2ee7a456;
       public         postgres    false    236            �           2606    464535 Q   FoodWaste_attachment FoodWaste_attachment_uploaded_by_id_c3c14fa9_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public."FoodWaste_attachment"
    ADD CONSTRAINT "FoodWaste_attachment_uploaded_by_id_c3c14fa9_fk_auth_user_id" FOREIGN KEY (uploaded_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE ONLY public."FoodWaste_attachment" DROP CONSTRAINT "FoodWaste_attachment_uploaded_by_id_c3c14fa9_fk_auth_user_id";
       public       postgres    false    2871    238    207            �           2606    464600 T   FoodWaste_dataattachmentmap FoodWaste_dataattach_attachment_id_c9f41a70_fk_FoodWaste    FK CONSTRAINT     �   ALTER TABLE ONLY public."FoodWaste_dataattachmentmap"
    ADD CONSTRAINT "FoodWaste_dataattach_attachment_id_c9f41a70_fk_FoodWaste" FOREIGN KEY (attachment_id) REFERENCES public."FoodWaste_attachment"(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."FoodWaste_dataattachmentmap" DROP CONSTRAINT "FoodWaste_dataattach_attachment_id_c9f41a70_fk_FoodWaste";
       public       postgres    false    238    240    2936            �           2606    464605 N   FoodWaste_dataattachmentmap FoodWaste_dataattach_data_id_d28146ba_fk_FoodWaste    FK CONSTRAINT     �   ALTER TABLE ONLY public."FoodWaste_dataattachmentmap"
    ADD CONSTRAINT "FoodWaste_dataattach_data_id_d28146ba_fk_FoodWaste" FOREIGN KEY (data_id) REFERENCES public."FoodWaste_existingdata"(id) DEFERRABLE INITIALLY DEFERRED;
 |   ALTER TABLE ONLY public."FoodWaste_dataattachmentmap" DROP CONSTRAINT "FoodWaste_dataattach_data_id_d28146ba_fk_FoodWaste";
       public       postgres    false    242    240    2944            �           2606    464610 W   FoodWaste_existingdatasharingteammap FoodWaste_existingda_data_id_9177d03c_fk_FoodWaste    FK CONSTRAINT     �   ALTER TABLE ONLY public."FoodWaste_existingdatasharingteammap"
    ADD CONSTRAINT "FoodWaste_existingda_data_id_9177d03c_fk_FoodWaste" FOREIGN KEY (data_id) REFERENCES public."FoodWaste_existingdata"(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."FoodWaste_existingdatasharingteammap" DROP CONSTRAINT "FoodWaste_existingda_data_id_9177d03c_fk_FoodWaste";
       public       postgres    false    242    244    2944            �           2606    464615 W   FoodWaste_existingdatasharingteammap FoodWaste_existingda_team_id_1c14a1f5_fk_teams_tea    FK CONSTRAINT     �   ALTER TABLE ONLY public."FoodWaste_existingdatasharingteammap"
    ADD CONSTRAINT "FoodWaste_existingda_team_id_1c14a1f5_fk_teams_tea" FOREIGN KEY (team_id) REFERENCES public.teams_team(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."FoodWaste_existingdatasharingteammap" DROP CONSTRAINT "FoodWaste_existingda_team_id_1c14a1f5_fk_teams_tea";
       public       postgres    false    2930    234    244            �           2606    464623 T   FoodWaste_existingdata FoodWaste_existingdata_created_by_id_11974ff1_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public."FoodWaste_existingdata"
    ADD CONSTRAINT "FoodWaste_existingdata_created_by_id_11974ff1_fk_auth_user_id" FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public."FoodWaste_existingdata" DROP CONSTRAINT "FoodWaste_existingdata_created_by_id_11974ff1_fk_auth_user_id";
       public       postgres    false    2871    207    242            �           2606    448263 H   accounts_state accounts_state_country_id_39e7b64f_fk_accounts_country_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_state
    ADD CONSTRAINT accounts_state_country_id_39e7b64f_fk_accounts_country_id FOREIGN KEY (country_id) REFERENCES public.accounts_country(id) DEFERRABLE INITIALLY DEFERRED;
 r   ALTER TABLE ONLY public.accounts_state DROP CONSTRAINT accounts_state_country_id_39e7b64f_fk_accounts_country_id;
       public       postgres    false    219    213    2888            �           2606    448234 T   accounts_userprofile accounts_userprofile_country_id_ace726da_fk_accounts_country_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_country_id_ace726da_fk_accounts_country_id FOREIGN KEY (country_id) REFERENCES public.accounts_country(id) DEFERRABLE INITIALLY DEFERRED;
 ~   ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_country_id_ace726da_fk_accounts_country_id;
       public       postgres    false    213    221    2888            �           2606    448239 N   accounts_userprofile accounts_userprofile_role_id_43fb6111_fk_accounts_role_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_role_id_43fb6111_fk_accounts_role_id FOREIGN KEY (role_id) REFERENCES public.accounts_role(id) DEFERRABLE INITIALLY DEFERRED;
 x   ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_role_id_43fb6111_fk_accounts_role_id;
       public       postgres    false    215    221    2890            �           2606    448244 R   accounts_userprofile accounts_userprofile_sector_id_a623e498_fk_accounts_sector_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_sector_id_a623e498_fk_accounts_sector_id FOREIGN KEY (sector_id) REFERENCES public.accounts_sector(id) DEFERRABLE INITIALLY DEFERRED;
 |   ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_sector_id_a623e498_fk_accounts_sector_id;
       public       postgres    false    221    217    2892            �           2606    448249 P   accounts_userprofile accounts_userprofile_state_id_305ae9e2_fk_accounts_state_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_state_id_305ae9e2_fk_accounts_state_id FOREIGN KEY (state_id) REFERENCES public.accounts_state(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_state_id_305ae9e2_fk_accounts_state_id;
       public       postgres    false    219    2895    221            �           2606    448254 J   accounts_userprofile accounts_userprofile_user_id_92240672_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_user_id_92240672_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 t   ALTER TABLE ONLY public.accounts_userprofile DROP CONSTRAINT accounts_userprofile_user_id_92240672_fk_auth_user_id;
       public       postgres    false    207    2871    221            �           2606    448142 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public       postgres    false    2858    205    201            �           2606    448137 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public       postgres    false    2863    205    203            �           2606    448128 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public       postgres    false    2853    199    201            �           2606    448157 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public       postgres    false    209    2863    203            �           2606    448152 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public       postgres    false    2871    207    209            �           2606    448171 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public       postgres    false    2858    211    201            �           2606    448166 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public       postgres    false    211    2871    207            �           2606    448280 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public       postgres    false    223    2853    199            �           2606    448285 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public       postgres    false    223    207    2871            �           2606    448355 B   support_priority support_priority_user_id_324b092c_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.support_priority
    ADD CONSTRAINT support_priority_user_id_324b092c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.support_priority DROP CONSTRAINT support_priority_user_id_324b092c_fk_auth_user_id;
       public       postgres    false    228    207    2871            �           2606    448361 K   support_support support_support_priority_id_d8bed132_fk_support_priority_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.support_support
    ADD CONSTRAINT support_support_priority_id_d8bed132_fk_support_priority_id FOREIGN KEY (priority_id) REFERENCES public.support_priority(id) DEFERRABLE INITIALLY DEFERRED;
 u   ALTER TABLE ONLY public.support_support DROP CONSTRAINT support_support_priority_id_d8bed132_fk_support_priority_id;
       public       postgres    false    228    230    2915            �           2606    448374 E   support_support support_support_support_type_id_7bc5a55b_fk_support_s    FK CONSTRAINT     �   ALTER TABLE ONLY public.support_support
    ADD CONSTRAINT support_support_support_type_id_7bc5a55b_fk_support_s FOREIGN KEY (support_type_id) REFERENCES public.support_supporttype(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.support_support DROP CONSTRAINT support_support_support_type_id_7bc5a55b_fk_support_s;
       public       postgres    false    232    2923    230            �           2606    448380 @   support_support support_support_user_id_92b766a7_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.support_support
    ADD CONSTRAINT support_support_user_id_92b766a7_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 j   ALTER TABLE ONLY public.support_support DROP CONSTRAINT support_support_user_id_92b766a7_fk_auth_user_id;
       public       postgres    false    207    2871    230            �           2606    448367 H   support_supporttype support_supporttype_user_id_9ab29626_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.support_supporttype
    ADD CONSTRAINT support_supporttype_user_id_9ab29626_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 r   ALTER TABLE ONLY public.support_supporttype DROP CONSTRAINT support_supporttype_user_id_9ab29626_fk_auth_user_id;
       public       postgres    false    2871    207    232            �           2606    448401 <   teams_team teams_team_created_by_id_4d452be8_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams_team
    ADD CONSTRAINT teams_team_created_by_id_4d452be8_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 f   ALTER TABLE ONLY public.teams_team DROP CONSTRAINT teams_team_created_by_id_4d452be8_fk_auth_user_id;
       public       postgres    false    2871    207    234            �           2606    448406 B   teams_team teams_team_last_modified_by_id_d25361ee_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams_team
    ADD CONSTRAINT teams_team_last_modified_by_id_d25361ee_fk_auth_user_id FOREIGN KEY (last_modified_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.teams_team DROP CONSTRAINT teams_team_last_modified_by_id_d25361ee_fk_auth_user_id;
       public       postgres    false    234    207    2871            �           2606    448415 L   teams_teammembership teams_teammembership_member_id_5d9958f7_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams_teammembership
    ADD CONSTRAINT teams_teammembership_member_id_5d9958f7_fk_auth_user_id FOREIGN KEY (member_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 v   ALTER TABLE ONLY public.teams_teammembership DROP CONSTRAINT teams_teammembership_member_id_5d9958f7_fk_auth_user_id;
       public       postgres    false    236    207    2871            �           2606    448420 K   teams_teammembership teams_teammembership_team_id_2ee7a456_fk_teams_team_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams_teammembership
    ADD CONSTRAINT teams_teammembership_team_id_2ee7a456_fk_teams_team_id FOREIGN KEY (team_id) REFERENCES public.teams_team(id) DEFERRABLE INITIALLY DEFERRED;
 u   ALTER TABLE ONLY public.teams_teammembership DROP CONSTRAINT teams_teammembership_team_id_2ee7a456_fk_teams_team_id;
       public       postgres    false    2930    236    234            F   <   x�3�62040007430r4�+HI�L��/�K74�O,)IL��M�+)�ǦА+F��� �Jo      H      x�3�4�4����� 	_      J     x��R�n�0=;_��Զd7u�Ӳ�;X�t�eY���dHr��G'�Р[O=�(�G�ɷ�M~w��̿>>m����s2��v�V�����:�O>,y��7uZ]/y��9?D�L�|��]��(�VA�q�T��y@����m�L0Z�����.��b>��I��b�*��Q��Ð��<��uŠC&]�/����m���,
��b�*����`�1V�V�y6�6�L�r�K�Ū(We�5ce���d݄腌�a�Nb4�Bj��Rسd�T��c��Ť��}��i��Ŗ���G�Ts4ڥH�t|��؎hf,5�� �r"��ƀ�
h�:
�4(�ג����k����S^� �\)|�v��0˟�5?�e�>����4�BКQ+����h���&ޞ�4x�ԟ,�$�n�k�,��60��2�s�0yg��i֝���^�w'�?k�t�X��H���ȗ/9�g�����!R�����E�}�䂦��A�|��v�,�yU��./\���+^�v~h���-���jn      L   C   x�Uʱ�0�ڞ�b��(�%c���D��cb��y -5��,�,{V��bS;�.f�[�k���]2^      -     x�mZMs۸<O~�n�[�����ђe��G��켤��`
I( )E���A��d�]�*�I3==ӄ���5٪�����L�]�󚪤�G�~��ɇ&ݤ*�4
�����؏�,£�� �m � ���;`s���p=Vyc�2��ă�ץ�|c��V 65�@bS\�,���z�_�L�aj� �R���j��_��^c��<�$�j`=��rQ�z"�I@_ӍK4nȁy0��tù@d�(�*��/��1\G���t*��x�*`:�k�(>k)��i!��B��{4T[����"OQ��u�#�29�b �$U]li(��l6���Vm,�4�(@�i�S�* �
�) ���*��X t@�<5ņ���f��o�Q\�;��2ρ��^����p[�R��G!�M�Ԧ��u�@�&bj0��ܽvg�؃���Fܠ��-���A�(��� ��K.q��!�e��&���o��B��)M�m<��:�k�\k�?[w��+v�B�]�kӸ�I,T����xI�HC�&��w(j-
��B&*�CTw��4�aku=��Ji(d 
2���He��^h*(�n�=D;ks���!�� �/F"Gq�Q�
��n�h��4яC��� �2��"�SA�]�z�I#�4�q���I�(51�D$��v�F[�����2T`���&�҄�Ǭ����!e�.�;4�Ņc#�E��Eڈ��m��s�Q�y���vG#qG�@lj�9	zŁ^m$�f�A@�"E���2`�3h$Fu������V7nufc���#����/�HD0� '��~�e*`� C,zq�������8TYٰ%V�9X��NA�8����8�U*�O���LF�QġQt���ދ�H0-L� �goᗐΘ;��nu�)��[��M�y��n�Ld��Э��M���5����>4�"����n���o+6����
m��XPKju�4NN��Ƃ:��ۡq�Y%=�OY��-B�v�4�^)�AIN*�kE1S$a���h�t@�E�t�Y�O㢴~F�F�C#�h\n��{��3:���ݩt��X��3�>P��_t'r�rԻ�]��w߉������tg�݉<��<�Z���"p'����kӝSy��N�5��@�`��;�D�Zt�׽��6=�@H��gh�]��[�~�-�Z��J��OA�'Bٓ�����4�Mc�W4��%!ҙ�t���p���
ĆM�l�(����o��D��hi"B�����4qZ#��$��ߩ!o����]��;�D�`t�ߣ	JN����UK�P߃2�YJ�,��r��W�G<	 �rX�MD�&�x�+ע�ZI�Z�&��F��&b|J��4@x�S!�I��A���"����b;t����b=����U��u��l]����r���>�����$�)~н(�m(�A��CՉ�EԷ!�=ĺ������WWT�}� br\{�u� b6j���c����K�����U��������Uk�:�^���ި}#�cB�6l����9�SzE`RF��T)�]�n���O��M��=���]�2 d�e<�y۳���G�<��~�x?0���m�3�L�YF4i��j����T���<XΩ�O�ŋv��ij��0i�T���0�CS������i��>��ex*6��l�{y�oh����tZQt4E�c�s:=��t�����͔����3��LH���_���{���#�i�#��̄�M#�4)l��4e�r����LTX��p���
m�F5n���}[�I�	�JO|Gw`�+u^��w&2�rf�ig��V����`|ʌ���U?4�T��	�I����\���\6c����7~�	���u�^��Ub��߸1R������Q�*b�ù�|ƙ�ٝ����2fܮG����E3#�-0s�1,Ș0���=BO2��ٹ��4��8��s劭J��v1�@�\�h�-1"�4ͅ\f,�-��
�O�չ`UƬje`�"�'���}�e��X���g;�?L��S��`Bmb:��Ɲ�h��4V%~>�wBI_YIam�6���!:N��v�f��/|@3����_�梹e��`r�A����IB,3K�[�*0Z��梤3.ix�9�j�$�%cu���۳�-�D
��X��k�(��](� ��.�g������]p�$���`B�L�o]�Ji!�;g��g]h?Uv.�s�:,�/������(�s�1��]�cc�� 
�	�9����M�zX�p�p�i���TR�YB�rV<�مI����q�9���~=B]� �y[��ɹj`dֽ���ɀ䯌lyd0,s�Q,W?E@d#�l��➣:�B(m�Jg���>�X&<�R�±�R��u^v�pW��g��@^�~�J���9����Z��s���.��vNpvϜ��]�}�>�<�/E6���0�ː�-���Y�aj�%�I�s��j�[����*h)�w��k�4e��C����j�[�U�����=�	|�I���R��U�v	TZ�1��R��K�_��"��/��Ӹ���'�w�{��}�Y�+��
.��*
�gV�������G�tD �<��܁�])���إ܎S��h(�q��m�^�p���)87��75eY�6l����HԎ�n�U��~���,>0�:/�E)g\���4(|����Z�J�s%���^Lk��w��(8�/ba^\r8h�"���e��RAWrK+���� ����YX����߯5���'�ژzE�V�zS�y��)X�)(8��+��C���eH�>�[]w��Eq	r䣮3�1�V�Ks	Fye`���"�zR���+�RL;�7��EP�&̲�ԇ}+�i
���ڶ?����O(� �y���J�`�'G����->�o"�g>0�W8�0�Ψ�Wbs4��}I���� 5{�7 } 3�4f*ߡxD��K���ʻؕ�ފ�� 2�!� 	"W8� !�F�#���cM��S�7ʂ���WG��ex%ƅ�a�WG�#���3EX��є�0��H(O�eRs�;��wk�ͨ��LX�2G��d���_\��0k!��o��7�]{-6^^6�*?��b=��Oٿ����Ey�E��[��,/����d��훾����2e؀�6���U��j�X��N��b-XS2k���Q%|��1�����U�,<�=�[��P�2grR��>�Z��d�S{�?�)zZ�)1,�ǅ4R��]�m-�������a3�#����=�Yĵ��u@�;\��YhC�� �̜��:Ό�a����L����B576����n����ѳP��U��7 Zdn]�sU�'��=R�"�Gv��U���,ʫ���~>G�+�Y0�b��v���ReE/b�9T�R֧Q#S��E�p	n�^���h��^DD������F/���"<���t����>�����\�����D/�5�5��QijI者��|�͑�����x���g�I��B!4+��W���b�'�>���p��M������f�HEGM߄����Ӈ��      /   _   x�3��M�KLO�M�+�2�IM���LN�Q(�OK-.���r4\��3�RS����3�j3�K4��9���L8�KJS@��r��d�q��qqq 'F      1   I   x�3���K)-.)��2�tLNLI��L�2�t�/K-��M�+�2�����-(�O�,��s��2��/�H-����� ��      3   z  x�M��n�0��O�'X�?~.Q�BJPخ��.�H��N�e�~'������<��3���ī�O�``aoB;���$$��M)�{}K��$F"*�f�Vɢg$�2V\�mO�D��E���Ar��KY�Oa%�?{2�R�ƪ��̛GE����.����ʪ��+�}���W�Y��~�5�T
�A��"J�t�q����6�!��H�E	j3͙L��O
��Sl��́�����ݱya4Ǔi���<���PZ"���b{��� c9A@�9Q���M����TQ���ȸ� "DCt��Xhs����2�LzjZK��Ȍn:qO?�!��V��@>��4�����	|zkQ��R�O�����Gi��#d�0�Ua�g��{CΓ
#��6��k�	�����`)n]�9�(�`[*��p��[E���n�5�ak��hly)�9vRkw�>D��;j4ƾ4饮�`σ�|L�]ЁE�p0:��(�QvF8)qd#���_ڐ�/�c<7��3;��$mM�4�)N�6��w��p4g}m��� �8K�x_�g�&�\a�S�ˍ�>�wSS�y�1��Z҃�;���C�V$�!V���z�p�DZ�ъvK<�6r�)1v��������=����W�)����F��#([      5   �   x�}ν
�0����*r-9''5�&���".]J	��dh���K�"·=��"���@S�׈�l@W�[W�"���em=�_���C��f|�2��S�9U�����%��3�q�GIw���v�I���+ K@`�V��V���R�|��G�Z�˿��J��*9�      #      x������ � �      %      x������ � �      !   �  x���]�� ��a^A��7�s�љ�����$v1i����o1�$9D-���j�\���z��؞��l ~��ϫ"�[T�Eݕ��[TԟI�%�}D����DR�O9PD?P��C�ߍQx1�N᭫:�Y���d�A_|��j�� �5QD@@�ڨČF��	��e�1�2�3�x��>�U�j���i�\=�K�"�#������'�-�Q"囏(4�A/c�zz���c4������R��'Ȇ��r*�R�f��������ʹ�f)3�d�Ӭ'�h�?ʆمP�M�o��#HD0�!�ײ�ڈ����I��K���c�M�;�c�Or��#m��2�E��eWd��y��s|_��y.��C&��T�c��b;��\�[��w>����	�DG��� �Ek���?�^o�"�:���kRIIQG��Tg�F$Ӵ��O�B4%:�>_+�F��.ۂrӉy�q�?��5E�%�a �Xt΢�cZ���v�(�Ȟ���ۄf>�78���8�\N�誫�_�ww�
dϜ ��sO`P2�1� )�J�qH�>�N6Lƒ�yd	2��L �G�%��i���ٹ��k`�!�Dq:\�HBr��	�VE�Պ�x�"ptê�?>�������¥9�{r��«2�F��_��Z�y��ڍ�h��� ��y�R��ְb�,��3'�Fm�2�wu�X��QC.W㶑O���0K!G׸��G�����|f}^3�_�kҹ�yE�ݯ]EFc���aw�-ѸQhC1y��;���
��4��Ư�g�I��}2�)�qc6��#;B8�MQ����&(M΂hJ����M����N4��>j��8��tV"�˼ʡ���*���U��}�����W�'V���6�O���xl���+K��x
9��h��m��ܹM�������6X,W�8����_�X� i�a���e�+��틔�?1���      '     x�m�Ko�@��ïp��a�{�IS���A�6Ӥ�=���__�EӦ'wq�99ɇ�o�?O�S�5R����b��K�
o48���K\o�	��o��{�6>�'�,��wB-6�80����!E0ږ�1N
��gyB��vO�k��m��a��X��YH��s�K��Yu���~*���p�8x�;��J�_ӹ��E1tV����߬�"sѢ�8:xg_��g ��W閄ח�B*nQ'=D4��=�40[���5w�����|�@bT      )      x������ � �      +      x������ � �      7   �  x����j�@����j�^vf��.�>A|������Y
�BSB޽+)T��؁�NH��3�2�`���(r.��C+��%e��7y��>�1�B�M<�UR�^��J��4W��in��p(����~.ʵo�BU����U��ڥ����Pܼ�܌lq�6�b�����p9����0t����n�V]�L.z,oCM�s�;)I������*�][���O�.&�7�4Hu:��n�P|͋��u�?<����bJ��	�#ɬ����\�T���F�l3g'5SV)%>�������;��6��w9�W�n}Y��.}���>̜ɑe�hQ�朳yw� s�pR0 юWy�/כ����<���<���K��ᬧ�䷱.�p���Ё1���	��y���~g���S�+���b���N�{w: ~��b��T�           x�uP�R�0<[��iZ���p��x�-WRf���И\,kW�]y�]�c2uK�	��l�\�3h+��v+0*I>�ҹw:��b.�KD���#����X�Mp�C����M��o�F]^��"�wB_��1$w�3-�|�2��2I�E�����Ҳ�e�	��r�d�u^�u���e��|��s��j�L���l��Ǌ)7�ԣL=�2W��1C��
gͰbY�о�W
�������y4۪�7���<h{{�/�6Ł           x���mn�@��S�E�����J�Y¦h!��Q��_	��6�"	�����<�����M�%B����P%R�{�� ���Rkz�$�0��Dh"a�LB����?p�cA�Q����O��C� �G�.�K֌ ��p�2�@� �I�N¡.O�Ds�t�`1��xd���u|+f�p�g(r�F��2���8�'��
G���2����4�Y�S��E�����S��}�18�	b)<���7E[�]7j��*NG�j�e�$`a�5t�(�PVw1N�T��"�)�c��~� ���`�C�U�����S���Ka/��B��￡l�'����>���9KyUy}l���E����Eׅ���`/��gwݹc�D}f����C(R���@�Q�6�cE��܂?4lQ�6��Z�4��R$]q����F�='!醦�m? LiK����2V�y�j�7H*=���x\�B�G����j'' %}�2%K�/U�#��O�r�u�̄� Rż �6��y�3�3b�ОW��pM�<��0A�gУ����3�n�	��?2��� jB�-Bmȶ�H\�,\"#Ly���A[��}�%wx���ۂ���`$d ��ySM�G�r̖s(��
e͗�gϚ�zd$Se��w�ܢ�MR D�J�4Ҝnn� ϛ��Β��bS2�S�"ܬ�>�H߇����T1n|�)3��X��	����ɬ���d�dS+�S3B�'#B��1��fį����?��q�      8   W  x���Io�6 �s�+�"p_�T'��1lر=�E�P�6j㯯��i��{�6@���Վf$<�ڮ+�̢sY�NS��\���;O��o���Jϯ���z���\�^���{y)Rr�����r�=��ۆ�J��oO���o�*x}���|ʧ�}��]��K�2�t�W�OE�_�,����2��i	^O���w�N>-���2�z��#[��c����j����,�P��	/ե<�jtv����2_�5~>�:-��LnO���:�}W�뉫��}B �/~�3�>>�D����㥋3Z�t]J6�3cI��Ad���Î���Xz@�fWJ�tA묥��,y,�FGNM���a�ۑ�;������X~�&��Q��sS��c10W���q(&�����[��m�1N�f����� �8	z��De��I�����o;��a�v�17��N0��d�:�+I;R�І�l h���aG?��S��1`��X��:L�0OD��Ԇt�Z��n����N�I֧�@�v����]j��-hR@�^�7�N����r�"O ���p�]�V�k����%ke�a���>a� q��U	P,��s�mD��Z׹�VΡ�ͱ�~�!R �c�F'Xc�:��(�0��6Se��9Qy��B��*ŃR��(Z�.��P�Sܚ*-�̓5~{1R1}�T�e������E똱��u_�u��x!g���"��B�k�ڙ�2�OE�d���k��!�_�������3/�#�1F��6/H�m�/[ɵ(�f
qP��_�B���Ò�{-FMHK�ضq2,5}�Xp	8�ڿ���* �{E	-&�$!��8d�Ȓ��
���^)^�\"�Je$�����!����}z��_��K�(^/�{Ə����k�&:�ED&���$��6,�_��#rL�F7�qY`���(�0�6LemAܐ������p
3L�b�ȹ��Wj�np��S4�dJSw����@���]ZMf�h�,��(�����X�)��:�?�O���Q��\��0QpL�R/J6��q��,���a����RD�"0Y�p$�z'd3d��a\�rQ�k���m}D
| =&�2}��NB^q1(��0��fsɀ�fh��n��[���5U ���G�TWV�h�R�
�[������a�ۉ͎"�5U�Uo��'��2e�F�M�k"3�a�FG����{/�{������,w%�
J��QH*���̪���i'��?������f�;:�SF�%�-���C�b;i�1�a�O��͉�72�7(�%�5r"��``�$	�&�-	k�%�a�a}|��(�=f��nnn��6��      :      x������ � �      <      x������ � �      >      x������ � �      @      x������ � �      B   �   x���;�0����@#��o�Tl$F�YP%��c�@H��Cj�X�KqX�TM�#�C�ݰ�X�>���g)��sVG��)^t��yi���i:������k�	pyv��"V�����Oc���c���-l      D   e   x�e̱	�0D�ښ�X�ɲ5K�L���	���PT0��Q!)3M����ʽ����������n��v^�4O����iq���1b�����9�LD�G     