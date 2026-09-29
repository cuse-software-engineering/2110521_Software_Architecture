// Clear the database used by the gRPC server.
//   npm run db:clear           -> delete every document in the menus collection (collection stays)
//   npm run db:clear -- --drop -> drop the whole database
require("dotenv").config({ path: require("path").join(__dirname, "..", ".env") });
const mongoose = require("mongoose");
const Menu = require("../models/Menu");

async function main() {
    mongoose.set("strictQuery", true);
    await mongoose.connect(process.env.DATABASE_URL, { serverSelectionTimeoutMS: 5000 });
    const dbName = mongoose.connection.name;

    if (process.argv.includes("--drop")) {
        await mongoose.connection.dropDatabase();
        console.log(`Dropped database "${dbName}"`);
    } else {
        const result = await Menu.deleteMany({});
        console.log(`Deleted ${result.deletedCount} document(s) from "${dbName}.menus"; remaining: ${await Menu.countDocuments()}`);
    }
    await mongoose.disconnect();
}

main().catch((err) => {
    console.error("Clear failed:", err.message);
    console.error("Is MongoDB running? Start it with `npm run mongo` (Docker) or check DATABASE_URL in .env.");
    process.exit(1);
});
