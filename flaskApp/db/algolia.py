import os
from algoliasearch import algoliasearch

# init algolia client
application_id = os.getenv("ALGOLIA_APPLICATION_ID")
admin_api_key = os.getenv("ALGOLA_ADMIN_API_KEY")
client = algoliasearch.Client(application_id, admin_api_key)

# init index
index = client.init_index('prod_sippas')

# customize index
index.set_settings({"searchableAttributes": [ "title", "body" ]})