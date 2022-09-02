----------------------------------------------------------------------------
-- Test the insert-statements of the db
----------------------------------------------------------------------------

-- init user table
INSERT INTO
	public.user(username, email, password, is_staff, is_superuser)
VALUES
	('teddy', 'teddy@email.com', 'hashtest', 1, 1), 
	('user1', 'user1@email.com', 'hashtest', 1, 0),
	('user2', 'user2@email.com', 'test', 0, 0),
	('user3', 'user3@email.com', 'hashtest', 0, 0),
	('user4', 'user4@email.com', 'hashtest', 0, 0);
SELECT * FROM public.user;

-- init units
INSERT INTO
	public.unit(unit_name)
VALUES
	('stk.'),
	('Packung(en)'),
	('g'),
	('kg'),
	('ml'),
	('l'),
	('EL'),
	('TL');
SELECT * FROM public.unit;

-- init day_time
INSERT INTO
	public.day_time(day_time_name)
VALUES
	('vormittag'),
	('mittag'),
	('nachmittag'),
	('abend');
SELECT * FROM public.day_time;

-- init ingredients
INSERT INTO 
	public.ingredient(
		ingredient_name, ingredient_display_name, default_price,
		search_description, quantity_per_unit, unit_id, is_spices
	)
VALUES
	('Barilla Spagetti No3', 'Spagetti No3', 1.89, 'pasta spagetti barilla dünn', 500, 3, 0),
	('Barilla Spagetti No5', 'Spagetti No5', 1.89, 'pasta spagetti barilla normal', 500, 3, 0),
	('Barilla Spagetti No7', 'Spagetti No7', 1.89, 'pasta spagetti barilla dick', 500, 3, 0),
	('Stückige Tomaten', 'Stückige Tomaten', 1.19, 'tomate sauce konserve dose', 280, 4, 0),
	('Knoblauch (Zähen)', 'Knoblauch', 0.99, 'knoblauch zähen', 24, 1, 0),
	('Jodsalz', 'Salz (Jod)', 0.19, 'salz jod einfach', 200, 3, 1),
	('Salz Kristalle', 'Salz (Kristalle)', 2.49, 'salz kristalle ', 400, 3, 1),
	('Pfeffer Roh für die Mühle', 'Pfeffer', 0.99, 'pfeffer roh mühle', 30, 3, 1),
	('Eier 6er', 'Eier', 0.99, 'eier vegetarisch eiweiß', 6, 1, 0),
	('Gouda Jung Packung groß', 'Gouda', 2.39, 'gouda käse eiweiß', 400, 3, 0),
	('Parmesan', 'Parmesan', 2.39, 'parmesan käse eiweiß', 50, 3, 0),
	('Rapsöl', 'Rapsöl', 2.49, 'öl rapsöl', 1000, 4, 0),
	('Bacon Stückchen Doppelpack', 'Bacon', 2.39, 'bacon schinken eiweiß', 250, 3, 0);
SELECT * FROM public.ingredient;

-- init recipe
INSERT INTO
	public.recipe(user_id, recipe_name, person_count, cooking_duration_min, prep_description)
VALUES
	(1, 'Spagetti mit Tomatensauce', 2, 20, 'Spagetti und Sauce kochen'),
	(2, 'Spagetti Carbonara', 2, 15, 'Spagetti kochen. Sauce vorbereiten und mit den Spagetti vermischen.');
SELECT * FROM public.recipe;

-- init recipe ingredients
INSERT INTO
	public.recipe_ingredient(recipe_id, ingredient_id, unit_quantity)
VALUES
	(1, 2, 250),
	(1, 4, 150),
	(1, 5, 1.5),
	(1, 7, 3),
	(1, 8, 3),
	(1, 10, 20),

	(2, 1, 250),
	(2, 7, 3),
	(2, 8, 3),
	(2, 9, 4),
	(2, 11, 20),
	(2, 13, 90),
	(2, 12, 5);
SELECT r.recipe_name, i.ingredient_name, i.ingredient_display_name 
FROM public.recipe_ingredient ri 
JOIN public.recipe r ON ri.recipe_id = r.id
JOIN public.ingredient i ON ri.ingredient_id = i.id;

