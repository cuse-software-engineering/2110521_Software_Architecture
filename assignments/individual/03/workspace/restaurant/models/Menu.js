const mongoose = require("mongoose");

// MenuSchema: a menu item has a name and a price (THB).
// MongoDB generates _id; the gRPC layer exposes it as the string field `id`
// defined in restaurant.proto (message MenuItem { string id = 1; ... }).
const MenuSchema = new mongoose.Schema(
    {
        name: { type: String, required: true, trim: true },
        price: { type: Number, required: true, min: 0 }
    },
    { timestamps: true }
);

// Convert a Menu document into the MenuItem message shape used by the proto.
MenuSchema.methods.toMenuItem = function () {
    return { id: this._id.toString(), name: this.name, price: this.price };
};

module.exports = mongoose.model("Menu", MenuSchema);
