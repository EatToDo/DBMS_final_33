PGDMP                      |            Final Project    17rc1    17rc1     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    17787    Final Project    DATABASE     �   CREATE DATABASE "Final Project" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Chinese (Traditional)_Taiwan.950';
    DROP DATABASE "Final Project";
                     postgres    false            O           1247    17798    gender_domain    DOMAIN     �   CREATE DOMAIN public.gender_domain AS character varying(10)
	CONSTRAINT gender_domain_check CHECK (((VALUE)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])));
 "   DROP DOMAIN public.gender_domain;
       public               postgres    false            S           1247    17801    role_domain    DOMAIN     �   CREATE DOMAIN public.role_domain AS character varying(10)
	CONSTRAINT role_domain_check CHECK (((VALUE)::text = ANY ((ARRAY['User'::character varying, 'Admin'::character varying])::text[])));
     DROP DOMAIN public.role_domain;
       public               postgres    false            �            1259    17812    artists    TABLE     �   CREATE TABLE public.artists (
    artist_id bigint NOT NULL,
    name character varying(20) NOT NULL,
    gender public.gender_domain,
    bdate date
);
    DROP TABLE public.artists;
       public         heap r       postgres    false    847            �            1259    17803    users    TABLE     �   CREATE TABLE public.users (
    user_id bigint NOT NULL,
    username character varying(20) NOT NULL,
    password character varying(15) NOT NULL,
    gender public.gender_domain NOT NULL,
    bdate date,
    role public.role_domain NOT NULL
);
    DROP TABLE public.users;
       public         heap r       postgres    false    847    851            �          0    17812    artists 
   TABLE DATA           A   COPY public.artists (artist_id, name, gender, bdate) FROM stdin;
    public               postgres    false    218   �       �          0    17803    users 
   TABLE DATA           Q   COPY public.users (user_id, username, password, gender, bdate, role) FROM stdin;
    public               postgres    false    217   �       1           2606    17818    artists artists_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.artists
    ADD CONSTRAINT artists_pkey PRIMARY KEY (artist_id);
 >   ALTER TABLE ONLY public.artists DROP CONSTRAINT artists_pkey;
       public                 postgres    false    218            -           2606    17809    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    217            /           2606    17811    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    217            �     x�U�]OZY�����˙�18�9W��vj?g2�L�IoHk*�TMS'i�D8�(*P)��PQL淜�uտ0�֡M�Y����z߳�B|��?�G�=�߄��5m�ɣ���6
Ur�G��Q�!S��z
���?g�G��<�5uwh������������a`������(N����}��@�������J���������;�酷S/����c�!��-�v�X�[zx��Kf&�'�u���x�����9"�<�/.��zc�[.����kWub^͋]A�r���k��(�H!�U��b�S���n6��
"��b���^��\G�! �X+�d������4���ZF�ΐ�Or�*B��E�=��O��B
�f����'*b��0�U	c�Ua4��(,���r�d�C\P��ߑ�=Q���8�-�[�m��%4�X.��8T̼�B�z���
�l!�	�o��Ϣ)T��X�P�� >]u��������$N��r*�=�c�M�����=*�%W!��1˟��"+�c�h~s�Pn�rXf#�4��,QJ�.�B�M��R�19-D%��=�����n r���U�!��g�_�"���ZOB�<D��ޙF�<^"�8<�a_O�נ��}��7�ᇱN� i��<���»)z6���K����C4�A
��0X��ζX�`�=��50�� ���y�J�nX�c���2<6���D��
x!��/��L7nib�#Z�D�[H������i!Z��	,��^��2���>e>'��,�~��v�"��p�o�J��XH�0�uy��G�~��v�:ǧY�'�`)D��_�3<H�w�� 
�T�+�,[}`//
��j�Cl���,�jn"�V�2C�{aZ��]t�決���y�-,�Io���l?M�v��"��=5�B��d����՝�� ��iB�~�%�C����X����^@�RܼC�����/���K�f?+�mn�ע��\�ۨ�!����?��i����	d���>�+�bV���FD*k�@g���]&8ٜD3tе�BD�դ�.��_��fp�7��"|5n��6�17�aB�a�T	ϔ�6w'g~u@�Y���;�2X.]0yh#6�Z>�q�R���J�wj��f3�n�N918��N��-��- ���D,f0^�B�-��d3א��P&�Aߊu�o�����'yM��o��gڳk�[��ɖ�`�"�P���hS� e�T��"e�6??B��������������ɉ�����Џ      �   <  x�M��N�0�볷0`����Zz�	.Hb����dŮ�n���š����Ο��ʕ�;oT���JM<�E�#�ep���6�0$�a+��G�e�@��R�ފ�Q~�!씮�Y9%,�w�����o�bLf�Fǁ��r��2�3�~�NO�!�"x�rİU����(\N����*:�y�m8�*�:wU%��O��.6��Q!]o8+�^Èz�e�z�lO~H���}���Sk%}5�ުZ�.ʳ-�c�pU!��Ff���x8L�&^�p߄����E�	����&��^,��ym��}��?~���,!�     