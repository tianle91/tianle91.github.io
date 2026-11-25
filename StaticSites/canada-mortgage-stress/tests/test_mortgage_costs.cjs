'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const M = require('../src/mortgage-costs.js');
const data = JSON.parse(fs.readFileSync(path.join(__dirname,'../data/series.json'),'utf8'));
// Independent FCAC published example: $300k loan, 25 years, 5%, $1,744.81/month.
assert.equal(M.monthlyPayment(300000,5,0).toFixed(2),'1744.81');
assert.ok(Math.abs(M.monthlyPayment(300000,0,0)-1000)<1e-8);
assert.ok(Math.abs(M.monthlyPayment(500000,0,20)-400000/300)<1e-8);
assert.ok(M.monthlyPayment(900000,6)>M.monthlyPayment(900000,4));
assert.ok(M.monthlyPayment(900000,4,20,30)<M.monthlyPayment(900000,4,20,25));
assert.throws(()=>M.paymentFactor(-1));
assert.throws(()=>M.paymentFactor(NaN));
const rows=M.observations(data);
assert.equal(rows[0].period,'2013-01');
assert.equal(rows.at(-1).period,'2026-09'); // October's benchmark has no matching rate.
assert.equal(rows.length,165);
assert.equal(rows.at(-1).price,917600);
assert.equal(rows.at(-1).rate,4.66);
assert.equal(rows[0].priceIndex,100);
assert.equal(rows[0].paymentIndex,100);
for (const row of rows) {
  assert.ok(Math.abs(row.payment-M.monthlyPayment(row.price,row.rate))<1e-8);
  assert.ok(Math.abs(row.paymentIndex-row.payment/rows[0].payment*100)<1e-8);
}
const constantPrices=structuredClone(data);
for (const point of constantPrices.groups.find(g=>g.id==='benchmark').series[0].points) point.value=900000;
const rateOnly=M.observations(constantPrices);
assert.ok(rateOnly.every(row=>row.priceIndex===100));
assert.ok(rateOnly.at(-1).paymentIndex>100); // Later historical rate exceeds starting rate.
const constantRates=structuredClone(data);
for (const point of constantRates.groups.find(g=>g.id==='mortgage_rates').series[0].points) point.value=4;
assert.ok(M.observations(constantRates).every(row=>Math.abs(row.priceIndex-row.paymentIndex)<1e-8));
const missing=structuredClone(data);
missing.groups.find(g=>g.id==='mortgage_rates').series[0].points.pop();
assert.equal(M.observations(missing).at(-1).period,'2026-08');
const forecast=structuredClone(data);
forecast.groups.find(g=>g.id==='mortgage_rates').series[0].points.at(-1).status='forecast';
assert.equal(M.observations(forecast).at(-1).period,'2026-08');
console.log('Mortgage-cost checks passed: FCAC payment, zero rate, historical monthly rates, price/payment indexes, direction, exact-month join and forecast exclusion.');
