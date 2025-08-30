const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Game variables
const WIDTH = canvas.width;
const HEIGHT = canvas.height;
const car = {
  width: 50,
  height: 100,
  x: WIDTH / 2 - 25,
  y: HEIGHT - 120,
  speed: 5,
  color: "red"
};

let obstacles = [];
let lines = [];
let score = 0;
let gameOver = false;

// Create initial road lines
for (let y = 0; y < HEIGHT; y += 40) {
  lines.push({ x: WIDTH / 2 - 5, y });
}

// Draw functions
function drawCar() {
  ctx.fillStyle = car.color;
  ctx.fillRect(car.x, car.y, car.width, car.height);
}

function drawObstacles() {
  ctx.fillStyle = "lime";
  obstacles.forEach((obs) => {
    ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
  });
}

function drawLines() {
  ctx.fillStyle = "white";
  lines.forEach((line) => {
    ctx.fillRect(line.x, line.y, 10, 20);
  });
}

function drawScore() {
  ctx.fillStyle = "white";
  ctx.font = "20px Arial";
  ctx.fillText("Score: " + score, 10, 30);
}

function createObstacle() {
  const x = Math.random() * (WIDTH - 100) + 50;
  obstacles.push({
    x,
    y: -100,
    width: 50,
    height: 100
  });
}

// Game loop
function update() {
  if (gameOver) return;

  // Move road lines
  lines.forEach((line) => {
    line.y += 10;
    if (line.y > HEIGHT) line.y = -20;
  });

  // Add obstacles randomly
  if (Math.random() < 0.03) createObstacle();

  // Move and remove obstacles
  obstacles.forEach((obs, i) => {
    obs.y += 7;
    if (obs.y > HEIGHT) {
      obstacles.splice(i, 1);
      score++;
    }
    // Collision detection
    if (
      car.x < obs.x + obs.width &&
      car.x + car.width > obs.x &&
      car.y < obs.y + obs.height &&
      car.y + car.height > obs.y
    ) {
      gameOver = true;
      alert("💥 Game Over! Final Score: " + score);
      document.location.reload();
    }
  });
}

function render() {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);
  drawLines();
  drawCar();
  drawObstacles();
  drawScore();
  requestAnimationFrame(gameLoop);
}

function gameLoop() {
  update();
  render();
}

// Controls
document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft" && car.x > 0) car.x -= car.speed;
  if (e.key === "ArrowRight" && car.x < WIDTH - car.width) car.x += car.speed;
});

// Start the loop
gameLoop();