[![Backend Checks](https://github.com/enricogoerlitz/WeeklyChef/actions/workflows/backend_checks.yml/badge.svg)](https://github.com/enricogoerlitz/WeeklyChef/actions/workflows/backend_checks.yml)

# WeeklyChef-Project

## What is this project about?

This project is an Recipe / Cart API, written in Python with the Framework Django & the Django-REST-Framework.

With this API can a client save recipes, see other recipes, mark favorite recipes, add recipes to own created watchlists, rate recipes and add tags to recipes.

The API also give the client the possibility to add specific recipes and single ingredients to a cart at a certain date and day time (morning, evening etc). This card will be used for the shopping in the food shop. The cart also calculates the predicted price.

The food shop is split into different areas. Each area is split into different parts. And the ingredients are assigned to the area part. The cart sorts the ingredients at the shopping process by the areas and area parts. This allows the client to navigate smart to their ingredients. No scrolling, searching and finding is necessary within the shopping process, because the ingredients are orderly in the food shop.
