// Reset the floorplans collection to a known state before recording the demo.
//   npm run seed      -> uses DATABASE_URL from config.env
//   npm run seed:memory   -> seed the in-memory server started by npm run start:memory
//
// Seed data follows the venue's printed zone map (assignments/group/deliverable-1/assets/zone_map.PNG):
//   Zone A (green, stage side)  : circle 2 seats, square 4 seats, sofa 6 seats
//   Zone B (teal, bar side)     : circle, square, sofa, plus triangle 1-seat spots
//   Landmarks                   : STAGE, LONG TABLE, BAR
//   Prices (THB)                : Zone A circle 2,400 / square 4,800 / sofa 7,200
//                                 Zone B circle 2,000 / square 4,000 / sofa 6,000 / triangle 700
//                                 extra person 600
require('dotenv').config({ path: require('path').join(__dirname, 'config.env') })
const mongoose = require('mongoose')
const FloorPlan = require('./models/floorplan')

// Fixed ids so route.rest can reference a seeded document directly.
const IDS = {
  concertLayout: new mongoose.Types.ObjectId('66f0000000000000000000a1'),
  acousticLayout: new mongoose.Types.ObjectId('66f0000000000000000000a2')
}

const photo = (n) => `https://example.com/seatview/${n}.jpg`

const ZONE_A_PRICING = [
  { type: 'circle', packagePrice: 2400, package: '1 TOWER + 1 ICE' },
  { type: 'square', packagePrice: 4800, package: '2 TOWER + 2 ICE' },
  { type: 'sofa', packagePrice: 7200, package: '3 TOWER + 3 ICE' }
]
const ZONE_B_PRICING = [
  { type: 'circle', packagePrice: 2000, package: '1 TOWER + 1 ICE' },
  { type: 'square', packagePrice: 4000, package: '2 TOWER + 2 ICE' },
  { type: 'sofa', packagePrice: 6000, package: '3 TOWER + 3 ICE' },
  { type: 'triangle', packagePrice: 700, package: '1 JUG + 1 ICE' }
]

const seedData = [
  {
    _id: IDS.concertLayout,
    name: 'Concert Layout - Stage Night',
    venue: 'La Loy Bar, Nanglinchee / Rama 3',
    status: 'active',
    extraPersonFee: 600,
    landmarks: [
      { name: 'STAGE', position: { x: 30, y: 5 } },
      { name: 'LONG TABLE', position: { x: 62, y: 35 } },
      { name: 'BAR', position: { x: 95, y: 40 } }
    ],
    zones: [
      {
        name: 'Zone A',
        color: '#5aa35a',
        pricing: ZONE_A_PRICING,
        tables: [
          { number: 'A1', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('A1'), position: { x: 5, y: 12 } },
          { number: 'A2', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('A2'), position: { x: 12, y: 12 } },
          { number: 'A3', type: 'sofa', capacity: 6, seatViewPhotoUrl: photo('A3'), position: { x: 20, y: 12 } },
          { number: 'A4', type: 'square', capacity: 4, seatViewPhotoUrl: photo('A4'), position: { x: 5, y: 25 } },
          { number: 'A5', type: 'square', capacity: 4, seatViewPhotoUrl: photo('A5'), position: { x: 12, y: 25 } },
          { number: 'A6', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('A6'), position: { x: 20, y: 25 } }
        ]
      },
      {
        name: 'Zone B',
        color: '#2a7f7f',
        pricing: ZONE_B_PRICING,
        tables: [
          { number: 'B4', type: 'square', capacity: 4, seatViewPhotoUrl: photo('B4'), position: { x: 75, y: 12 } },
          { number: 'B5', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B5'), position: { x: 83, y: 10 } },
          { number: 'B6', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B6'), position: { x: 83, y: 18 } },
          { number: 'B7', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B7'), position: { x: 89, y: 10 } },
          { number: 'B8', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B8'), position: { x: 89, y: 18 } },
          { number: 'B14', type: 'sofa', capacity: 6, seatViewPhotoUrl: photo('B14'), position: { x: 76, y: 30 } },
          { number: 'B15', type: 'sofa', capacity: 6, seatViewPhotoUrl: photo('B15'), position: { x: 83, y: 30 } },
          { number: 'B16', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B16'), position: { x: 76, y: 38 } },
          { number: 'B17', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B17'), position: { x: 83, y: 38 } },
          { number: 'B22', type: 'square', capacity: 4, seatViewPhotoUrl: photo('B22'), position: { x: 83, y: 46 } },
          { number: 'B23', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B23'), position: { x: 76, y: 52 } },
          { number: 'B24', type: 'circle', capacity: 2, seatViewPhotoUrl: photo('B24'), position: { x: 83, y: 52 } },
          { number: 'T1', type: 'triangle', capacity: 1, seatViewPhotoUrl: photo('T1'), position: { x: 91, y: 28 } },
          { number: 'T2', type: 'triangle', capacity: 1, seatViewPhotoUrl: photo('T2'), position: { x: 91, y: 36 } }
        ]
      }
    ]
  },
  {
    _id: IDS.acousticLayout,
    name: 'Acoustic Layout - Small Show',
    venue: 'La Loy Bar, Nanglinchee / Rama 3',
    status: 'draft',
    extraPersonFee: 600,
    landmarks: [
      { name: 'STAGE', position: { x: 30, y: 5 } },
      { name: 'BAR', position: { x: 95, y: 40 } }
    ],
    zones: [
      {
        name: 'Zone A',
        color: '#5aa35a',
        pricing: ZONE_A_PRICING,
        tables: [
          { number: 'A1', type: 'sofa', capacity: 6, position: { x: 5, y: 12 } },
          { number: 'A2', type: 'sofa', capacity: 6, position: { x: 15, y: 12 } },
          { number: 'A3', type: 'square', capacity: 4, position: { x: 25, y: 12 } }
        ]
      }
    ]
  }
]

async function main() {
  const uri = process.env.DATABASE_URL
  if (!uri) throw new Error('DATABASE_URL is not set in config.env')
  mongoose.set('strictQuery', true)
  try {
    await mongoose.connect(uri, { serverSelectionTimeoutMS: 5000 })
  } catch (err) {
    console.error(`Cannot connect to ${uri}\n${err.message}\n`)
    console.error('Is MongoDB running there? Options:')
    console.error('  - in-memory server (npm run start:memory) -> npm run seed:memory')
    console.error('  - local Docker MongoDB                    -> docker compose up -d, then npm run seed')
    console.error('  - MongoDB Atlas                           -> set DATABASE_URL in config.env, then npm run seed')
    process.exit(1)
  }

  const removed = await FloorPlan.deleteMany({})
  const inserted = await FloorPlan.insertMany(seedData)
  console.log(`Removed ${removed.deletedCount} floor plan(s), inserted ${inserted.length}:`)
  for (const fp of inserted) {
    console.log(`  ${fp._id}  ${fp.name}  [${fp.status}]  ${fp.tableCount} tables / capacity ${fp.totalCapacity}`)
  }
  await mongoose.disconnect()
}

main().catch((err) => {
  console.error(err.message)
  process.exit(1)
})
