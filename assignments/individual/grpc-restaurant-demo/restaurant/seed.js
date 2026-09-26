// Reset the menus collection to the three items from the original in-memory server.
//   node seed.js
require("dotenv").config();
const mongoose = require("mongoose");
const Menu = require("./models/Menu");

const seedData = [
    { name: "Tomyam Gung", price: 500 },
    { name: "Somtam", price: 60 },
    { name: "Pad-Thai", price: 120 }
];

async function main() {
    mongoose.set("strictQuery", true);
    await mongoose.connect(process.env.DATABASE_URL, { serverSelectionTimeoutMS: 5000 });

    const removed = await Menu.deleteMany({});
    const inserted = await Menu.insertMany(seedData);
    console.log(`Removed ${removed.deletedCount} item(s), inserted ${inserted.length}:`);
    for (const item of inserted) {
        console.log(`  ${item._id}  ${item.name}  ${item.price} THB`);
    }
    await mongoose.disconnect();
}

main().catch((err) => {
    console.error("Seed failed:", err.message);
    process.exit(1);
});
