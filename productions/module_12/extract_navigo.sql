select * from ports.port_points pp where toponyme  like 'Gravelines'
select * from ports.port_points pp where toponyme  like 'Dunkerque' -- A0204180

select * from ports.port_points pp where toponyme  like 'Douvres'
A0382747

select distinct pointcall_action, count(*) as c from navigoviz.pointcall
group by pointcall_action
order by c

/*
Unloading	71
Loading	142
In-Out	311
Transit	878
Sailing around	2387
In-out	3574
In	50795
Out	50923
*/

select * from ports.port_points pp where toponyme  like 'Noirmoutier'

select * from ports.port_points pp where toponyme  like 'Dunkerque'
select * from ports.port_points pp where toponyme  like 'Graveline'

select distinct ship_flag_standardized_fr  from navigoviz.pointcall p 
select distinct ship_flag_standardized_fr  from navigoviz.raw_flows rf 

select distinct departure_uhgs_id  from navigoviz.raw_flows rf 


select  distinct destination, destination_uhgs_id , destination_state_1789_fr  
from navigoviz.raw_flows p where destination like '%Lisbonne%'

-- Lisbonne [mais: Angleterre]	Grande-Bretagne
select  distinct destination, destination_state_1789_fr  from navigoviz.raw_flows p where destination like '%ergen%'
select  distinct destination, destination_state_1789_fr  from navigoviz.raw_flows p where destination like '%(destination simulée pour)%'

Angleterre (destination simulée pour)

select * from navigoviz.pointcall p 
where p.pointcall ilike '%destination simulée%'


select  distinct destination, destination_uhgs_id , destination_state_1789_fr  
from navigoviz.raw_flows p where destination like '%Bergen%'


select * from navigoviz.pointcall p 
where p.pointcall ilike '%Bergen%'

select * from navigoviz.pointcall p where ship_id = '0000159N'
order by  p.pointcall_rankfull 


select count(*) from navigoviz.pointcall where state_1789_fr = 'Grande-Bretagne' and pointcall_function= 'T'

select count(*) from navigoviz.raw_flows rf where extract(year from outdate_fixed) = 1789
and destination_state_1789_fr = 'Grande-Bretagne' 

select * from ports.port_points pp where toponyme ilike '%Angleterre%'


select * from navigoviz.pointcall where pointcall = 'Hull' order by source_doc_id 
-- A0389327


select source_doc_id, rf.commodity_purpose , rf.commodity_purpose2 , rf.commodity_purpose3 , rf.all_cargos 
from navigoviz.raw_flows rf  
where destination = 'Hull' and departure = 'Dunkerque'
and extract(year from outdate_fixed) = 1789
order by source_doc_id 


00335599
00335600
00335601
00335602
00335603


select * from   navigocheck.check_cargo where link_to_pointcall = '00335599'
create or replace view navigocheck.pointcall_cargo2 as (
            select r.link_to_pointcall, 
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'commodity_purpose' as commodity_purpose,
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'commodity_id' as commodity_id,
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'quantity' as quantity,
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'quantity_u' as quantity_u,
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'commodity_standardized_en' as commodity_standardized,
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'commodity_standardized_fr' as commodity_standardized_fr,
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'commodity_permanent_coding' as commodity_permanent_coding,
            ((jsonb_agg(to_jsonb(r.*)))::json->>0)::json->>'cargo_item_action' as cargo_item_action,
            jsonb_agg(to_jsonb(r.*) ) as all_cargos
            from 
                (
                select c.link_to_pointcall as  link_to_pointcall, c.commodity_purpose, c.commodity_id, c.cargo_item_quantity as quantity, c.cargo_item_quantity_u as quantity_u,
                 c.dictionary_commodities__permanent_coding as commodity_permanent_coding, c.cargo_item_action
                 -- ,
                -- labels.fr as commodity_standardized_fr,  labels.en as commodity_standardized_en  
                from navigocheck.check_cargo c left join ports.labels_lang_csv labels
                on label_type= 'commodity' and key_id = c.commodity_id
                ) as r
            group by r.link_to_pointcall)
            
            
            select count(*) from navigocheck.pointcall_cargo2
            -- 31363
            
            select * from navigocheck.pointcall_cargo2 where link_to_pointcall = '00335599'
            
            select count(*) from navigocheck.pointcall_cargo
			-- 31168
            
