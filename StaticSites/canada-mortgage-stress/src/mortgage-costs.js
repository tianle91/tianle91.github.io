/* Fixed-rate Canadian mortgage convention: nominal annual, compounded semi-annually. */
(function(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.MortgageCosts = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, () => {
  function paymentFactor(rate, years=25) {
    if (!Number.isFinite(rate) || rate < 0 || rate > 25 || !Number.isFinite(years) || years < 1 || years > 50)
      throw new Error('Invalid mortgage rate or amortization');
    const n = years * 12;
    if (rate === 0) return 1/n;
    const monthly = Math.expm1(Math.log1p(rate/200)/6);
    return monthly / -Math.expm1(-n * Math.log1p(monthly));
  }
  function monthlyPayment(price, rate, down=20, years=25) {
    if (!Number.isFinite(price) || price < 0 || !Number.isFinite(down) || down < 0 || down >= 100)
      throw new Error('Invalid price or down payment');
    return price * (1-down/100) * paymentFactor(rate, years);
  }
  function samePaymentPrice(price, rate, reference=4, years=25) {
    if (!Number.isFinite(price) || price < 0) throw new Error('Invalid price');
    return price * paymentFactor(rate,years) / paymentFactor(reference,years);
  }
  function observations(data, reference=4) {
    const prices = data.groups.find(group => group.id === 'benchmark').series[0].points;
    const rates = data.groups.find(group => group.id === 'mortgage_rates').series[0].points;
    const byMonth = new Map(rates.filter(point=>point.status === 'observed').map(point=>[point.period,point.value]));
    // Exact monthly join only: never interpolate, extend or substitute forecasts.
    const rows = prices.filter(point=>point.status === 'observed' && byMonth.has(point.period)).map(point=>{
      const rate = byMonth.get(point.period);
      return {period:point.period,price:point.value,rate,
        payment:monthlyPayment(point.value,rate), equivalent:samePaymentPrice(point.value,rate,reference)};
    });
    if (rows.length < 2) throw new Error('No shared benchmark and mortgage-rate history');
    return rows;
  }
  return {paymentFactor,monthlyPayment,samePaymentPrice,observations};
});
