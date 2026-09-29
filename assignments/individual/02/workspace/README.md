# CTRS FloorPlan REST API — assignment demo

REST API for one resource from the Concert Table Reservation System (CTRS) term project:
the **FloorPlan** (venue zone map) from use case UC-04 *Create Venue Zone Map*.

Stack follows the term project's ADR-03 and ADR-06: Node.js + Express + Mongoose on MongoDB.

| | |
|---|---|
| Resource | `/floorplans` |
| Methods | GET all, GET one, POST, PUT (full replace), PATCH (partial), DELETE |
| Database | MongoDB, db `ctrs-demo`, collection `floorplans` |
| Diagrams | [docs/er-diagram.png](docs/er-diagram.png), [docs/architecture.png](docs/architecture.png) |
| Video script | [docs/video-script.md](docs/video-script.md) |
| REST Client file | [route.rest](route.rest) |

## The resource

A floor plan is one document that embeds its zones, and each zone embeds its tables. **FloorPlan is the
aggregate root and the only entity with an `_id`.** Zones, tables, pricing entries and landmarks are embedded
value objects identified by natural keys: a zone by its name, a table by its number, a price by zone plus
table type. Other resources reference them that way (floor plan id + table number), never by a sub-document id.

Table shapes and seat counts follow the venue's printed map (`assignments/group/workspace/report/deliverable-1/assets/zone_map.PNG`):

| type | seats |
|---|---|
| circle | 2 |
| square | 4 |
| sofa | 6 |
| triangle | 1 (Zone B only) |

`capacity` may be omitted when creating a table; the server fills it from the type.
Landmarks (STAGE, LONG TABLE, BAR) are stored with a position but are not bookable.

**Pricing.** Each zone carries the venue's standard price list, one entry per table type, matching the printed
map (Zone A circle 2,400 / square 4,800 / sofa 7,200; Zone B circle 2,000 / square 4,000 / sofa 6,000 /
triangle 700). The floor plan holds the 600 baht `extraPersonFee`. Prices live on the zone, not on each
table, because the price is a function of zone plus type. A ConcertRound (UC-03) copies this list when it is
published, so a round's prices stay frozen even if the floor plan changes later. Booking totals are not
computed here; that is UC-01's job.

Validation implemented from UC-04 plus pricing consistency:
- name required, at least one zone, every zone has a name and at least one table
- zone names are unique in the plan
- every table has a number and a valid type, capacity ≥ 1
- table numbers are unique across the whole floor plan
- every table type used in a zone has exactly one pricing entry in that zone

```json
{
  "name": "Concert Layout - Stage Night",
  "venue": "La Loy Bar, Nanglinchee / Rama 3",
  "status": "active",
  "extraPersonFee": 600,
  "landmarks": [ { "name": "STAGE", "position": { "x": 30, "y": 5 } } ],
  "zones": [
    {
      "name": "Zone A",
      "color": "#5aa35a",
      "pricing": [ { "type": "circle", "packagePrice": 2400, "package": "1 TOWER + 1 ICE" } ],
      "tables": [
        { "number": "A1", "type": "circle", "capacity": 2, "seatViewPhotoUrl": "...", "position": { "x": 5, "y": 12 } }
      ]
    }
  ]
}
```

## API

| Method | Route | Success | Errors |
|---|---|---|---|
| GET | `/floorplans` (optional `?status=active`) | 200 list | 500 |
| GET | `/floorplans/:id` | 200 document | 400 bad id, 404 not found |
| POST | `/floorplans` | 201 created document | 400 validation |
| PUT | `/floorplans/:id` | 200 replaced document | 400 bad id / validation, 404 |
| PATCH | `/floorplans/:id` | 200 updated document | 400, 404 |
| DELETE | `/floorplans/:id` | 200 `{ message, id }` | 400, 404 |

Responses include two computed fields, `tableCount` and `totalCapacity`, that are not stored.

## Setup

```sh
npm install
copy config.env.example config.env     # then edit DATABASE_URL
```

Pick one database option in `config.env`:

- **A. MongoDB Atlas** (recommended for the video): set `DATABASE_URL` to your own cluster's connection string.
- **B. Local MongoDB in Docker**: `docker compose up -d`, keep `DATABASE_URL=mongodb://localhost:27017/ctrs-demo`.
- **C. In-memory MongoDB** (no install, data lost on restart): `npm run start:memory`. The server prints a
  connection string (default `mongodb://127.0.0.1:27018/ctrs-demo`) you can paste into Compass while it runs.
  To seed it, run `npm run seed:memory` in a second terminal (works in PowerShell, cmd and bash).

## Run

```sh
npm run seed      # reset the collection to 2 known floor plans (DATABASE_URL from config.env)
npm run seed:memory   # same, but targets the in-memory server started by npm run start:memory
npm start         # REST API on http://localhost:5000
npm run client    # optional read-only web client on http://localhost:3000/floorplans
npm test          # smoke test of all methods + error cases against the running server
```

Open `route.rest` in VS Code with the REST Client extension and click *Send Request* above each block.
The POST response is captured as `created`, so the following GET / PUT / DELETE reuse its `_id` automatically.

Regenerate the diagrams after editing the `.dot` files (needs Graphviz):

```sh
dot -Tpng -Gdpi=130 docs/er-diagram.dot -o docs/er-diagram.png
dot -Tpng -Gdpi=130 docs/architecture.dot -o docs/architecture.png
```

## Files

```
server.js              Express app, mounts /floorplans
db.js                  MongoDB connection (DATABASE_URL or in-memory fallback)
models/floorplan.js    Mongoose schema: FloorPlan (root) > Zone > Table + Pricing, Landmark, validation
routes/floorplans.js   GET all / GET one / POST / PUT / PATCH / DELETE
seed.js                Reset script with fixed ids
route.rest             VS Code REST Client requests, success and error cases
client.js, views/      Read-only Handlebars client (lecture "simple client" pattern)
test/smoke.js          End-to-end check of every method and error case
docker-compose.yml     Local MongoDB
docs/                  ER diagram, architecture diagram, video script
```
