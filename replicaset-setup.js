// rs.initiate({
// _id: "MainRepSet",
// members: [
//   { _id: 0, host: "mongo-0.mongo.default.svc.cluster.local:27017"
//   },
//   { _id: 1, host: "mongo-1.mongo.default.svc.cluster.local:27017"
//   },
//   { _id: 2, host: "mongo-2.mongo.default.svc.cluster.local:27017"
//   }]
// })
//
rs.initiate();
var cfg = rs.conf();
cfg.members[0].host="mongo-0.mongo:27017";
rs.reconfig(cfg);
rs.add("mongo-1.mongo:27017");
rs.add("mongo-2.mongo:27017");

// config = {
//       "_id" : "rs0",
//       "members" : [
//         {
//           "_id" : 0,
//           "host" : "mongo-0.mongo:27017",
//           "priority": 2
//         },
//         {
//           "_id" : 1,
//           "host" : "mongo1.mongo:27017"
//         },
//         {
//           "_id" : 2,
//           "host" : "mongo2.mongo:27017"
//         }
//       ]
// };
// rs.initiate(config);
