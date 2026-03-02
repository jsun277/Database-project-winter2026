// Q7: Fetch cart information: device type, number of items in the cart,
// and total amount.

db.carts.aggregate([
  {
    $project: {
      user_id: 1,
      device: 1,
      num_items: { $size: "$items" },
      total_amount: { $sum: { $map: { input: "$items", as: "i", in: { $multiply: ["$$i.price", "$$i.quantity"] } } } }
    }
  },
  { $sort: { total_amount: -1 } }
]);
