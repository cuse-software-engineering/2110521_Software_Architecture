// Minimal read-only web client (Handlebars + unirest), following the lecture's "simple client".
// It calls the REST API server-side and renders the floor plans as HTML.
//   node client.js   ->  http://localhost:3000/floorplans
const path = require('path')
require('dotenv').config({ path: path.join(__dirname, 'config.env') })
const express = require('express')
const { engine } = require('express-handlebars')
const unirest = require('unirest')

const app = express()
const PORT = process.env.CLIENT_PORT || 3000
const API = process.env.API_URL || `http://localhost:${process.env.PORT || 5000}`

app.engine('.hbs', engine({ defaultLayout: 'main', extname: '.hbs' }))
app.set('view engine', '.hbs')
app.set('views', path.join(__dirname, 'views'))

app.get('/', (req, res) => res.redirect('/floorplans'))

app.get('/floorplans', async (req, res) => {
  try {
    const response = await unirest.get(`${API}/floorplans`)
    res.render('floorplans', { floorPlans: response.body, api: API })
  } catch (err) {
    res.status(502).render('floorplans', { error: `Cannot reach API at ${API}: ${err.message}`, api: API })
  }
})

app.get('/floorplans/:id', async (req, res) => {
  const response = await unirest.get(`${API}/floorplans/${req.params.id}`)
  if (response.status !== 200) {
    return res.status(response.status).render('floorplans', { error: response.body.message, api: API })
  }
  res.render('floorplan', { plan: response.body, api: API })
})

app.listen(PORT, () => console.log(`Client Started on http://localhost:${PORT}/floorplans (API: ${API})`))
