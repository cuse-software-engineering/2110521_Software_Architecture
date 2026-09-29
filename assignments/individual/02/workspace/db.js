// Database connection helper.
//
// Normal mode  : connects to DATABASE_URL from config.env (MongoDB Atlas or local/Docker MongoDB).
// Memory mode  : USE_MEMORY_DB=true starts an in-process MongoDB (mongodb-memory-server) on
//                MEMORY_DB_PORT so MongoDB Compass can still be pointed at it while the server runs.
//                Data is lost when the process exits, so use a real database for the recorded demo.
const mongoose = require('mongoose')

async function connect() {
  let uri = process.env.DATABASE_URL

  if (process.env.USE_MEMORY_DB === 'true') {
    const { MongoMemoryServer } = require('mongodb-memory-server')
    const port = Number(process.env.MEMORY_DB_PORT || 27018)
    const mongod = await MongoMemoryServer.create({
      instance: { port, dbName: 'ctrs-demo' }
    })
    uri = mongod.getUri('ctrs-demo')
    console.log(`In-memory MongoDB started at ${uri}`)
    console.log('Compass connection string:', uri)
  }

  if (!uri) {
    throw new Error('DATABASE_URL is not set. Copy config.env.example to config.env or run with USE_MEMORY_DB=true.')
  }

  mongoose.set('strictQuery', true)
  await mongoose.connect(uri)
  console.log('Connected to Database')
  return mongoose.connection
}

module.exports = { connect }
