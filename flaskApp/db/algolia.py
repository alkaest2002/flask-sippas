from algoliasearch import algoliasearch

# init algolia client
client = algoliasearch.Client("LQMK4ZKUA1", '8bce8f14cb3cfe58b16fcc7e1f3da662')

# init index
index = client.init_index('prod_sippas')

# customize index
index.set_settings({"searchableAttributes": [ "title", "body" ]})