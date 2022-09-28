# NEXT:
# 1) Recipe Serializer / RecipeModel mit
#       TagSerializer(many=True) etc...
#       IngredientSerializer
#
# 2) FoodShop Serializer mit
#       Areas mit
#           AreaParts mit
#               AreaPartIngredients mit
#                   Ingredients
#
# 3) UserCart Serializer mit
#       Ingredients
#
# 4) /user/me/* routes
#
# 5) Write TemplateTest -> devted
# 6) Write CompareObj -> devted
# 7) Refactor tests
# ==> FINISHED
#

# /api/v1/user/me/                      # return me as object
# /api/v1/user/me/watchlists/           # list of user watchlists
# /api/v1/user/me/favorite-recipes/     # list of user recipe favorites
# /api/v1/user/me/favorite-foodshop/    # specific foodshop
# /api/v1/user/me/cart/                 # cart of the user [full joined]
# /api/v1/user/me/cart/count/


# ViewSet Notes

// base ViewSetRoute /api/v1/recipe/[{pk}] <br>
// detail=True, when pk...? /recipe/{pk}/test/  <br>
// detail=False, when pk...? /recipe/test/  <br>
@action(methods=["GET"], detail=False, url_path="test")  <br>
def list_test(self, request: IRequest):  <br>
    return Response({"test": True})  <br>
<br>
@action(methods=["GET"], detail=True, url_path="test") <br>
def retrieve_test(self, request: IRequest, pk): <br>
    return Response({"test_pk": pk}) <br>

# APIView Notes
