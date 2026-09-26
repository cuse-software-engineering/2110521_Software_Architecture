// FloorPlan (venue zone map) — see term project UC-04 "Create Venue Zone Map".
//
// FloorPlan is the aggregate root and the only entity with an _id.
// Zones, tables, pricing entries and landmarks are embedded VALUE OBJECTS:
//   - a zone is identified by (floorPlanId, zone.name)
//   - a table is identified by (floorPlanId, table.number)   [unique across the plan, UC-04 rule]
//   - a pricing entry is identified by (floorPlanId, zone.name, type)
// Other resources (ConcertRound, Booking) reference them by those natural keys.
//
// Table types follow the venue's printed zone map (assignments/group/deliverable-1/assets/zone_map.PNG):
//   circle = 2 seats, square = 4 seats, sofa = 6 seats, triangle = 1 seat (Zone B only)
//
// Pricing is the venue's standard price list per zone and table type (e.g. Zone A circle 2,400 THB,
// "1 TOWER + 1 ICE"). A ConcertRound (UC-03) copies this list when it is published, so prices of a
// round stay frozen even if the floor plan's list changes later.
const mongoose = require('mongoose')

const TABLE_TYPES = ['circle', 'square', 'sofa', 'triangle']
const DEFAULT_CAPACITY = { circle: 2, square: 4, sofa: 6, triangle: 1 }

const positionSchema = new mongoose.Schema(
  {
    x: { type: Number, default: 0 },
    y: { type: Number, default: 0 }
  },
  { _id: false }
)

const tableSchema = new mongoose.Schema(
  {
    number: { type: String, required: true, trim: true },   // natural key, e.g. "B14"
    type: { type: String, required: true, enum: TABLE_TYPES },
    capacity: { type: Number, min: 1 },                     // defaults from type if omitted
    seatViewPhotoUrl: { type: String, default: '' },
    position: { type: positionSchema, default: () => ({}) }
  },
  { _id: false }
)

tableSchema.pre('validate', function (next) {
  if (this.capacity == null && DEFAULT_CAPACITY[this.type]) {
    this.capacity = DEFAULT_CAPACITY[this.type]
  }
  next()
})

// Standard price for one table type inside a zone.
const pricingSchema = new mongoose.Schema(
  {
    type: { type: String, required: true, enum: TABLE_TYPES },
    packagePrice: { type: Number, required: true, min: 0 },  // THB, full table fee for the package
    package: { type: String, default: '' }                   // e.g. "1 TOWER + 1 ICE"
  },
  { _id: false }
)

const zoneSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },     // natural key, e.g. "Zone A"
    color: { type: String, default: '' },                   // display colour on the map
    pricing: { type: [pricingSchema], default: [] },        // one entry per table type used in the zone
    tables: {
      type: [tableSchema],
      validate: [(arr) => arr.length > 0, 'A zone must contain at least one table']
    }
  },
  { _id: false }
)

// Fixed features drawn on the map that are not bookable (stage, long table, bar).
const landmarkSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    position: { type: positionSchema, default: () => ({}) }
  },
  { _id: false }
)

const floorPlanSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    venue: { type: String, default: '' },
    status: { type: String, enum: ['draft', 'active'], default: 'draft' },
    extraPersonFee: { type: Number, default: 0, min: 0 },   // THB per person above table capacity
    landmarks: { type: [landmarkSchema], default: [] },
    zones: {
      type: [zoneSchema],
      validate: [(arr) => arr.length > 0, 'A floor plan must contain at least one zone']
    }
  },
  { timestamps: true }
)

// Aggregate-level rules (UC-04 {Validate the Zone Map} plus pricing consistency).
floorPlanSchema.pre('validate', function (next) {
  const zoneNames = new Set()
  const tableNumbers = new Set()

  for (const zone of this.zones || []) {
    if (zoneNames.has(zone.name)) {
      return next(new Error(`Duplicate zone name "${zone.name}" in floor plan`))
    }
    zoneNames.add(zone.name)

    const pricedTypes = new Set()
    for (const p of zone.pricing || []) {
      if (pricedTypes.has(p.type)) {
        return next(new Error(`Duplicate pricing for type "${p.type}" in zone "${zone.name}"`))
      }
      pricedTypes.add(p.type)
    }

    for (const table of zone.tables || []) {
      if (tableNumbers.has(table.number)) {
        return next(new Error(`Duplicate table number "${table.number}" in floor plan`))
      }
      tableNumbers.add(table.number)

      if (!pricedTypes.has(table.type)) {
        return next(new Error(`Zone "${zone.name}" has a ${table.type} table (${table.number}) but no pricing for type "${table.type}"`))
      }
    }
  }
  next()
})

// Virtuals for convenience in API responses (not stored).
floorPlanSchema.virtual('tableCount').get(function () {
  return (this.zones || []).reduce((n, z) => n + (z.tables || []).length, 0)
})
floorPlanSchema.virtual('totalCapacity').get(function () {
  return (this.zones || []).reduce(
    (n, z) => n + (z.tables || []).reduce((m, t) => m + (t.capacity || 0), 0), 0
  )
})
floorPlanSchema.set('toJSON', { virtuals: true })

module.exports = mongoose.model('FloorPlan', floorPlanSchema)
module.exports.TABLE_TYPES = TABLE_TYPES
module.exports.DEFAULT_CAPACITY = DEFAULT_CAPACITY