select all_cargos  from navigoviz.pointcall p 

----------------------
-- Pour le module 12
/*Module 12 : Où vont les navires qui ne vont pas en GB ni en France en partant de Dunkerque en 1789
-> part qui repart vers l'Europe (20 milions de marchandises ?)
-> peut etre que pas et ca valide l'hypothèse que Dunkerque est fraudeur / France
Toflit (valeur et quantité ) qui rentre dans les imports du bureau de Ferme de Dunkerque  : ok
Toflit : sorties officielles vers les colonies et les autres parties de la France connues

Navigo : #navires et somme des tonneaux en 1789 + détails des produits (Lège / others)
*/
----------------------

select distinct partner_balance_supp_1789 from navigoviz.pointcall p 
/*
 * 
NULL
Sénégal et Guinée
colonies françaises
Etranger
France
 */

select * from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180' and rf.destination_state_1789_fr not in ('Grande-Bretagne', 'France') and rf.destination_partner_balance_supp_1789 not in ('Sénégal et Guinée','colonies françaises', 'France')
-- 1053 / 4689

-- C0000009 cote d'Angola


--- 
-- Extraction de tout dégroupé pour mettre dans le git et faire les graphiques et group by dans python
---

select * , jsonb_array_length(rf.all_cargos) as nb_products from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180' and extract(year from rf.outdate_fixed) = 1789
and rf.destination_partner_balance_supp_1789  in ('Etranger')  and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_uhgs_id != 'C0000009'
-- 583 / 2539

select rf.travel_id, rf.source_doc_id, rf.destination_uhgs_id, rf.destination_fr, rf.destination_substate_1789_fr , rf.destination_state_1789_fr, 
rf.tonnage , rf.outdate_fixed , rf.commodity_purpose, rf.commodity_purpose2 , rf.commodity_purpose3, rf.commodity_purpose3 , rf.commodity_purpose4 , 
rf.all_cargos , jsonb_array_length(rf.all_cargos) as nb_products,
rf.commodity_standardized_fr , rf.commodity_standardized2_fr , rf.commodity_standardized3_fr , rf.commodity_standardized4_fr 
from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180' and extract(year from rf.outdate_fixed) = 1789
and rf.destination_partner_balance_supp_1789  in ('Etranger')  and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_uhgs_id != 'C0000009'

-- Récupérer seulement les produits, standardisés ou pas, et des infos sur les destinations
select rf.travel_id, rf.source_doc_id, rf.destination_uhgs_id, rf.destination_fr, rf.destination_substate_1789_fr , rf.destination_state_1789_fr, 
rf.tonnage , rf.outdate_fixed , rf.commodity_purpose, rf.commodity_purpose2 , rf.commodity_purpose3, rf.commodity_purpose3 , rf.commodity_purpose4 , 
rf.all_cargos , jsonb_array_length(rf.all_cargos),
rf.commodity_standardized_fr , rf.commodity_standardized2_fr , rf.commodity_standardized3_fr , rf.commodity_standardized4_fr 
from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180' and extract(year from rf.outdate_fixed) = 1789
and rf.destination_partner_balance_supp_1789  in ('Etranger')  and rf.destination_state_1789_fr not in ('Grande-Bretagne')
-- [{"quantity": null, "quantity_u": null, "commodity_id": "00000147", "cargo_item_action": "Out", "commodity_purpose": "Sucre", "link_to_pointcall": "00339495", "commodity_standardized_en": "Sugar", "commodity_standardized_fr": "Sucre", "commodity_permanent_coding": "ID-GBAxxx-JF-DCAxxx-FBxx"}]

