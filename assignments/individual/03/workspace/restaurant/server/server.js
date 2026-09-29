require("dotenv").config();
const PROTO_PATH="./restaurant.proto";

//var grpc = require("grpc");
var grpc = require("@grpc/grpc-js");

var protoLoader = require("@grpc/proto-loader");
const mongoose = require("mongoose");
const Menu = require("../models/Menu");

var packageDefinition = protoLoader.loadSync(PROTO_PATH,{
    keepCase: true,
    longs: String,
    enums: String,
    arrays: true
});

var restaurantProto =grpc.loadPackageDefinition(packageDefinition);

const server = new grpc.Server();

// Map a caught error to a gRPC status for the callback.
function toGrpcError(err) {
    if (err.name === "CastError") {
        return { code: grpc.status.NOT_FOUND, details: "Not found" };
    }
    if (err.name === "ValidationError") {
        return { code: grpc.status.INVALID_ARGUMENT, details: err.message };
    }
    return { code: grpc.status.INTERNAL, details: err.message };
}

server.addService(restaurantProto.RestaurantService.service,{
    getAllMenu: async (_,callback)=>{
        try {
            const items = await Menu.find().sort({ createdAt: 1 });
            callback(null, { menu: items.map(item => item.toMenuItem()) });
        } catch (err) {
            callback(toGrpcError(err));
        }
    },
    get: async (call,callback)=>{
        try {
            const menuItem = await Menu.findById(call.request.id);

            if(menuItem) {
                callback(null, menuItem.toMenuItem());
            }else {
                callback({
                    code: grpc.status.NOT_FOUND,
                    details: "Not found"
                });
            }
        } catch (err) {
            callback(toGrpcError(err));
        }
    },
    insert: async (call, callback)=>{
        try {
            const menuItem = await Menu.create({
                name: call.request.name,
                price: call.request.price
            });
            callback(null, menuItem.toMenuItem());
        } catch (err) {
            callback(toGrpcError(err));
        }
    },
    update: async (call,callback)=>{
        try {
            const existingMenuItem = await Menu.findById(call.request.id);

            if(existingMenuItem){
                existingMenuItem.name=call.request.name;
                existingMenuItem.price=call.request.price;
                await existingMenuItem.save();
                callback(null, existingMenuItem.toMenuItem());
            } else {
                callback({
                    code: grpc.status.NOT_FOUND,
                    details: "Not Found"
                });
            }
        } catch (err) {
            callback(toGrpcError(err));
        }
    },
    remove: async (call, callback) => {
        try {
            const deleted = await Menu.findByIdAndDelete(call.request.id);

            if(deleted){
                callback(null,{});
            } else {
                callback({
                    code: grpc.status.NOT_FOUND,
                    details: "NOT Found"
                });
            }
        } catch (err) {
            callback(toGrpcError(err));
        }
    }
});

const ADDRESS = process.env.GRPC_ADDRESS || "127.0.0.1:30043";

async function main() {
    mongoose.set("strictQuery", true);
    await mongoose.connect(process.env.DATABASE_URL);
    console.log("Connected to MongoDB:", mongoose.connection.name);

    server.bindAsync(ADDRESS, grpc.ServerCredentials.createInsecure(), (err) => {
        if (err) throw err;
        server.start();
        console.log("Server running at http://" + ADDRESS);
    });
}

main().catch((err) => {
    console.error("Failed to start:", err.message);
    process.exit(1);
});
