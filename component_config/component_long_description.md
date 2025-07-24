# Recombee Extractor for Keboola

The Recombee Extractor fetches recommendations from [Recombee](https://www.recombee.com/) via selected recommendation endpoint and exports the results as structured CSV tables.

---

## Supported Recommendation Endpoints

* [`Recommend Items to User`](https://docs.recombee.com/api.html#recommend-items-to-user)
* [`Recommend Items to Item`](https://docs.recombee.com/api.html#recommend-items-to-item)
* [`Recommend Item Segments to User`](https://docs.recombee.com/api.html#recommend-item-segments-to-user)

---

## Input Structure

Place one CSV file into `in/tables/`, depending on the selected recommendation endpoint.

| Filename     | Used For Endpoint(s)                                                                                                                                                                |
| ------------ |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `users.csv`  | [Recommend Items to User](https://docs.recombee.com/api#recommend-items-to-user) / [Recommend Item Segments to User](https://docs.recombee.com/api#recommend-item-segments-to-user) |
| `items.csv`  | [Recommend Items to Item](https://docs.recombee.com/api#recommend-items-to-item)                                                                                                    |

The CSV file must contain a single column with IDs of users / items for which recommendations should be generated.

### Example Input

```
user_id
user_3fa8c1
user_4b92d8
user_7c13f0
user_1d8a9e
```

---

## Output Format

The recommendations are exported to:
`out/tables/recomms.csv`

| Column                                            | Description                                                                |
| ------------------------------------------------- |----------------------------------------------------------------------------|
| `user_id` / `item_id`                             | The ID the recommendation was generated for                                |
| `recomm_id`                                       | Recombee [recommId](https://docs.recombee.com/getting_started#reporting-successful-recommendations) used for tracking                                    |
| `recommended_items` / `recommended_item_segments` | List of recommended item or segment IDs                                    |
| `api_response`                                    | Full JSON response from Recombee (including e.g., the returned properties) |


---

### Example Output: `recomms.csv`

```csv
user_id,recomm_id,recommended_items,api_response
user_3fa8c1,cc08bcf0-9d8e-4726-8b21-e47f770316e1,"[""item-165"", ""item-69"", ""item-857""]","{""recommId"": ""cc08bcf0-9d8e-4726-8b21-e47f770316e1"", ""recomms"": [{""id"": ""item-165""}, {""id"": ""item-69""}, {""id"": ""item-857""}], ""numberNextRecommsCalls"": 0}"
user_4b92d8,9c291302-abcd-4ab4-b926-aceac05ad15a,"[""item-165"", ""item-69"", ""item-857""]","{""recommId"": ""9c291302-abcd-4ab4-b926-aceac05ad15a"", ""recomms"": [{""id"": ""item-165""}, {""id"": ""item-69""}, {""id"": ""item-857""}], ""numberNextRecommsCalls"": 0}"
```

---

### Notes

* Use the `Included Properties` configuration parameter to include item metadata such as `title`, `url`, `category`, or `price` in the `api_response` column.
* All values in `recommended_items` or `recommended_item_segments` are exported as JSON arrays.