--- 
-- Pour faire la carto vite fait mal fait par port dans QGIS
--- 
-- array_agg(rf.commodity_purpose) as cargo1, array_agg(rf.commodity_purpose2) as cargo2, 
select destination_uhgs_id, count(*) , sum(tonnage::int), 
array_agg(rf.all_cargos) as cargo_all, sum(jsonb_array_length(rf.all_cargos)) as nb_total_products
from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
group by destination_uhgs_id


 
/*
select sucre.destination_uhgs_id, sucre.c, tout.c, sucre.somme_tonnage as sucre_somme_tonnage, sucre.nbproduits as sucre_nbproduits, tout.somme_tonnage as tout_somme_tonnage, tout.nbproduits as tout_nbproduits
from 

	(select destination_uhgs_id, count(*) as c , sum(tonnage::int) as somme_tonnage, array_agg(rf.commodity_purpose) as cargo1, 
	array_agg(rf.commodity_purpose2) as cargo2, sum(jsonb_array_length(rf.all_cargos)) as nbproduits
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger')
	and commodity_purpose ilike '%sucre%' or commodity_purpose2 ilike '%sucre%'
	group by destination_uhgs_id ) as sucre,
	
	(select destination_uhgs_id, count(*) as c , sum(tonnage::int) as somme_tonnage, array_agg(rf.commodity_purpose) as cargo1, 
	array_agg(rf.commodity_purpose2) as cargo2, sum(jsonb_array_length(rf.all_cargos)) as nbproduits
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger')
	--and commodity_purpose ilike '%sucre%' or commodity_purpose2 ilike '%sucre%'
	group by destination_uhgs_id ) as tout
where sucre.destination_uhgs_id = tout.destination_uhgs_id
*/

-- pour un graphique vite fait avec ou sans le sucre par pays
select destination_state_1789_fr , count(*) as c, sum(tonnage::int), sum(jsonb_array_length(all_cargos) )
from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180' and extract(year from rf.outdate_fixed) = 1789
and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
--and commodity_purpose ilike '%sucre%' or commodity_purpose2 ilike '%sucre%'
group by destination_state_1789_fr
order by c desc



/*
select destination_uhgs_id, commodity_purpose, count(*) , sum(tonnage::int) 
from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger')
and commodity_purpose ilike '%sucre%'
group by destination_uhgs_id, commodity_purpose
union
(
select destination_uhgs_id, rf.commodity_purpose2  as commodity_purpose, count(*) , sum(tonnage::int)  
from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger')
and commodity_purpose2 ilike '%sucre%'
group by destination_uhgs_id, commodity_purpose2
)
order by destination_uhgs_id
*/


--------------------------------------------------------------------------------------------------
-- Analyse du sucre (exemple de produit colonial à très forte valeur ajoutée)
--------------------------------------------------------------------------------------------------

-- Pour faire la carto par port du sucre par rapport à tout le monde
select sum(total_flux), sum(total_tonnage), sum(flux_sucre),  sum(somme_ton_sucre) from (
select q.destination_uhgs_id, sum(all_conge) as total_flux, sum(all_tonnage) as total_tonnage, sum(coalesce(c, 0)) as flux_sucre, sum(coalesce(q.ton_sucre, 0)) as somme_ton_sucre
from (
select tout.destination_uhgs_id, tout.travel_id, tout.c as all_conge, tout.tonnage as all_tonnage, tout.nbproduits, sucre.c, sucre.ton_sucre
from 
(select travel_id, destination_uhgs_id, 1 as c , tonnage::int , jsonb_array_length(rf.all_cargos) as nbproduits
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
	--and commodity_purpose ilike '%sucre%' or commodity_purpose2 ilike '%sucre%'
) as tout left join
(select travel_id, destination_uhgs_id, 1 as c , tonnage::int , jsonb_array_length(rf.all_cargos) as nbproduits, tonnage::int/jsonb_array_length(rf.all_cargos) as ton_sucre
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
	and (commodity_purpose ilike '%sucre%' or commodity_purpose2 ilike '%sucre%')
) as sucre 
on  tout.travel_id=sucre.travel_id 
) as q
group by destination_uhgs_id
) as k
-- 44030
-- 584	44030	60	2491 -- avant correction BDD sur cargos
-- 583	43560	60	2326 -- après correction BDD sur cargos

select 2491 / 44030.0 * 100 , 60 / 584.0 *100
-- 5% du tonnage pour 10 % des navires en flux sont du sucre
select 2326 / 43560.0 * 100  as part_tons, 60 / 583.0 *100 as part_flux
-- 5% du tonnage pour 10 % des navires en flux sont du sucre


--------------------------------------------------------------------------------------------------
-- Analyse du blé et des céréales 
-- '{"bled","avoine","orge","Avoine","farines","lin","blé"}'
--------------------------------------------------------------------------------------------------


