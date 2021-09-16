# BetterGraph

BetterGraph programmatically provides graph schemas and resolvers from object 
configuration provided by BetterManager, loaded from database by BetterBase.

### BetterGraph's operation:
##### Queries:
- query_config.json:
```json
{
  "query_model": {
    "name": "fromage",
    "fields": {
      "_id": "str",
      "name": "str",
      "localisation": {
        "country": "Union[str, List[str], None]",
        "region": "Union[str, List[str], None]",
        "city": "Union[str, List[str], None]"
      },
      "gastronomy": {
        "smell": "Union[str, List[str], None]",
        "taste": "Union[str, List[str], None]",
        "similar_cheese": "Union[str, List[str], None]"
      },
      "price": "float",
      "should_be": "str",
      "input_exclude": "str",
      "output_exclude": "str"
    },
    "excluded_query_params": ["gt"],
    "excluded_input_fields": ["input_exclude"],
    "excluded_output_fields": ["output_exclude"]
  }
}
```
- initial_document.json
```json
{
  "id": "1",
  "name": "Maroilles",
  "localisation": {
    "country": "France",
    "region": "Picardie"
  },
  "gastronomy": {
    "smell": "strong",
    "taste": "Very good",
    "similar_cheese": [
      "__NODE__az13e12e3jae93z30J28zE=",
      "__NODE__J30a2e3jaz18zEe12393ze="
    ]
  },
  "price": "5.98",
  "should_be": "excluded_by_projection",
  "input_exclude": "blabla",
  "output_exclude": "blablabla"
}
```
- query_body.json:
```json
{
  "data": {
    "graph": {
      "name": "fromage",
      "query": {
        "query_params": {
          "price__lte": 6.00,
          "price__gt": 5.99
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
- response_body.json
```json
{
  "id": "1",
  "name": "Maroilles",
  "localisation": {
    "country": "France",
    "region": "Picardie"
  },
  "gastronomy": {
    "smell": "strong",
    "taste": "Very good",
    "similar_cheese": [
      "__NODE__az13e12e3jae93z30J28zE=",
      "__NODE__J30a2e3jaz18zEe12393ze="
    ]
  },
  "price": "5.98"
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
        "data": { 
          "TODO": "MUTATION QUERY"
        }
      }
    }
  }
}
```