# Recombee Extractor for Keboola

A Keboola Extractor component that fetches recommendations from [Recombee](https://www.recombee.com/) using a selected recommendation endpoint and exports the results as a structured CSV table.

---

## ✨ Features

* Supports following **Recombee recommendation endpoints**:

  * [`Recommend Items to User`](https://docs.recombee.com/api.html#recommend-items-to-user)
  * [`Recommend Items to Item`](https://docs.recombee.com/api.html#recommend-items-to-item)
  * [`Recommend Item Segments to User`](https://docs.recombee.com/api.html#recommend-item-segments-to-user)
* Uses **batch requests** with automatic retry handling
* Supports using [Scenarios](https://docs.recombee.com/scenarios)
* Supports [returning item properties](https://docs.recombee.com/api#recommend-items-to-user-param-includedProperties) (metadata) of the recommended items
* Outputs results with full **Recombee API response** for auditability

---

## 🔧 Configuration Parameters

Set via Keboola UI or `config.json`:

```json
{
  "parameters": {
    "database_id": "your-recombee-db-id",
    "#private_token": "your-recombee-private-token",
    "region": "eu-west",
    "scenario": "emailing",
    "endpoint": "Recommend Items to User",
    "count": 5,
    "included_properties": ["title", "category"],
    "batch_size": 100
  }
}
```

| Field                 | Description                                                       |
| --------------------- | ----------------------------------------------------------------- |
| `database_id`         | Your Recombee Database ID                                         |
| `#private_token`      | Private token used to authenticate requests                       |
| `region`              | Recombee cluster region (e.g., `eu-west`, `us-west`)              |
| `scenario`            | Scenario to be used (defined in Recombee Admin UI)                |
| `endpoint`            | Recommendation endpoint to use (must match scenario)              |
| `count`               | Number of recommendations to return per user/item                 |
| `included_properties` | *(Optional)* List of item properties to include in the response   |
| `batch_size`          | *(Optional)* Number of requests sent per batch. Defaults to `100` |

---

## 🧱 Input Structure

Place a single CSV file in the standard Keboola input directory:
`/data/in/tables/`

Depending on the selected endpoint, you should include:

| Filename    | Used for Endpoint                               |
| ----------- | ----------------------------------------------- |
| `users.csv` | Recommend Items to User / Item Segments to User |
| `items.csv` | Recommend Items to Item                         |

The CSV file must contain a single column with IDs of users / items for which recommendations should be generated.

---

##  🧱 Example Input

```
user_id
user_3fa8c1
user_4b92d8
user_7c13f0
user_1d8a9e
```
---

## 📤 Output Format

The output will be written to:
`/data/out/tables/recomms.csv`

| Column                                            | Description                                                                |
| ------------------------------------------------- | -------------------------------------------------------------------------- |
| `user_id` / `item_id`                             | ID of the user or item the recommendation was generated for                |
| `recomm_id`                                       | Recombee `recommId` used for tracking                                      |
| `recommended_items` / `recommended_item_segments` | List of recommended item/segment IDs                                       |
| `api_response`                                    | Full JSON response from Recombee (including e.g., the returned properties) |

---

## 📤 Example Output

```csv
user_id,recomm_id,recommended_items,api_response
user_3fa8c1,cc08bcf0-9d8e-4726-8b21-e47f770316e1,"[""item-165"", ""item-69"", ""item-857""]","{""recommId"": ""cc08bcf0-9d8e-4726-8b21-e47f770316e1"", ""recomms"": [{""id"": ""item-165""}, {""id"": ""item-69""}, {""id"": ""item-857""}], ""numberNextRecommsCalls"": 0}"
user_4b92d8,9c291302-abcd-4ab4-b926-aceac05ad15a,"[""item-165"", ""item-69"", ""item-857""]","{""recommId"": ""9c291302-abcd-4ab4-b926-aceac05ad15a"", ""recomms"": [{""id"": ""item-165""}, {""id"": ""item-69""}, {""id"": ""item-857""}], ""numberNextRecommsCalls"": 0}"
```

---

## 🐳 Local Development

### Build the Docker image:

```bash
docker build -t recombee-extractor .
```

### Run locally with test data:

```bash
docker run --rm -v $(pwd)/data:/data recombee-extractor
```

---

## 📋 Error Handling

* Retries on:

  * `ResponseException` (5xx errors)
  * `ApiTimeoutException`
* Logs:

  * Success/failure summaries
  * Up to 5 example errors
  * Error codes and frequency

---

## 🛠 Tech Stack

* Python 3.11
* [Recombee Python API Client](https://github.com/recombee/python-api-client)
* Dockerized for Keboola compatibility

---

## 📄 License

The Recombee Extractor for Keboola is provided under the [MIT License](https://opensource.org/licenses/MIT).
