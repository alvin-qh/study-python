;
(() => {
  window.home = window.home || {};
  window.home['index'] = function () {
    const input = document.querySelector('input[type=text]');
    const link = document.querySelector('a');

    input.addEventListener('input', function (e) {
      link.href = '/user?name=' + e.currentTarget.value;
    }, false);
  };
})();
