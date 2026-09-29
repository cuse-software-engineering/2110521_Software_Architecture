# Video Script — FloorPlan REST API Demo (≤ 5 minutes)

**Assignment:** one resource from the term project, its database, and a REST API with GET ONE / GET ALL / POST / PUT / DELETE, demonstrated on video with the database contents changing after each call.

**Resource chosen:** `FloorPlan` (venue zone map) from use case UC-04 *Create Venue Zone Map* of the Concert Table Reservation System (CTRS).

## Screen setup before recording

| Window | Content |
|---|---|
| Left half | VS Code with `route.rest` open, response pane on the right of the editor |
| Right half | MongoDB Compass, database `ctrs-demo`, collection `floorplans`, in **JSON view** |
| Terminal (VS Code bottom panel) | `npm start` already running, server log visible |
| Optional tab | Browser at `http://localhost:3000/floorplans` (client running with `npm run client`) |

Checklist:
- [ ] `npm run seed` executed, Compass shows **2 documents**
- [ ] Recorder set to capture the whole screen, microphone tested
- [ ] `docs/er-diagram.png` and `docs/architecture.png` open in an image viewer tab
- [ ] `assignments/group/workspace/report/deliverable-1/assets/zone_map.PNG` open for the intro

## Timeline

Total target: **4 min 30 s**, leaving 30 s of slack.

### 0:00 – 0:35 · Introduction (35 s)

Show `zone_map.PNG`, then `er-diagram.png`, then `architecture.png`.

> "Hi, I'm [name] from group SE 101. Our term project is a Concert Table Reservation System for a bar. Customers pick a specific table on a floor plan like this one, with Zone A near the stage and Zone B near the bar. Tables come in four shapes: circle for two people, square for four, sofa for six, and triangle for one.
>
> For this assignment I picked the **FloorPlan** resource from use case UC-04. One MongoDB document holds the whole map: the floor plan is the aggregate root, it embeds its zones, and each zone embeds its tables and its price list per table type, exactly like the printed map. Zones and tables are value objects identified by name and number, so they have no ids of their own. Landmarks like the stage and bar are stored too, but are not bookable.
>
> The stack is Node.js with Express and Mongoose, MongoDB as the database, and I'll call the API from the VS Code REST Client while Compass shows the collection on the right."

### 0:35 – 1:05 · GET ALL (30 s)

Send request **1. GET ALL**.

> "GET on `/floorplans` returns every floor plan. There are two seeded documents: the active Concert Layout with 20 tables, and a draft Acoustic Layout. The response includes computed fields, `tableCount` and `totalCapacity`, that are not stored in the database."

Point at Compass: two documents, same ids.

Optionally send **1b** to show `?status=active` filtering.

### 1:05 – 1:30 · GET ONE (25 s)

Send request **2. GET ONE**.

> "GET with an id returns a single plan. Here is the Concert Layout: Zone A with six tables, Zone B with fourteen including the two triangle seats. Each zone shows its price list, for example a sofa is 7,200 in Zone A but 6,000 in Zone B, and the plan carries the 600 baht extra-person fee. Each table has its number, type, capacity, seat-view photo and position on the map."

Expand the same document in Compass to show it matches.

### 1:30 – 2:15 · POST (45 s)

Scroll to request **3. POST**, briefly show the body, send.

> "POST creates a new floor plan. I send only the name, venue, landmarks and zones. Notice the tables have no capacity field: the server fills it in from the type. The response is **201 Created** with the new `_id` and timestamps."

Refresh Compass: **3 documents**. Click the new one.

> "Compass now shows three documents, and here is the one we just created, with capacities filled in: circle 2, square 4, sofa 6, triangle 1."

### 2:15 – 2:55 · PUT (40 s)

Send request **5. PUT**.

> "PUT replaces the whole resource. The REST Client reuses the id captured from the POST response. I rename the plan, set it to active, and send a new layout with only Zone A and three tables. Fields I leave out go back to their defaults, which is what makes PUT different from PATCH."

Refresh Compass, open the document.

> "Same id, new name, status active, and Zone B is gone. The `updatedAt` timestamp changed while `createdAt` did not."

Optional 10 s: send **5b. PATCH** on the seeded plan to show a partial update changing only `status`.

### 2:55 – 3:25 · DELETE (30 s)

Send request **6. DELETE**, then **6b. GET ONE after delete**.

> "DELETE removes the plan and returns a confirmation with the id. Calling GET on the same id now returns **404 Not Found**."

Refresh Compass: back to **2 documents**.

### 3:25 – 4:05 · Validation and error codes (40 s)

Send **E1**, **E4**, **E6** in sequence.

> "A few error cases. A malformed id gives **400**. This one matters for our use case: UC-04 says table numbers must be unique across the whole map, so sending the same number X1 in Zone A and Zone B is rejected with **400** and a clear message. And a zone that contains a sofa table but has no sofa price is rejected too, so a customer can never pick a table that cannot be priced."

Point at Compass: still 2 documents, nothing invalid was stored.

### 4:05 – 4:30 · Wrap-up (25 s)

Optional: switch to the browser tab at `localhost:3000/floorplans` and click a plan.

> "Finally, a small read-only web client built with Handlebars calls the same API server-side and renders the floor plans as HTML, following the client pattern from the lecture.
>
> To summarise: one resource, FloorPlan, stored as a nested MongoDB document with the venue's price list; five methods with proper status codes; and business validation from the use case. The next resource in our project will be ConcertRound, which references a floor plan by id and copies its price list when the round is published. Thank you."

## Reset between takes

```sh
npm run seed
```

Then refresh Compass and confirm 2 documents before starting the recorder again.

## After recording

1. Export as **mp4**, check the length is under 5:00.
2. Upload to YouTube (Unlisted or Public) or Google Drive with **Anyone with the link**.
3. Open the link in a private browser window to confirm it plays without signing in.
4. Submit the link in the assignment.
