document.addEventListener('DOMContentLoaded', function () {
  const onePlayerBtn = document.getElementById('onePlayerBtn');
  const twoPlayerBtn = document.getElementById('twoPlayerBtn');
  const onePlayerOptions = document.querySelectorAll('.game-options')[0];
  const twoPlayerOptions = document.querySelectorAll('.game-options')[1];

  onePlayerBtn.addEventListener('click', () => {
    onePlayerOptions.style.display = 'block';
    twoPlayerOptions.style.display = 'none';
  });

  twoPlayerBtn.addEventListener('click', () => {
    onePlayerOptions.style.display = 'none';
    twoPlayerOptions.style.display = 'block';
  });
});

