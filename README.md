# BetterGraph

BetterGraph programmatically provides graph schemas and resolvers from object 
configuration provided by BetterManager, loaded from database by BetterBase.

### BetterGraph's operation:
##### Queries:
- query_body.json:
```json
{
  "data": {
    "graph": {
      "name": "fromage",
      "query": {
        "query_params": {
      "price__lte": 6.00
    },
        "projection": {
          "_id": 1,
          "name": 1,
          "localisation": {
            "country": 1,
            "region": 1,
            "city": 1
          },
          "gastronomy": {
            "smell": 1,
            "taste": 1,
            "similar_cheese": 1
          },
          "price": 1,
          "input_exclude": 1,
          "output_exclude": 1
        }
      }
    }
  }
}
```

##### Mutations:
- mutation_body.json
```json
{
  "data": {
    "graph": {
      "name": "fromage",
      "mutation": {
        "type": "create",
        "data": { THE MUTATION QUERY }
      }
    }
  }
}
```