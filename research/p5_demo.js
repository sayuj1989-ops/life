let t = 0;
  
function setup() {
  createCanvas(400, 400);
  stroke(255, 120);
}
  
function organism(x, y) {
  let k = 5 * cos(x / 14) * cos(y / 30);
  let e = y / 8 - 13;
  
  let d = pow(mag(k, e), 2) / 59 + 4;
  
  let angleTerm = atan2(k, e);
  let q = 60 - 3 * sin(angleTerm * e);
  
  let wave = k * (3 + 4 / d * sin(d * d - t * 2));
  
  let c = d / 2 + e / 99 - t / 18;
  
  let xCoord = (q + wave) * sin(c) + 200;
  let yCoord = (q + d * 9) * cos(c) + 200;
  
  point(xCoord, yCoord);
}
  
function draw() {
  background(9);
  t += PI / 20;
  
  for (let i = 0; i < 10000; i++) {
    let x = i % 80;
    let y = i / 43;
    organism(x, y);
  }
}
