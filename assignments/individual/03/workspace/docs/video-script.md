# Video Script — gRPC restaurant CRUD with MongoDB (≤ 5 min)

Required by task.txt: add / edit / delete through the web page with the database shown after each,
the model code, the .env with the connection string, and the server code that was changed.
Narration is optional; if no mic, move the mouse over what you are talking about.

## Screen setup before recording

| Window | Content |
|---|---|
| Left | Browser at `http://localhost:3000` |
| Right | MongoDB Compass, database `restaurant`, collection `menus` (Documents tab) |
| Bottom / second desktop | VS Code with `models/Menu.js`, `.env`, `server/server.js`, and a terminal |

Checklist:
- [ ] Docker Desktop running and `npm run mongo` done in `restaurant/` (or Atlas reachable)
- [ ] `npm run seed` done (or `npm run db:clear` if you want to add items live), Compass shows the expected count
- [ ] `npm start` and `npm run client` running, page lists 3 items
- [ ] `docs/architecture.png` open in an image viewer tab for the intro
- [ ] Recorder captures the whole screen

## Timeline (target 4:30)

### 0:00 – 0:30 · Intro

Show `docs/architecture.png`.

> "This is the gRPC restaurant sample from the lecture. The browser talks to an Express web app, which is a gRPC client, and the gRPC server used to keep the menu in an array. For the assignment I connected the gRPC server to MongoDB with mongoose. On the right is Compass showing the `menus` collection with the three seeded items."

### 0:30 – 1:20 · Create

Click **Add New**, enter `Green Curry` / `150`, Create.

> "Insert calls `Menu.create`. The page reloads with the new row, and the Menu ID column now shows a MongoDB ObjectId instead of a UUID."

Refresh Compass → **4 documents**, open the new one.

> "Compass has the same document, with `name`, `price`, and timestamps added by the schema."

### 1:20 – 2:10 · Update

Click **Edit** on Green Curry, change to `Green Curry (spicy)` / `180`, Update.

> "Update does `findById`, changes the fields, and `save()`. The row changed."

Refresh Compass → same `_id`, new name and price, `updatedAt` changed.

### 2:10 – 2:50 · Delete

Click **Remove** on Green Curry, confirm.

> "Remove uses `findByIdAndDelete`. The row is gone."

Refresh Compass → back to **3 documents**.

### 2:50 – 3:20 · Model and env

Switch to VS Code, show `models/Menu.js`.

> "The model is a mongoose schema with `name` and `price`. `toMenuItem` converts the document to the proto's `MenuItem` shape, mapping `_id` to the string `id` field."

Show `.env` (hover over `DATABASE_URL`; blur or partially cover the password if it is Atlas).

### 3:20 – 4:20 · Server changes via git diff

In the VS Code terminal, inside `restaurant/`:

```sh
git log --oneline
git diff a1903ba HEAD -- server/server.js
```

Or open Source Control → compare with the first commit for a side-by-side view.

> "The first commit is the untouched lecture code. The diff shows what changed: dotenv and mongoose are loaded, the in-memory array and uuid are gone, and every handler is `async` and awaits the model. `getAllMenu` maps the documents to `MenuItem`, `get` and `update` use `findById`, `remove` uses `findByIdAndDelete`. Errors are converted to gRPC status codes: a bad or unknown id returns NOT_FOUND, a validation error returns INVALID_ARGUMENT. The server connects to the database before it binds the port."

### 4:20 – 4:40 · Wrap-up

> "So the web client and the proto are unchanged; only the server's data layer moved from memory to MongoDB. Thank you."

## Reset between takes

```sh
npm run seed        # back to the 3 lecture items
npm run db:clear    # or start from an empty collection
```

Refresh Compass and confirm the count before pressing record.

## If recording is impossible (screenshot fallback from task.txt)

Capture, in this order: add via web + Compass after; edit via web + Compass after; delete via web +
Compass after; `models/Menu.js`; `.env`; the `git diff` of `server/server.js`.
