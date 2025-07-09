The Recombee Writer uploads items, users, and interactions from CSV tables into [Recombee](https://www.recombee.com/) to power personalized recommendations and search. It supports all major Recombee APIs for catalog and behavior data ingestion.

---
## Input Structure

Place CSV files in `in/tables/`.


### Catalog
| Filename             | Recombee API                                                            | Required Columns                | Optional Columns                                                                   |
| -------------------- | ----------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------- |
| `items.csv`          | [SetItemValues](https://docs.recombee.com/api.html#set-item-values)     | `item_id`                       | All others based on your Recombee item properties (e.g. `title`, `price`, `tags`)  |
| `users.csv`          | [SetUserValues](https://docs.recombee.com/api.html#set-user-values)     | `user_id`                       | All others based on your Recombee user properties (e.g. `subscribed_topics`, `age`, `country`) |

### Interactions
| Filename             | Recombee API                                                            | Required Columns                | Optional Columns                                                                   |
| -------------------- | ----------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------- |
| `bookmarks.csv`      | [AddBookmark](https://docs.recombee.com/api.html#add-bookmark)          | `user_id`, `item_id`            | `timestamp`, `recomm_id`, `additional_data`                                        |
| `cart_additions.csv` | [AddCartAddition](https://docs.recombee.com/api.html#add-cart-addition) | `user_id`, `item_id`            | `timestamp`, `recomm_id`, `amount`, `additional_data`                              |
| `detail_views.csv`   | [AddDetailView](https://docs.recombee.com/api.html#add-detail-view)     | `user_id`, `item_id`            | `timestamp`, `recomm_id`, `duration`, `additional_data`                            |
| `purchases.csv`      | [AddPurchase](https://docs.recombee.com/api.html#add-purchase)          | `user_id`, `item_id`            | `timestamp`, `recomm_id`, `amount`, `price`, `profit`, `additional_data`           |
| `ratings.csv`        | [AddRating](https://docs.recombee.com/api.html#add-rating)              | `user_id`, `item_id`, `rating`  | `timestamp`, `recomm_id`, `additional_data`                                        |
| `view_portions.csv`  | [SetViewPortion](https://docs.recombee.com/api.html#set-view-portion)   | `user_id`, `item_id`, `portion` | `timestamp`, `recomm_id`, `additional_data`                                        |

---

### Notes:

* `item_id` / `user_id` must always be in the **first column** for catalog files.
* Columns such as `tags`, `additional_data`, `imageList` should be passed as valid JSON strings.
---

## Example Input: `detail_views.csv`

```csv
user_id,item_id,timestamp,recomm_id,additional_data
user-1,item-10,2025-07-06T21:12:43Z,644c005f-aa99-4bce-aa55-a0c610e80df0,"{""source"": ""newsletter""}"
user-2,item-09,2025-07-06T21:09:13Z,,"{""source"": ""newsletter""}"
user-3,item-05,2025-07-06T21:14:45Z,2d2eb48f-cd65-421a-943b-0e015055fd8e,"{""source"": ""homepage""}"
```

---

## Example Input: `items.csv`

Item properties must be created in the [Recombee Admin UI](https://admin.recombee.com/):

```csv
item_id,title,price,available,date_added,tags
item-01,Wireless Mouse,25.99,true,2025-07-20T10:11:49.039302,"[""electronics"", ""accessory"", ""mouse""]"
item-42,Mechanical Keyboard,75.49,false,2025-08-04T10:11:49.039318,"[""electronics"", ""keyboard""]"
item-77,USB-C Hub,34.9,true,2025-08-19T10:11:49.039321,"[""electronics"", ""usb"", ""hub""]"
```
