# Recombee Writer for Keboola

A Keboola Writer component that uploads items, users, and interactions to [Recombee](https://www.recombee.com/).

---

## ✨ Features

- Uploads [**Items Catalog**](https://docs.recombee.com/api.html#set-item-values) and [**Users Catalog**](https://docs.recombee.com/api.html#set-user-values)
- Supports all standard **Recombee interactions**:
  - [`AddDetailView`](https://docs.recombee.com/api.html#add-detail-view)
  - [`AddPurchase`](https://docs.recombee.com/api.html#add-purchase)
  - [`AddRating`](https://docs.recombee.com/api.html#add-rating)
  - [`AddBookmark`](https://docs.recombee.com/api.html#add-bookmark)
  - [`AddCartAddition`](https://docs.recombee.com/api.html#add-cart-addition)
  - [`SetViewPortion`](https://docs.recombee.com/api.html#set-view-portion)
- Supports **optional fields** (e.g., `timestamp`, `recomm_id`, `additional_data`)
- Gracefully handles bad data (e.g. `NaN`, invalid types) and logs summarizations
- Retries on **timeouts** and **server-side errors**


---

## 🔧 Configuration Parameters

Set via Keboola UI or `config.json`:

```json
{
  "parameters": {
    "database_id": "your-recombee-db-id",
    "#private_token": "your-recombee-private-token",
    "region": "eu-west"
  }
}
```


---

## 🧱 Input Structure

Place CSV files in the standard Keboola input directory:  
`/data/in/tables/`

Supported filenames:

| Filename             | Request Type                                                                 |
|----------------------|------------------------------------------------------------------------------|
| `items.csv`          | [Set Item Values](https://docs.recombee.com/api.html#set-item-values)       |
| `users.csv`          | [Set User Values](https://docs.recombee.com/api.html#set-user-values)       |
| `detail_views.csv`   | [Add Detail View](https://docs.recombee.com/api.html#add-detail-view)       |
| `purchases.csv`      | [Add Purchase](https://docs.recombee.com/api.html#add-purchase)             |
| `ratings.csv`        | [Add Rating](https://docs.recombee.com/api.html#add-rating)                 |
| `bookmarks.csv`      | [Add Bookmark](https://docs.recombee.com/api.html#add-bookmark)             |
| `cart_additions.csv` | [Add Cart Addition](https://docs.recombee.com/api.html#add-cart-addition)   |
| `view_portions.csv`  | [Set View Portion](https://docs.recombee.com/api.html#set-view-portion)     |


---

## 📤 Example Input: `detail_views.csv`

```csv
user_id,item_id,timestamp,recomm_id,additional_data
user-1,item-10,2025-07-06T21:12:43Z,644c005f-aa99-4bce-aa55-a0c610e80df0,"{""source"": ""newsletter""}"
user-2,item-09,2025-07-06T21:09:13Z,,"{""source"": ""newsletter""}"
user-3,item-05,2025-07-06T21:14:45Z,2d2eb48f-cd65-421a-943b-0e015055fd8e,"{""source"": ""homepage""}"
```

## 📤 Example Input: `items.csv`

Properties (columns) shall be created in the [Recombee Admin UI](https://admin.recombee.com/).

```csv
item_id,title,price,available,date_added,tags
item-01,Wireless Mouse,25.99,true,2025-07-20T10:11:49.039302,"[""electronics"", ""accessory"", ""mouse""]"
item-42,Mechanical Keyboard,75.49,false,2025-08-04T10:11:49.039318,"[""electronics"", ""keyboard""]"
item-77,USB-C Hub,34.9,true,2025-08-19T10:11:49.039321,"[""electronics"", ""usb"", ""hub""]"
```

---

## 🐳 Local Development

### Build the Docker image:
```bash
docker build -t recombee-writer .
```

### Run locally with test data:
```bash
docker run --rm -v $(pwd)/data:/data recombee-writer
```

---

## 📋 Error Handling

- Retries on:
  - `ResponseException` (5xx status codes)
  - `ApiTimeoutException`
- Aggregates and logs:
  - Success/failure counts
  - Example errors (up to 5)
  - Error code frequency

---

## 🛠 Tech Stack

- Python 3.11
- [Recombee Python API Client](https://github.com/recombee/python-api-client)
- Dockerized for Keboola compatibility

---

## 📄 License

The Recombee Writer for Keboola is provided under the [MIT License](https://opensource.org/licenses/MIT).