select sum(total_flux), sum(total_tonnage), sum(flux_cereales),  sum(somme_ton_cereales) from (
select q.destination_uhgs_id, sum(all_conge) as total_flux, sum(all_tonnage) as total_tonnage, sum(coalesce(c, 0)) as flux_cereales, sum(coalesce(q.ton_sucre, 0)) as somme_ton_cereales
from (
select tout.destination_uhgs_id, tout.travel_id, tout.c as all_conge, tout.tonnage as all_tonnage, tout.nbproduits, sucre.c, sucre.ton_sucre
from 
(select travel_id, destination_uhgs_id, 1 as c , tonnage::int , jsonb_array_length(rf.all_cargos) as nbproduits
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
	--and commodity_purpose ilike '%sucre%' or commodity_purpose2 ilike '%sucre%'
) as tout left join
(select travel_id, destination_uhgs_id, 1 as c , tonnage::int , jsonb_array_length(rf.all_cargos) as nbproduits, tonnage::int/jsonb_array_length(rf.all_cargos) as ton_sucre
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
	and (commodity_purpose ilike '%blé%' or commodity_purpose2 ilike '%bled%' or commodity_purpose2 ilike '%avoine%' or commodity_purpose2 ilike '%farine%' or commodity_purpose2 ilike '%orge%' or commodity_purpose2 ilike '%lin%')
) as sucre 
on  tout.travel_id=sucre.travel_id 
) as q
group by destination_uhgs_id
) as k


-- 583	43560	2	157
select 157 / 43560.0 * 100  as part_tons, 2 / 583.0 *100 as part_flux
-- 0.36% du tonnage pour 0.34 % des navires en flux sont des céreales

-- qui recoit les céréales
select * from (
select q.destination_uhgs_id, sum(all_conge) as total_flux, sum(all_tonnage) as total_tonnage, sum(coalesce(c, 0)) as flux_cereales, sum(coalesce(q.ton_sucre, 0)) as somme_ton_cereales
from (
select tout.destination_uhgs_id, tout.travel_id, tout.c as all_conge, tout.tonnage as all_tonnage, tout.nbproduits, sucre.c, sucre.ton_sucre
from 
(select travel_id, destination_uhgs_id, 1 as c , tonnage::int , jsonb_array_length(rf.all_cargos) as nbproduits
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
	--and commodity_purpose ilike '%sucre%' or commodity_purpose2 ilike '%sucre%'
) as tout left join
(select travel_id, destination_uhgs_id, 1 as c , tonnage::int , jsonb_array_length(rf.all_cargos) as nbproduits, tonnage::int/jsonb_array_length(rf.all_cargos) as ton_sucre
	from navigoviz.raw_flows rf 
	where rf.departure_uhgs_id = 'A0204180'  and extract(year from rf.outdate_fixed) = 1789
	and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_partner_balance_supp_1789 in ('Etranger') and rf.destination_uhgs_id != 'C0000009'
	and (commodity_purpose ilike '%blé%' or commodity_purpose2 ilike '%bled%' or commodity_purpose2 ilike '%avoine%' or commodity_purpose2 ilike '%farine%' or commodity_purpose2 ilike '%orge%' or commodity_purpose2 ilike '%lin%')
) as sucre 
on  tout.travel_id=sucre.travel_id 
) as q
group by destination_uhgs_id
) as k
where flux_cereales > 0
-- A0079352	7	943	2	157

select * from ports.port_points pp where uhgs_id = 'A0079352'
-- Barcelonne en Espagne

--------------------------------------------------------------------------------------------------
-- demain : filtrer les départs pour la pêche (terre-neuve, island) + commodity_purpose ~ pêche
-- A1964976 Ile feroe
-- A0146289 Islande
-- B0000715 Grands Bancs de Terre-Neuve
--------------------------------------------------------------------------------------------------

--- La pêche 

select rf.destination_uhgs_id, rf.destination_substate_1789_fr , rf.destination_state_1789_fr, rf.tonnage , rf.outdate_fixed , 
rf.commodity_purpose, rf.commodity_purpose2 , rf.commodity_purpose3, rf.commodity_purpose3 , rf.commodity_purpose4 , 
rf.all_cargos , jsonb_array_length(rf.all_cargos)
from navigoviz.raw_flows rf 
where rf.departure_uhgs_id = 'A0204180' and extract(year from rf.outdate_fixed) = 1789
and rf.destination_partner_balance_supp_1789  in ('Etranger')  and rf.destination_state_1789_fr not in ('Grande-Bretagne') and rf.destination_uhgs_id != 'C0000009'
and  rf.destination_uhgs_id = 'A1964976'	