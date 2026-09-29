require('dotenv').config({ path: require('path').join(__dirname, 'config.env') })
const express = require('express')
const { connect } = require('./db')

const app = express()
app.use(express.json())

// Resource: FloorPlan (venue zone map) — from term-project use case UC-04 "Create Venue Zone Map"
const floorPlansRouter = require('./routes/floorplans')
app.use('/floorplans', floorPlansRouter)

app.get('/', (req, res) => {
  res.json({
    name: 'CTRS FloorPlan REST API',
    resource: '/floorplans',
    methods: ['GET /floorplans', 'GET /floorplans/:id', 'POST /floorplans', 'PUT /floorplans/:id', 'PATCH /floorplans/:id', 'DELETE /floorplans/:id']
  })
})

// Fallback error handler (malformed JSON body etc.)
app.use((err, req, res, next) => {
  if (err.type === 'entity.parse.failed') {
    return res.status(400).json({ message: 'Invalid JSON body' })
  }
  console.error(err)
  res.status(500).json({ message: err.message })
})

const PORT = process.env.PORT || 5000

connect()
  .then(() => app.listen(PORT, () => console.log(`Server Started on http://localhost:${PORT}`)))
  .catch((err) => {
    console.error(err.message)
    process.exit(1)
  })
