# Next Steps & Notes

## Whats to do

<ol>
    <li>Rewrite Models (Recipe, User, FoodShop, Cart etc.) with ManyToMany-Fields</li>
    <li>Rewrite Serializer</li>
    <li>Rewrite Model tests</li>
    <li>Rewrite API tests</li>
    <li>Rewrite API-ViewSets</li>
    <li>Add "/api/v1/user/me/*" routes</li>
    <li>Upload image to a recipe</li>
</ol>

<br>

## Routes: /user/me/*

/api/v1/user/me/                      # return me as object <br>
/api/v1/user/me/watchlists/           # list of user watchlists <br>
/api/v1/user/me/favorite-recipes/     # list of user recipe favorites <br>
/api/v1/user/me/favorite-foodshop/    # specific foodshop <br>
/api/v1/user/me/cart/                 # cart of the user [full joined] <br>
/api/v1/user/me/cart/count/ <br>

<br>

## ViewSet Notes

base ViewSetRoute /api/v1/recipe/[{pk}] <br>
detail=True by pk /recipe/{pk}/test/ <br>
detail=False no pk /recipe/test/ <br>
@action(methods=["GET"], detail=False, url_path="test") <br>
def list_test(self, request: IRequest): <br>
    return Response({"test": True}) <br>


@action(methods=["GET"], detail=True, url_path="test") <br>
def retrieve_test(self, request: IRequest, pk): <br>
    return Response({"test_pk": pk}) <br>

<br>

## APIView Notes

pass