-- init tag
INSERT INTO
	public.tag(tag_name)
VALUES
	('hauptgericht'),
	('kleines-gericht'),
	('dessert'),
	('backen'),
	('kochen'),
	('beilage'),
	('spargel'),
	('pilze'),
	('tomatensauce'),
	('pasta'),
	('fleisch'),
	('veggi'),
	('vegan');
SELECT * FROM public.tag;

-- init recipe_tag
INSERT INTO
	public.recipe_tag(recipe_id, tag_id)
VALUES
	(1, 1),
	(1, 5),
	(1, 9),
	(1, 10),
	(1, 12),

	(2, 1),
	(2, 5),
	(2, 10),
	(2, 11);
SELECT * FROM public.recipe_tag;

-- init recipe_image
INSERT INTO
	public.recipe_image(recipe_id, image_path)
VALUES
	(1, 'image_path1'),
	(1, 'image_path2'),
	(1, 'image_path3'),
	(2, 'image_path4'),
	(2, 'image_path5'),
	(2, 'image_path6');
SELECT * FROM public.recipe_image;

-- init recipe_favorite
INSERT INTO
	public.recipe_favorite(user_id, recipe_id)
VALUES
	(1, 1),
	(1, 2),
	(2, 2),
	(3, 1),
	(4, 1),
	(5, 1),
	(5, 2);
SELECT u.username, r.recipe_name 
FROM public.recipe_favorite rf 
JOIN public.recipe r ON rf.recipe_id = r.id 
JOIN public.user u ON rf.user_id = u.id;

-- init recipe_rating
INSERT INTO
	public.recipe_rating(user_id, recipe_id, rating)
VALUES
	(1, 1, 5),
	(1, 2, 4.5),
	(2, 1, 4),
	(4, 2, 3.5),
	(5, 1, 5),
	(5, 2, 3.5);
SELECT u.username, r.recipe_name, rr.rating
FROM public.recipe_rating rr
JOIN public.user u ON rr.user_id = u.id
JOIN public.recipe r ON rr.recipe_id = r.id;

-- init watchlist
INSERT INTO
	public.watchlist(user_id, watchlist_name)
VALUES
	(1, 'pasta love'),
	(1, 'pasta ok'),
	(2, 'i like'),
	(3, 'watchlist1'),
	(3, 'watchlist2');
SELECT * FROM public.watchlist;

-- init recipe_watchlist
INSERT INTO
	public.recipe_watchlist(watchlist_id, recipe_id)
VALUES
	(1, 1),
	(2, 2),
	(3, 1),
	(3, 2),
	(4, 1),
	(4, 2),
	(5, 1);
SELECT u.username, w.watchlist_name, r.recipe_name
FROM public.recipe_watchlist rw
JOIN public.watchlist w ON rw.watchlist_id = w.id
JOIN public.user u ON w.user_id = u.id
JOIN public.recipe r ON rw.recipe_id = r.id;

-- init food_shop
INSERT INTO
	public.food_shop(shop_name, address, zip_code, city, shop_comment)
VALUES
	('Kaufland Pankow', 'Breite Straße 19', '13187', 'Berlin', 'Pankow Center'),
	('Kaufland Wedding', 'Residenzstraße 85', '13409', 'Berlin', 'Osloer Straße');
SELECT * FROM public.food_shop;

-- init food_shop_area
INSERT INTO
	public.food_shop_area(food_shop_id, area_name, area_order_number)
VALUES
	(1, 'Eingangsbereich (Gemüse/Convenience)', 1),
	(1, 'Übergangsbereich (Gewürze/Mischungen)', 2),
	(1, 'Brotbereich', 3),
	(1, 'Müsli, Mehl, Fertiggerichte', 4),
	(1, 'Tiefkühlbereich', 5),
	(1, 'Saucen & Asia Gewürze', 6),
	(2, 'Eingangebereich (Gemüse/Gewürze/Mehl/Brot)', 1),
	(2, 'Übergangsbereich', 2),
	(2, 'Milch/Käse/Eier', 3),
	(2, 'TK-Bereich', 4),
	(2, 'Konserven & Fleisch', 5);
SELECT fs.shop_name, a.area_name, a.area_order_number 
FROM public.food_shop fs
JOIN public.food_shop_area a ON fs.id = a.food_shop_id;
	
