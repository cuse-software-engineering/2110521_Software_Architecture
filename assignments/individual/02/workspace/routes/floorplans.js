const express = require('express')
const mongoose = require('mongoose')
const router = express.Router()
const FloorPlan = require('../models/floorplan')

// Fields a client is allowed to send. _id / timestamps are server-managed.
function pickBody(body) {
  const { name, venue, status, extraPersonFee, landmarks, zones } = body
  return { name, venue, status, extraPersonFee, landmarks, zones }
}

// Middleware: load one floor plan by :id, or answer 400 / 404.
async function getFloorPlan(req, res, next) {
  if (!mongoose.isValidObjectId(req.params.id)) {
    return res.status(400).json({ message: `Invalid id "${req.params.id}"` })
  }
  let floorPlan
  try {
    floorPlan = await FloorPlan.findById(req.params.id)
    if (floorPlan == null) {
      return res.status(404).json({ message: 'Cannot find floor plan' })
    }
  } catch (err) {
    return res.status(500).json({ message: err.message })
  }
  res.floorPlan = floorPlan
  next()
}

// GET ALL
router.get('/', async (req, res) => {
  try {
    const filter = req.query.status ? { status: req.query.status } : {}
    const floorPlans = await FloorPlan.find(filter).sort({ createdAt: 1 })
    res.json(floorPlans)
  } catch (err) {
    res.status(500).json({ message: err.message })
  }
})

// GET ONE
router.get('/:id', getFloorPlan, (req, res) => {
  res.json(res.floorPlan)
})

// POST — create
router.post('/', async (req, res) => {
  const floorPlan = new FloorPlan(pickBody(req.body))
  try {
    const created = await floorPlan.save()
    res.status(201).json(created)
  } catch (err) {
    res.status(400).json({ message: err.message })
  }
})

// PUT — full replace (every required field must be sent again)
router.put('/:id', getFloorPlan, async (req, res) => {
  try {
    const replacement = pickBody(req.body)
    // PUT = full replace: fields omitted from the body fall back to schema defaults.
    res.floorPlan.set({
      name: replacement.name,
      venue: replacement.venue ?? '',
      status: replacement.status ?? 'draft',
      extraPersonFee: replacement.extraPersonFee ?? 0,
      landmarks: replacement.landmarks ?? [],
      zones: replacement.zones
    })
    res.floorPlan.markModified('zones')
    res.floorPlan.markModified('landmarks')
    const updated = await res.floorPlan.save() // runs schema + duplicate-table validation
    res.json(updated)
  } catch (err) {
    res.status(400).json({ message: err.message })
  }
})

// PATCH — partial update (only the fields present in the body change)
router.patch('/:id', getFloorPlan, async (req, res) => {
  const patch = pickBody(req.body)
  for (const key of Object.keys(patch)) {
    if (patch[key] !== undefined) res.floorPlan[key] = patch[key]
  }
  try {
    const updated = await res.floorPlan.save()
    res.json(updated)
  } catch (err) {
    res.status(400).json({ message: err.message })
  }
})

// DELETE
router.delete('/:id', getFloorPlan, async (req, res) => {
  try {
    await res.floorPlan.deleteOne()
    res.json({ message: 'Deleted floor plan', id: req.params.id })
  } catch (err) {
    res.status(500).json({ message: err.message })
  }
})

module.exports = router
