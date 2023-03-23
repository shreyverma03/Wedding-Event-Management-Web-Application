let heartCount = 0;

function createHeart() {
  const heart = document.createElement('div');
  heart.classList.add('heart');

  heart.style.left = Math.random() * 100 + "vw";
  heart.style.animationDuration = Math.random() * 2 + 3 + "s";
  heart.innerText = '❤️';
  heart.style.fontSize = '50px';
  document.body.appendChild(heart);

  setTimeout(() => {
    heart.remove();
  }, 5000);

  heartCount++;

}

const intervalId = setInterval(createHeart, 100);