-- food_shop_area_part
INSERT INTO
	public.food_shop_area_part(area_id, area_part_name, area_part_order_number)
VALUES
	(1, 'Convenience', 1),
	(1, 'Gemüse', 2),
	(1, 'Konserven', 3),
	(2, 'Gewürze', 1),
	(2, 'Fertig-Mischungen', 2),
	(2, 'Süßkram', 3),
	(3, 'Brot', 1),
	(4, 'Müsli', 1),
	(4, 'Mehl/Nudeln/Fertiggerichte', 2),
	(7, 'Gewürze/Mehl/Nudeln', 1),
	(7, 'Gemüse', 2),
	(7, 'Konserven', 3),
	(7, 'Brot', 4),
	(9, 'Milch & Käse', 1),
	(9, 'Joghurts', 2),
	(9, 'Eier & Fertiggerichte', 3);
SELECT fs.shop_name, a.area_name, a.area_order_number, ap.area_part_name, ap.area_part_order_number
FROM public.food_shop_area_part ap
JOIN public.food_shop_area a ON ap.area_id = a.id
JOIN public.food_shop fs ON a.food_shop_id = fs.id;

-- init food_shop_area_part_ingredient
INSERT INTO
	public.food_shop_area_part_ingredient(area_part_id, ingredient_id, ingredient_price)
VALUES
	(9, 1, 1.89),
	(9, 2, 1.89),
	(9, 3, 1.89),
	(3, 4, 0.99),
	(2, 5, 0.19),
	
	(10, 1, 1.99),
	(10, 2, 1.99),
	(10, 3, 1.99),
	(12, 4, 1.09);
SELECT 
	fs.shop_name, a.area_name, 
	a.area_order_number, ap.area_part_name, 
	ap.area_part_order_number, i.ingredient_name, api.ingredient_price
FROM public.food_shop_area_part_ingredient api
JOIN public.ingredient i ON api.ingredient_id = i.id
JOIN public.food_shop_area_part ap ON api.area_part_id = ap.id
JOIN public.food_shop_area a ON ap.area_id = a.id
JOIN public.food_shop fs ON a.food_shop_id = fs.id;

-- recipe_cart
INSERT INTO
	public.recipe_cart(user_id, recipe_name, food_shop_id, date, day_time_id)
VALUES
	(1, 'Recipe1', 1, '01.01.2023', 1),
	(1, 'Recipe2', 1, '01.01.2023', 3),
	(1, 'Recipe1', 1, '01.01.2023', 4),
	(2, 'Recipe8', 1, '05.01.2023', 1),
	(2, 'Recipe9', 1, '05.01.2023', 3),
	(2, 'Recipe13', 1, '05.01.2023', 4);
SELECT * FROM public.recipe_cart;

-- init recipe_cart_ingredient
INSERT INTO
	public.recipe_cart_ingredient(shopping_cart_recipe_id, ingredient_id, buy_unit_quantity)
VALUES
	(1, 1, 1),
	(1, 4, 1),
	(1, 5, 1),
	(2, 1, 1),
	(2, 5, 1),
	(2, 9, 1),
	(2, 11, 1);
SELECT 
	u.username, fs.shop_name,  rc.recipe_name, rc.date, 
	dt.day_time_name, i.ingredient_name, rci.buy_unit_quantity
FROM public.recipe_cart_ingredient rci
JOIN public.recipe_cart rc ON rci.shopping_cart_recipe_id = rc.id
JOIN public.user u ON rc.user_id = u.id
JOIN public.food_shop fs ON rc.food_shop_id = fs.id
JOIN public.day_time dt ON rc.day_time_id = dt.id
JOIN public.ingredient i ON rci.ingredient_id = i.id;

-- init preferred_user_food_shop
INSERT INTO
	public.preferred_user_food_shop(user_id, food_shop_id)
VALUES
	(1, 1),
	(2, 1),
	(3, 2),
	(5, 1);
SELECT ufs.id, u.username, fs.shop_name
FROM public.preferred_user_food_shop ufs
JOIN public.user u ON ufs.user_id = u.id
JOIN public.food_shop fs ON ufs.food_shop_id = fs.id;
