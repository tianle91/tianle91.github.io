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
for (const rate of [0,2,4,6]) {
  assert.ok(Math.abs(M.samePaymentPrice(900000,rate,rate)-900000)<1e-8);
  const equivalent=M.samePaymentPrice(900000,rate,4);
  assert.ok(Math.abs(M.monthlyPayment(equivalent,4)-M.monthlyPayment(900000,rate))<1e-8);
}
assert.ok(M.samePaymentPrice(900000,6,4)>900000);
assert.ok(M.samePaymentPrice(900000,2,4)<900000);
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
const missing=structuredClone(data);
missing.groups.find(g=>g.id==='mortgage_rates').series[0].points.pop();
assert.equal(M.observations(missing).at(-1).period,'2026-08');
const forecast=structuredClone(data);
forecast.groups.find(g=>g.id==='mortgage_rates').series[0].points.at(-1).status='forecast';
assert.equal(M.observations(forecast).at(-1).period,'2026-08');
console.log('Mortgage-cost checks passed: FCAC payment, zero rate, same-payment identity, direction, exact-month join and forecast exclusion.');
